"""NFP2.0 archive (MAR.NFP, ROM 0x1C0920): every game file by name. See docs/re/nfp.md.

Header (0x40 bytes): 'NFP2.0 (c)NOBORI 1997-2002' ... +0x34 u32 count, +0x38 u32 dir offset, +0x3C u32 data offset.
Directory: count x 16 bytes = name (12 bytes, NUL-padded) + u32 file offset from the archive start.
A file's size is the next entry's offset minus its own (entries are sorted by offset; checked in entries()).

    python -X utf8 tools/nfp.py list                 name, ROM offset, size, kind
    python -X utf8 tools/nfp.py extract OUTDIR       every file, unpacked where LZ77 (name.bin = raw stored bytes)
"""
import os
import struct
import sys

ROM = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'rom',
                   "MAER Heaven - Knockin' on Heaven's Door (Japan).gba")
BASE = 0x1C0920


def entries(rom, base=BASE):
    """[(name, rom_offset, size)]; the last file ends at the archive end (first non-file byte, see END)."""
    assert rom[base:base + 6] == b'NFP2.0', rom[base:base + 16]
    count, dirp, datap = struct.unpack_from('<3I', rom, base + 0x34)
    ent = []
    for i in range(count):
        e = base + dirp + 16 * i
        name = rom[e:e + 12].rstrip(b'\0').decode('ascii')
        off = struct.unpack_from('<I', rom, e + 12)[0]
        ent.append((name, off))
    offs = [o for _, o in ent]
    assert offs == sorted(offs) and offs[0] == datap, 'directory not sorted by offset'
    out = []
    for i, (name, off) in enumerate(ent):
        nxt = ent[i + 1][1] if i + 1 < count else None
        out.append((name, base + off, (nxt - off) if nxt is not None else None))
    return out


def kind(rom, off):
    b = rom[off:off + 8]
    if b[:4] == b'SCRP':
        return 'scrp'
    if b[0] == 0x10:
        return 'lz'
    return 'raw'


def main(a):
    rom = open(ROM, 'rb').read()
    ents = entries(rom)
    if a and a[0] == 'list':
        for name, off, size in ents:
            print('%-12s %07x %7s %s' % (name, off, size, kind(rom, off)))
    elif a and a[0] == 'extract':
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import gbalz
        os.makedirs(a[1], exist_ok=True)
        for name, off, size in ents:
            data = rom[off:off + size] if size else rom[off:off + 0x10000]
            open(os.path.join(a[1], name + '.bin'), 'wb').write(data)
            if kind(rom, off) == 'lz':
                try:
                    open(os.path.join(a[1], name), 'wb').write(gbalz.decompress(rom, off)[0])
                except (ValueError, IndexError):
                    pass
    else:
        print(__doc__)


if __name__ == '__main__':
    main(sys.argv[1:])
