"""build.py: original ROM -> build/maer_en.gba.

Unpacks MAR.NFP, rebuilds every script (scrp.rebuild relocates code when a string changes length), repacks the
archive in place and writes the ROM. Files whose bytes don't change keep their original stored (LZ77) bytes, since
our compressor's output differs from the original packer's. With no edits the output equals the original
(tests/test_build.py). With English text (or --marker) the engine patch goes in too (tools/engine.py: VWF font
and hooks).

    python -X utf8 tools/build.py [OUT] [--recompress] [--marker]

--marker: every script line becomes `[n]` + filler text (ids in <OUT dir>/marker_ids.tsv), the phase 5 marker build.
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
import nfp  # noqa: E402
import scrp  # noqa: E402
import text  # noqa: E402

ROM = ROOT / "rom" / "MAER Heaven - Knockin' on Heaven's Door (Japan).gba"
OUT = ROOT / "build" / "maer_en.gba"
SCRIPT = ROOT / "script"


def build(rom, edits=None, recompress=False, patch_engine=False):
    """edits: {SPC name: {CODE pos of a 0x10 op: new string bytes}}.
    recompress: re-pack every LZ77 script with our compressor (test ROM: proves our LZ77 and the moved archive).
    patch_engine: English font + VWF hooks (tools/engine.py)."""
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
        files.append((name, b))
    blocks = nfp.pack(files, rom[nfp.BASE:nfp.BASE + 0x40])
    out = bytearray(rom)
    for off, b in blocks.items():
        out[off:off + len(b)] = b
    end = nfp.BASE + len(blocks[nfp.BASE])
    out[end:nfp.END] = bytes(nfp.END - end)
    if patch_engine:
        engine.apply(out)
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


def main(a):
    check_rom.check()
    rom = ROM.read_bytes()
    rc, mk = '--recompress' in a, '--marker' in a
    a = [x for x in a if not x.startswith('--')]
    out = Path(a[0]) if a else OUT
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = script_lines()
    if mk:
        lines, ids = marker(lines)
        (out.parent / 'marker_ids.tsv').write_text(''.join('%d\t%s\n' % x for x in ids), encoding='utf-8')
    edits = edits_from(lines)
    b = build(rom, edits, recompress=rc, patch_engine=bool(edits))
    out.write_bytes(b)
    print('%s %s%s' % (out, hashlib.sha1(b).hexdigest(), ' (identical to original)' if b == rom else ''))


if __name__ == '__main__':
    main(sys.argv[1:])
