"""build.py: original ROM -> build/maer_en.gba.

Unpacks MAR.NFP, rebuilds every script (scrp.rebuild relocates code when a string changes length), repacks the
archive in place and writes the ROM. Files whose bytes don't change keep their original stored (LZ77) bytes, since
our compressor's output differs from the original packer's. With no edits the output equals the original
(tests/test_build.py).

    python -X utf8 tools/build.py [OUT] [--recompress]
"""
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import check_rom  # noqa: E402
import gbalz  # noqa: E402
import nfp  # noqa: E402
import scrp  # noqa: E402

ROM = ROOT / "rom" / "MAER Heaven - Knockin' on Heaven's Door (Japan).gba"
OUT = ROOT / "build" / "maer_en.gba"


def build(rom, edits=None, recompress=False):
    """edits: {SPC name: {CODE pos of a 0x10 op: new string bytes}} (phase 4 fills this).
    recompress: re-pack every LZ77 script with our compressor (test ROM: proves our LZ77 and the moved archive)."""
    edits = edits or {}
    files = []
    for name, b in nfp.unpack(rom):
        if name.endswith('.SPC'):
            raw = gbalz.decompress(b, 0)[0] if b[0] == 0x10 else b
            new = scrp.rebuild(raw, edits.get(name))
            if new != raw or (recompress and b[0] == 0x10):
                b = gbalz.compress(new) if b[0] == 0x10 else new
        files.append((name, b))
    blocks = nfp.pack(files, rom[nfp.BASE:nfp.BASE + 0x40])
    out = bytearray(rom)
    for off, b in blocks.items():
        out[off:off + len(b)] = b
    end = nfp.BASE + len(blocks[nfp.BASE])
    out[end:nfp.END] = bytes(nfp.END - end)
    return bytes(out)


def main(a):
    check_rom.check()
    rom = ROM.read_bytes()
    rc = '--recompress' in a
    a = [x for x in a if x != '--recompress']
    out = Path(a[0]) if a else OUT
    out.parent.mkdir(parents=True, exist_ok=True)
    b = build(rom, recompress=rc)
    out.write_bytes(b)
    print('%s %s%s' % (out, hashlib.sha1(b).hexdigest(), ' (identical to original)' if b == rom else ''))


if __name__ == '__main__':
    main(sys.argv[1:])
