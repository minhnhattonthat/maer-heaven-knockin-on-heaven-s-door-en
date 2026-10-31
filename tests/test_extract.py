"""Phase 4 extract (docs/re/text.md §Script files): every extracted string re-encodes to its original bytes, every
Japanese byte in the text ranges is covered, and script/ matches a fresh extraction of the ROM."""
import json
import struct
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import extract  # noqa: E402
import scrp  # noqa: E402
import text  # noqa: E402

needs_rom = pytest.mark.skipif(not extract.ROM.is_file(), reason="ROM not present")


@pytest.fixture(scope='module')
def rom():
    return extract.ROM.read_bytes()


@pytest.fixture(scope='module')
def files(rom):
    return extract.extract(rom)


def test_codec_tokens():
    for b in [b' C0D04 \x81\x6d\x83\x4d\x81\x6e C0F04 ', b'\xf0\x56\x82\x71\xf0\x40\xf0\x41', b'C0F04 x  C0F04 ']:
        assert text.encode(text.decode(b)) == b
    assert text.decode(b'\xf0\x56\xf0\x40 C0904 ') == 'Ä♥{C0904}'


def _bytes(rom, e):
    """Original bytes of an entry, read independently of the extractor's decode."""
    if e['id'].startswith('code:'):
        a = int(e['id'][5:], 16)
        return rom[a:rom.index(b'\0', a)]
    if 'addr' in e:
        a = int(e['addr'], 16)
        return rom[a:a + e['max'] + 1].split(b'\0')[0]
    return None


@needs_rom
def test_roundtrip(rom, files):
    scripts = {n[:-4]: b for _, b, n in scrp.load_rom_scripts(rom, True)}
    for ents in files.values():
        for e in ents:
            orig = _bytes(rom, e)
            if orig is None:
                name, pos = e['id'].split(':')
                b = scripts[name]
                s, _ = scrp.chunks(b)['CODE']
                p = s + int(pos, 16)
                assert b[p] == 0x10
                orig = b[p + 3:p + 3 + struct.unpack_from('<H', b, p + 1)[0] - 1]
            assert text.encode(e['jp']) == orig, e['id']


@needs_rom
def test_script_coverage(rom, files):
    """Every script string is either extracted or a pure-ASCII identifier; 5 563 display strings, plus 1 328 empty
    MswStr lines (spare lines for the English)."""
    ents = {e['id']: e for k, v in files.items() if k.startswith('spc/') for e in v}
    n = 0
    for _, b, name in scrp.load_rom_scripts(rom, True):
        s, sz = scrp.chunks(b)['CODE']
        for p, op, arg in scrp.instrs(b[s:s + sz]):
            if op == 0x10:
                key = '%s:%05x' % (name[:-4], p)
                if not arg[2:-1] and key in ents:
                    assert ents[key]['call'] == 'MswStr' and ents[key]['jp'] == '', key
                    continue
                assert (key in ents) == extract.is_text(arg[2:-1]), key
                n += key in ents
    assert n == 5563 and len(ents) == 5563 + 1328


@needs_rom
def test_code_block_coverage(rom, files):
    """Each byte of the string block is NUL, in a pure-ASCII string, or in an extracted string; each extracted string
    has a pointer (subrefs: the one pointer into a string's middle)."""
    lo, hi = extract.CODE_BLOCK
    got = {int(e['id'][5:], 16): e for e in files['code.json']}
    i = lo
    while i < hi:
        j = rom.index(b'\0', i)
        assert j < hi
        assert (i in got) == extract.is_text(rom[i:j]), hex(i)
        i = j + 1
    assert all(e['refs'] for e in got.values())
    # no Japanese just outside the block
    assert not extract.is_text(rom[lo - 0x40:lo]) and rom[hi - 1] == 0


@needs_rom
def test_record_fields_padded(rom, files):
    """Record text fields hold one string followed only by zero fill (nothing hidden after the NUL)."""
    for tab, base, n, size, fields in extract.TABLES:
        for k in range(n):
            for f, off, ln in fields:
                a = base + k * size + off
                fld = rom[a:a + ln]
                e = fld.index(b'\0')
                assert not any(fld[e:]), (tab, k, f)
    assert len(files['records.json']) == 917


def test_reextract_keeps_english(tmp_path):
    p = tmp_path / 'x.json'
    extract.write(p, [{'id': 'a', 'jp': 'あ', 'en': ''}, {'id': 'b', 'jp': 'い', 'en': ''}])
    disk = extract.load(p)
    disk[0]['en'], disk[1]['en'], disk[1]['notes'] = 'A', 'B', 'n'
    p.write_text(json.dumps(disk, ensure_ascii=False), encoding='utf-8')  # a translator's edit
    assert extract.write(p, [{'id': 'a', 'jp': 'あ', 'en': ''}, {'id': 'b', 'jp': 'う', 'en': ''}]) == 1
    assert extract.load(p) == [{'id': 'a', 'jp': 'あ', 'en': 'A'},
                               {'id': 'b', 'jp': 'う', 'en': 'B', 'notes': 'n', 'status': 'jp-changed'}]


@needs_rom
def test_script_dir_in_sync(files):
    """script/ was extracted from this ROM: same ids and jp (translator fields aside)."""
    for k, ents in files.items():
        path = extract.OUT / k
        assert path.is_file(), k
        disk = extract.load(path)
        assert [(e['id'], e['jp']) for e in disk] == [(e['id'], e['jp']) for e in ents], k
    assert len(list((extract.OUT / 'spc').glob('*.json'))) == sum(k.startswith('spc/') for k in files)
