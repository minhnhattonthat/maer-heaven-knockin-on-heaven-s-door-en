"""SCRP script container (LZ77-packed event scripts): parse, disassemble, check.

Layout (docs/re/script.md): 'SCRP' u32 size, then chunks 'CODE' u32 size <bytes>, 'FUNC' u32 size <bytes>,
CODE bytes: u16 0x0400, u32 nlocals, then instructions (opcode + fixed operands; see OPS).

    python -X utf8 tools/scrp.py check            parse every script in the ROM, verify jump targets
    python -X utf8 tools/scrp.py dis OFFSET       disassemble one script (ROM offset of its LZ77 block)
"""
import struct
import sys

# opcode -> operand byte count; 'str' = u16 len + bytes (NUL incl.), 'sw' = u8, u8 n, n*(u32 value, u32 target)
OPS = {0x00: 0, 0x10: 'str', 0x11: 4, 0x12: 5, 0x15: 'sw', 0x20: 2, 0x21: 5, 0x22: 5, 0x28: 1, 0x29: 4,
       0x2a: 1, 0x30: 2, 0x31: 5, 0x32: 2, 0x33: 5, 0x37: 5, 0x3a: 1, 0x35: 5, 0x39: 5,0x40: 2, 0x50: 2, 0x52: 2, 0x54: 1, 0x58: 1,
       0x5a: 1, 0x5b: 1, 0x5c: 1, 0x70: 3, 0x72: 2, 0x73: 2, 0x78: 2, 0x79: 1, 0x80: 4, 0x8f: 0}
CODE_BASE = 6  # instructions start after u16 version + u32 nlocals


def chunks(b):
    assert b[:4] == b'SCRP', b[:4]
    out = {}
    p = 8
    while p + 8 <= len(b):
        tag = b[p:p + 4].decode('latin1')
        sz = struct.unpack_from('<I', b, p + 4)[0]
        out[tag] = (p + 8, sz)
        p += 8 + sz
    return out


def instrs(code):
    """Yield (pos, op, operand bytes) over CODE bytes."""
    p = CODE_BASE
    while p < len(code):
        op = code[p]
        if op not in OPS:
            raise KeyError('op %02x at %x: %s' % (op, p, code[p - 12:p + 12].hex(' ')))
        n = OPS[op]
        if n == 'str':
            n = 2 + struct.unpack_from('<H', code, p + 1)[0]
        elif n == 'sw':
            n = 2 + code[p + 2] * 8
        yield p, op, code[p + 1:p + 1 + n]
        p += 1 + n
    assert p == len(code), (p, len(code))


def targets(op, arg):
    """Code offsets an instruction refers to (jumps)."""
    if op == 0x11:
        return [struct.unpack_from('<I', arg)[0]]
    if op == 0x12:
        return [struct.unpack_from('<I', arg, 1)[0]]
    if op == 0x15:
        return [struct.unpack_from('<I', arg, 2 + 8 * i + 4)[0] for i in range(arg[1])]
    return []


def load_rom_scripts(rom, names=False):
    """Yield (offset, script bytes) for every *.SPC file in MAR.NFP (stored or LZ77-packed); names=True adds the name."""
    import gbalz
    import nfp
    for name, off, size in nfp.entries(rom):
        if not name.endswith('.SPC'):
            continue
        b = gbalz.decompress(rom, off)[0] if rom[off] == 0x10 else rom[off:off + 8 + struct.unpack_from('<I', rom, off + 4)[0]]
        assert b[:4] == b'SCRP', name
        yield (off, b, name) if names else (off, b)


def main(a):
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    rom = open(os.path.join(os.path.dirname(__file__), '..', 'rom',
                            "MAER Heaven - Knockin' on Heaven's Door (Japan).gba"), 'rb').read()
    if a[0] == 'check':
        n = bad = 0
        for off, b in load_rom_scripts(rom):
            c = chunks(b)
            s, sz = c['CODE']
            code = b[s:s + sz]
            try:
                ins = list(instrs(code))
            except (KeyError, AssertionError) as e:
                bad += 1
                print('%07x parse error %r' % (off, e))
                continue
            starts = {p - CODE_BASE for p, _, _ in ins} | {len(code) - CODE_BASE}  # targets are relative to CODE_BASE
            for p, op, arg in ins:
                for t in targets(op, arg):
                    if t not in starts:
                        bad += 1
                        if bad < 10:
                            print('%07x bad target %x at %x op %02x' % (off, t, p, op))
            n += 1
        print(n, 'scripts,', bad, 'bad targets')
        return 1 if bad else 0
    if a[0] == 'dis':
        import gbalz
        b = gbalz.decompress(rom, int(a[1], 16))[0]
        s, sz = chunks(b)['CODE']
        for p, op, arg in instrs(b[s:s + sz]):
            txt = arg[2:-1].decode('cp932', 'replace') if op == 0x10 else ''
            print('%05x %02x %s %s' % (p, op, arg.hex(' ') if op != 0x10 else '', txt))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
