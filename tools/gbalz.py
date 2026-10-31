"""GBA BIOS LZ77 (type 0x10) codec and ROM scanner.

    python tools/gbalz.py scan ROM [--min 256] [--out work/lz]   list (and dump) plausible LZ77 blocks
    python tools/gbalz.py unpack ROM OFFSET OUT                  decompress one block

decompress() returns (data, compressed_size). compress() is VRAM-safe (no disp-0 refs, i.e. disp >= 2).
"""
import os
import sys


def decompress(d, off):
    if d[off] != 0x10:
        raise ValueError('not LZ77 at %x' % off)
    size = d[off + 1] | d[off + 2] << 8 | d[off + 3] << 16
    out = bytearray()
    p = off + 4
    while len(out) < size:
        flags = d[p]
        p += 1
        for bit in range(8):
            if len(out) >= size:
                break
            if flags & (0x80 >> bit):
                b1, b2 = d[p], d[p + 1]
                p += 2
                n = (b1 >> 4) + 3
                disp = ((b1 & 0xF) << 8 | b2) + 1
                if disp > len(out):
                    raise ValueError('bad backref at %x' % p)
                for _ in range(n):
                    out.append(out[-disp])
            else:
                out.append(d[p])
                p += 1
    return bytes(out[:size]), p - off


def compress(data, vram_safe=True):
    """Greedy LZ77 with a hash chain. Not byte-identical to the original packer."""
    n = len(data)
    out = bytearray([0x10, n & 0xFF, n >> 8 & 0xFF, n >> 16 & 0xFF])
    mind = 2 if vram_safe else 1
    heads = {}
    i = 0
    while i < n:
        flag_pos = len(out)
        out.append(0)
        flags = 0
        for bit in range(8):
            if i >= n:
                break
            best_len, best_d = 0, 0
            if i + 3 <= n:
                key = data[i:i + 3]
                for j in reversed(heads.get(key, [])[-64:]):
                    disp = i - j
                    if disp > 0x1000:
                        break
                    if disp < mind:
                        continue
                    ln = 0
                    while ln < 18 and i + ln < n and data[j + ln] == data[i + ln]:
                        ln += 1
                    if ln > best_len:
                        best_len, best_d = ln, disp
                        if ln == 18:
                            break
            if best_len >= 3:
                flags |= 0x80 >> bit
                v = (best_len - 3) << 12 | (best_d - 1)
                out += bytes([v >> 8, v & 0xFF])
                step = best_len
            else:
                out.append(data[i])
                step = 1
            for k in range(i, min(i + step, n - 2)):
                heads.setdefault(data[k:k + 3], []).append(k)
            i += step
        out[flag_pos] = flags
    while len(out) % 4:
        out.append(0)
    return bytes(out)


def scan(d, min_size=256, max_size=0x40000):
    """Yield (offset, size, csize) for 4-aligned offsets that decode cleanly."""
    for off in range(0, len(d) - 4, 4):
        if d[off] != 0x10:
            continue
        size = d[off + 1] | d[off + 2] << 8 | d[off + 3] << 16
        if size < min_size or size > max_size:
            continue
        try:
            data, csize = decompress(d, off)
        except (ValueError, IndexError):
            continue
        if csize >= size + size // 8 + 8:  # worse than stored: not real
            continue
        yield off, size, csize


def _selftest():
    import random
    r = random.Random(1)
    for n in (0, 1, 5, 100, 5000):
        s = bytes(r.choice(b'abcab\x00\x00') for _ in range(n))
        c = compress(s)
        assert decompress(c, 0)[0] == s, n


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] == 'selftest':
        _selftest()
        print('ok')
    elif a[0] == 'scan':
        d = open(a[1], 'rb').read()
        mn = int(a[a.index('--min') + 1]) if '--min' in a else 256
        out = a[a.index('--out') + 1] if '--out' in a else None
        if out:
            os.makedirs(out, exist_ok=True)
        for off, size, cs in scan(d, mn):
            print('%07x %6d %6d' % (off, size, cs))
            if out:
                open(os.path.join(out, '%07x.bin' % off), 'wb').write(decompress(d, off)[0])
    elif a[0] == 'unpack':
        d = open(a[1], 'rb').read()
        open(a[3], 'wb').write(decompress(d, int(a[2], 16))[0])
