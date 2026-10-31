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


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


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
    offs = sorted(o for _, o in ent)  # name order = data order, except pack's `late` files (placed last)
    assert offs[0] == datap, 'first file not at the data offset'
    nxt = dict(zip(offs, offs[1:] + [None]))
    return [(name, base + off, nxt[off] - off if nxt[off] is not None else None) for name, off in ent]


END = 0xF28406  # first byte after the archive (code-referenced data follows; docs/re/nfp.md)


def unpack(rom, base=BASE):
    """[(name, stored bytes)]: LZ77 and SCRP files trimmed to their real length (the zero fill after them is
    alignment), raw files keep their whole slot."""
    import gbalz
    out = []
    for name, off, size in entries(rom, base):
        size = size if size is not None else (END if off < END else SPILL_END) - off
        k = kind(rom, off)
        n = gbalz.decompress(rom, off)[1] if k == 'lz' else 8 + struct.unpack_from('<I', rom, off + 4)[0] if k == 'scrp' else size
        assert n <= size and (off + size > END or not rom[off + n:off + size].strip(b'\0')), name  # > END: jumps GAP
        out.append((name, rom[off:off + n]))
    return out


GAP = (END, 0xF2B450)  # code-referenced data the archive may jump over; free 0xFF fill after it
SPILL_END = 0xFE0000


LATE = ('MAP42_A.KMP',)  # 231 KB map, follows an .SPC: its data may sit in the spill (pelica_free warp loads it)


def pack(files, header, base=BASE, late=None):
    """Archive bytes from [(name, stored bytes)] in directory order; each file starts 16-aligned, zero fill.

    Returns {ROM offset: bytes} (one block, or two when it doesn't fit before GAP). The game sizes a file as next
    entry's offset - its own (0x0807AD4C, used for KCG/KCL named by a KMP), so data stays in directory order and the
    jump over GAP comes right after an .SPC, whose size is never taken that way: no raw file's size changes.
    When that doesn't fit (SYSTEM.NCD, 1.3 MB raw, sits right before GAP), the `late` files' data goes last, past
    GAP: lookups are by name, and a late file's directory predecessor is an .SPC, so no KCG/KCL size changes."""
    if late is None:
        try:
            return pack(files, header, base, ())
        except AssertionError:
            return pack(files, header, base, LATE)
    names = [n for n, _ in files]
    for n in late:
        assert names[names.index(n) - 1].endswith('.SPC'), n
    order = sorted(range(len(files)), key=lambda i: files[i][0] in late)  # stable: late data at the end
    files = [files[i] for i in order]
    count = len(files)
    datap = 0x40 + 16 * count
    offs, p = [], datap
    for name, b in files:
        offs.append(p)
        p += len(b) + (-len(b) % 16)
    end = offs[-1] + len(files[-1][1])
    gap = None
    if base + end > GAP[0]:
        over = next(i for i in range(count) if base + offs[i] + len(files[i][1]) > GAP[0])
        j = next(j for j in range(over, 0, -1) if files[j - 1][0].endswith('.SPC'))
        gap = offs[j]
        end1 = offs[j - 1] + len(files[j - 1][1])  # not padded: the 16-alignment could reach into GAP
        shift = GAP[1] - base - gap
        offs[j:] = [o + shift for o in offs[j:]]
        end += shift
        assert base + end <= SPILL_END, 'archive past 0x%X' % SPILL_END
    hdr = bytearray(header[:0x40])
    struct.pack_into('<3I', hdr, 0x34, count, 0x40, datap)
    dir_offs = dict(zip(order, offs))  # the directory stays in name order
    for i, name in enumerate(names):
        hdr += name.encode('ascii').ljust(12, b'\0') + struct.pack('<I', dir_offs[i])
    blob = bytearray(end - (shift if gap else 0))
    blob[:datap] = hdr
    for (name, b), o in zip(files, offs):
        o -= shift if gap and o >= GAP[1] - base else 0
        blob[o:o + len(b)] = b
    if not gap:
        return {base: bytes(blob)}
    return {base: bytes(blob[:end1]), GAP[1]: bytes(blob[gap:])}


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
