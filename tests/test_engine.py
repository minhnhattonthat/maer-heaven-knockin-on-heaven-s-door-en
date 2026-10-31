"""Phase 5 engine patch (docs/re/vwf.md): font, hooks, English encoding, marker build."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build  # noqa: E402
import engine  # noqa: E402
import nfp  # noqa: E402
import gbalz  # noqa: E402
import scrp  # noqa: E402
import text  # noqa: E402

needs_rom = pytest.mark.skipif(not build.ROM.is_file(), reason="ROM not present")


def test_font_and_widths():
    g = engine.glyphs()
    assert all(rows[7] == 0 or c in b'gjpqy,;_' for c, (rows, _) in g.items())  # row 7: descenders only
    adv = engine.advance()
    assert engine.width(b'Hi', adv) == adv[ord('H') - 32] + adv[ord('i') - 32]
    assert engine.width(b'C0D04[A]C0F04', adv) == engine.width(b'[A]', adv)  # codes take no room
    assert engine.width(b'Cafe!', adv) == sum(adv[c - 32] for c in b'Cafe!')  # C + non-hex is a letter
    assert engine.width(b'T0000 C0F04Hi', adv) == engine.width(b'Hi', adv)  # space after T0000 is skipped
    assert engine.width(b'their x', adv) == sum(adv[c - 32] for c in b'their x')


def test_encode_en():
    assert text.encode_en('{C0D04}[Ginta]{C0F04}') == b'C0D04[Ginta]C0F04'
    assert text.encode_en('MÄR…') == b'M' + bytes.fromhex('f056') + 'R…'.encode('cp932')
    assert text.encode_en('HP{p12}') == b'HP\x0c' and text.encode_en('{p32}') == b'{p32}'


def test_list_width_pads():
    adv = engine.advance()
    assert engine.list_width(b'HP\x0c', 0, adv) == engine.list_width(b'HP', 0, adv) + 12
    assert engine.list_width('木１'.encode('cp932'), 1, adv) == 18  # 2-byte glyphs: 8 + spacing
    assert engine.list_width(b'Hi', 1, adv) == engine.width(b'Hi', adv)  # ASCII: no window spacing
    assert engine.pxlen('ギンタ'.encode('cp932')) == 6 and engine.pxlen(b'Phantom') == 10
    stub = bytearray(b'\xff' * (0x60 + 0x260 * 8))
    stub[:3], stub[0x20], stub[0x24], stub[0x38] = b'NFT', 8, 8, 8
    assert engine.font(bytes(stub))[0x60 + (engine.GLYPH0 + 5) * 8:][:8] == bytes(8)  # pad glyphs are blank


def test_fit_code_pads_and_keeps():
    es = [{'id': 'a', 'jp': 'x', 'en': 'HP'}, {'id': 'b', 'jp': 'x', 'en': 'W' * 9}, {'id': 'k', 'jp': '０', 'en': ''}]
    build.fit_code(es, {'a': {'pad_to': 40}, 'b': {'pad_to': 80}, 'k': {'keep': True}})
    assert [engine.list_width(text.encode_en(e['en'])) for e in es[:2]] == [40, 80]
    assert es[2]['en'] == '０'


def test_every_code_string_has_one_window():
    import json
    ids = [e['id'] for e in json.loads((ROOT / 'script' / 'code.json').read_text(encoding='utf-8'))]
    wins = json.loads((ROOT / 'script' / 'windows.json').read_text(encoding='utf-8'))['code']
    listed = [i for k, w in wins.items() if not k.startswith('_') for i in w['ids']]
    assert sorted(listed) == sorted(ids)


@needs_rom
def test_patches_apply_to_original():
    rom = bytearray(build.ROM.read_bytes())
    engine.apply(rom)  # asserts the original bytes at every site and that free space is unused


@needs_rom
def test_marker_build_scripts():
    """Every script of the marker build parses and keeps CODE size 2 mod 4 (the VM's stack-top write)."""
    rom = build.ROM.read_bytes()
    lines, _ = build.marker(build.script_lines())
    out = build.build(rom, build.edits_from(lines), patch_engine=True)
    for name, b in nfp.unpack(out):
        if name.endswith('.SPC'):
            raw = gbalz.decompress(b, 0)[0] if b[0] == 0x10 else b
            assert scrp.chunks(raw)['CODE'][1] % 4 == 2, name
