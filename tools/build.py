"""build.py: original ROM -> build/maer_en.gba.

Unpacks MAR.NFP, rebuilds every script (scrp.rebuild relocates code when a string changes length), repacks the
archive in place and writes the ROM. Files whose bytes don't change keep their original stored (LZ77) bytes, since
our compressor's output differs from the original packer's. With no edits the output equals the original
(tests/test_build.py). With English text (or --marker) the engine patch goes in too (tools/engine.py: VWF font
and hooks).

    python -X utf8 tools/build.py [OUT] [--recompress] [--marker]

--marker: every script line becomes `[n]` + filler text (ids in <OUT dir>/marker_ids.tsv), the phase 5 marker build.
--qa=ID=TEXT (repeatable): override one script line's English (width and glyph tests).
--records-test / --code-test: ÄRM/item records / code strings get exact-width test strings (tools/widthtest.py).
Code strings follow script/windows.json 'code': `keep` windows stay Japanese, `pad_to` windows get pad bytes.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import check_rom  # noqa: E402
import engine  # noqa: E402
import gbalz  # noqa: E402
import gfxtext  # noqa: E402
import nfp  # noqa: E402
import scrp  # noqa: E402
import text  # noqa: E402

ROM = ROOT / "rom" / "MAER Heaven - Knockin' on Heaven's Door (Japan).gba"
OUT = ROOT / "build" / "maer_en.gba"
SCRIPT = ROOT / "script"


def put(out, off, data, by, log):
    """Every ROM write goes through here; log gets (offset, bytes replaced, bytes written, writer) for
    romdiff.check (tests/test_romdiff.py: overlaps, overwrites, writes outside the allowed ranges)."""
    if log is not None:
        log.append((off, bytes(out[off:off + len(data)]), bytes(data), by))
    out[off:off + len(data)] = data


def build(rom, edits=None, recompress=False, patch_engine=False, log=None):
    """edits: {SPC name: {CODE pos of a 0x10 op: new string bytes}}.
    recompress: re-pack every LZ77 script with our compressor (test ROM: proves our LZ77 and the moved archive).
    patch_engine: English font + VWF hooks (tools/engine.py). log: see put()."""
    edits = edits or {}
    files = []
    for name, b in nfp.unpack(rom):
        if name.endswith('.SPC'):
            raw = gbalz.decompress(b, 0)[0] if b[0] == 0x10 else b
            new = scrp.rebuild(raw, edits.get(name))
            if new != raw or (recompress and b[0] == 0x10):
                b = gbalz.compress(new) if b[0] == 0x10 else new
        elif name == 'FONT.NFT' and patch_engine:
            b = engine.font(b)
        elif name.endswith('.NCD') and patch_engine:
            b = gfxtext.apply(name, b)  # English lettering on sprite frames (gfx/<bank>.tsv)
        files.append((name, b))
    blocks = nfp.pack(files, rom[nfp.BASE:nfp.BASE + 0x40])
    out = bytearray(rom)
    for off, b in blocks.items():
        put(out, off, b, 'archive', log)
    end = nfp.BASE + len(blocks[nfp.BASE])
    put(out, end, bytes(nfp.END - end), 'archive fill', log)
    if patch_engine:
        engine.apply(out, log)
    return bytes(out)


def script_lines():
    """[(SPC name, entry)] for every script line, in file order."""
    return [(p.stem + '.SPC', e) for p in sorted((SCRIPT / 'spc').glob('*.json'))
            for e in json.loads(p.read_text(encoding='utf-8'))]


# Debug chapter select: unreachable in normal play, and warp.lua jumps to fixed code offsets inside it, so its
# code must not move (docs/re/debug.md). It stays Japanese.
KEEP_SCRIPTS = {'CH_ESC.SPC'}


def edits_from(lines):
    """{SPC: {pos: bytes}} from [(SPC, entry with 'en')], skipping empty en."""
    edits = {}
    for spc, e in lines:
        if e.get('en') and spc not in KEEP_SCRIPTS:
            edits.setdefault(spc, {})[int(e['id'].split(':')[1], 16)] = text.encode_en(e['en'])
    return edits


FILLER = 'The quick brown fox jumps over the lazy dog while Ginta waves at Babbo ' * 3


def marker(lines, px=184):
    """Marker text per line: `[n]` + filler cut at px pixels; speaker labels keep their colour codes.
    Returns (lines with en set, [(n, id)])."""
    adv, out, ids = engine.advance(), [], []
    lines = [x for x in lines if x[1]['jp']]  # spare empty lines stay empty
    for n, (spc, e) in enumerate(lines):
        tag = '[%d]' % n
        if e['jp'].startswith('{C0D04}'):
            en = '{C0D04}' + tag + '{C0F04}'
        else:
            en = tag
            for ch in FILLER:
                if engine.width(text.encode_en(en + ch), adv) > px:
                    break
                en += ch
        out.append((spc, dict(e, en=en)))
        ids.append((n, e['id']))
    return out, ids


STRINGS = (0xFE8000, engine.FREE_END)  # relocated code-block strings (after the engine hooks at 0xFE4000)


def patch_code(out, entries, log=None):
    """Code-block strings with `en`: written to free space, every pointer in `refs` repointed (refs to the middle,
    `subrefs`, get their own copy of the tail: `en_sub` {offset: text} or the tail of `en` at the same offset)."""
    at = STRINGS[0]
    for e in entries:
        if not e.get('en'):
            continue
        targets = [(text.encode_en(e['en']), e['refs'])]
        for k, refs in e.get('subrefs', {}).items():
            targets.append((text.encode_en(e.get('en_sub', {}).get(k, '')) or targets[0][0], refs))
        for b, refs in targets:
            assert at + len(b) + 1 <= STRINGS[1], 'string space full'
            put(out, at, b + b'\0', e['id'], log)
            for r in refs:
                r = int(r, 16)
                assert out[r + 3] == 0x08, (e['id'], hex(r))
                put(out, r, (0x08000000 + at).to_bytes(4, 'little'), e['id'] + ' ref', log)
            at = (at + len(b) + 4) & ~3


def code_windows():
    """{code id: window spec} from script/windows.json 'code' (tools/widthtest.py, phase 6 lint)."""
    w = json.loads((SCRIPT / 'windows.json').read_text(encoding='utf-8'))['code']
    return {i: dict(v, name=k) for k, v in w.items() if not k.startswith('_') for i in v['ids']}


def fit_code(entries, wins=None):
    """Window rules on code strings: `keep` windows get en = jp; `pad_to` windows get pad bytes ({pN}) after the
    English so the digits the game appends start at exactly pad_to px (engine.list_width)."""
    wins = wins or code_windows()
    for e in entries:
        w = wins.get(e['id'], {})
        if w.get('keep') and not e.get('en'):
            e['en'] = e['jp']
        if e.get('en') and w.get('pad_to'):
            gap = w['pad_to'] - engine.list_width(text.encode_en(e['en']))
            assert gap >= 0, (e['id'], e['en'], 'wider than pad_to')
            while gap:
                e['en'] += '{p%d}' % min(gap, 31)
                gap -= min(gap, 31)


def patch_records(out, entries, log=None):
    """ARM/item name and description fields with `en`, in place (field 0x22 bytes: max 33 + NUL)."""
    for e in entries:
        if e.get('en'):
            b = text.encode_en(e['en'])
            assert len(b) <= e['max'], (e['id'], len(b))
            put(out, int(e['addr'], 16), b.ljust(e['max'] + 1, b'\0'), e['id'], log)


def marker_tables(code, records):
    """Marker text for code strings ([cN], format specifiers and codes kept in order) and record fields ([rN])."""
    import re
    for n, e in enumerate(code):
        keep = ''.join(re.findall(r'%[sd]|\{C[0-9A-F]{4}\}', e['jp']))
        e['en'] = '[c%d]%s' % (n, keep)
        if e.get('subrefs'):
            e['en_sub'] = {k: '[c%d+%s]' % (n, k) for k in e['subrefs']}
    for n, e in enumerate(records):
        e['en'] = ('[r%d]' % n + 'Quick brown fox jumps over the lazy dog')[:e['max']]


def make(rom, lines, code, records, recompress=False, log=None):
    """The ROM for script lines + code strings + records (their `en`); no English at all = identity build."""
    edits = edits_from(lines)
    english = bool(edits) or any(e.get('en') for e in code + records)
    if english:
        fit_code(code)
    b = bytearray(build(rom, edits, recompress=recompress, patch_engine=english, log=log))
    patch_code(b, code, log)
    patch_records(b, records, log)
    return bytes(b)


def load_tables():
    return [json.loads((SCRIPT / n).read_text(encoding='utf-8')) for n in ('code.json', 'records.json')]


def main(a):
    check_rom.check()
    rom = ROM.read_bytes()
    rc, mk = '--recompress' in a, '--marker' in a
    qa_args = [x[5:] for x in a if x.startswith('--qa=')]
    a_all, a = a, [x for x in a if not x.startswith('--')]
    out = Path(a[0]) if a else OUT
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = script_lines()
    code, records = load_tables()
    if mk:
        lines, ids = marker(lines)
        marker_tables(code, records)
        ids += [('c%d' % n, e['id']) for n, e in enumerate(code)] + [('r%d' % n, e['id']) for n, e in enumerate(records)]
        (out.parent / 'marker_ids.tsv').write_text(''.join('%s\t%s\n' % x for x in ids), encoding='utf-8')
    if '--records-test' in sys.argv + a_all:
        import widthtest
        t = widthtest.record_tests(records)
        for e in records:
            e['en'] = t[e['id']]
    if '--code-test' in a_all:
        import widthtest
        wins = code_windows()
        t = widthtest.code_tests(wins)
        for e in code:
            e['en'] = e['jp'] if wins.get(e['id'], {}).get('keep') else t.get(e['id'], e['en'])
    qa = dict(x.split('=', 1) for x in qa_args)
    lines = [(s, dict(e, en=qa[e['id']]) if e['id'] in qa else e) for s, e in lines]
    b = make(rom, lines, code, records, rc)
    out.write_bytes(b)
    print('%s %s%s' % (out, hashlib.sha1(b).hexdigest(), ' (identical to original)' if b == rom else ''))


if __name__ == '__main__':
    main(sys.argv[1:])
