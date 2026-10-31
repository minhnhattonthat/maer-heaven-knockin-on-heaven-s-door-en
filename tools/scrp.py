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
    """{tag: (data start, data size)}. The file ends with a bare 'TERM'; NVAR's size counts its 8-byte header."""
    assert b[:4] == b'SCRP', b[:4]
    out = {}
    p = 8
    while b[p:p + 4] != b'TERM':
        tag = b[p:p + 4].decode('latin1')
        sz = struct.unpack_from('<I', b, p + 4)[0] - (8 if tag == 'NVAR' else 0)
        out[tag] = (p + 8, sz)
        p += 8 + sz
    assert p + 4 == len(b), 'bytes after TERM'
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


def natives(func):
    """FUNC chunk -> {CODE offset of a 0x80 operand: native name}."""
    out, p = {}, 0
    while p < len(func):
        e = func.index(b'\0', p)
        name = func[p:e].decode('latin1')
        p = e + 1
        while p + 4 <= len(func):  # the last list has no 0 terminator
            o = struct.unpack_from('<I', func, p)[0]
            p += 4
            if not o:
                break
            out[o] = name
    return out


def rebuild(b, strings=None):
    """Script bytes with some 0x10 strings replaced: {CODE pos of the 0x10 op: new bytes without NUL}.
    Shifts code and rewrites every jump/switch target, every 0x22 string address and every FUNC fixup.
    With no strings the output equals the input (identity test). Not touched: 0x29 pushes (docs/re/script.md)."""
    strings = strings or {}
    c = chunks(b)
    s, sz = c['CODE']
    code = b[s:s + sz]
    ins = list(instrs(code))
    # The VM copies CODE into a heap block of (size - 6) + stack and writes the stack top word-aligned: a size not
    # 2 mod 4 (as all 334 originals are) overwrites the next heap header and crashes (docs/re/vwf.md). Keep the
    # total length change a multiple of 4 by NUL-padding the last changed string inside its own length.
    grow = sum(len(t) - (len(code_arg[2:]) - 1) for p, op, code_arg in ins if p in strings for t in [strings[p]])
    last = max(strings) if strings else None
    new = bytearray(code[:CODE_BASE])
    pos = {}  # old pos -> new pos, for every instruction start and the end
    for p, op, arg in ins:
        pos[p] = len(new)
        if p in strings:
            t = strings[p] + b'\0' + (b'\0' * (-grow % 4) if p == last else b'')
            arg = struct.pack('<H', len(t)) + t
        new += bytes([op]) + arg
    pos[len(code)] = len(new)

    def reloc(o):  # operand offsets are relative to CODE_BASE
        return pos[o + CODE_BASE] - CODE_BASE

    prev = None
    for p, op, arg in ins:
        q = pos[p] + 1  # operand start in new
        if op == 0x11:
            struct.pack_into('<I', new, q, reloc(struct.unpack_from('<I', arg)[0]))
        elif op == 0x12:
            struct.pack_into('<I', new, q + 1, reloc(struct.unpack_from('<I', arg, 1)[0]))
        elif op == 0x15:
            for i in range(arg[1]):
                struct.pack_into('<I', new, q + 2 + 8 * i + 4, reloc(struct.unpack_from('<I', arg, 2 + 8 * i + 4)[0]))
        elif op == 0x22:
            assert prev[1] == 0x10 and struct.unpack_from('<I', arg, 1)[0] == prev[0] + 3 - CODE_BASE, p
            struct.pack_into('<I', new, q + 1, pos[prev[0]] + 3 - CODE_BASE)
        prev = (p, op)
    out = bytearray()
    for tag, (p, n) in c.items():
        data = b[p:p + n]
        if tag == 'CODE':
            data = new
        elif tag == 'FUNC':
            data = _reloc_func(data, lambda o: pos[o - 1 + CODE_BASE] + 1 - CODE_BASE)
        out += tag.encode('latin1') + struct.pack('<I', len(data) + (8 if tag == 'NVAR' else 0)) + data
    out += b'TERM'
    assert (len(new) - len(code)) % 4 == 0
    return b'SCRP' + struct.pack('<I', len(out)) + bytes(out)


def _reloc_func(func, f):
    """FUNC chunk with every fixup offset o replaced by f(o); same walk as natives()."""
    out, p = bytearray(func), 0
    while p < len(func):
        e = func.index(b'\0', p)
        p = e + 1
        while p + 4 <= len(func):
            o = struct.unpack_from('<I', func, p)[0]
            if o:
                struct.pack_into('<I', out, p, f(o))
            p += 4
            if not o:
                break
    return bytes(out)


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
        if a[1].upper().endswith('.SPC'):
            b = next(x for _, x, n in load_rom_scripts(rom, True) if n == a[1].upper())
        else:
            import gbalz
            b = gbalz.decompress(rom, int(a[1], 16))[0]
        c = chunks(b)
        s, sz = c['CODE']
        nat = natives(b[c['FUNC'][0]:c['FUNC'][0] + c['FUNC'][1]]) if 'FUNC' in c else {}
        for p, op, arg in instrs(b[s:s + sz]):
            txt = arg[2:-1].decode('cp932', 'replace') if op == 0x10 else nat.get(p + 1 - CODE_BASE, '')
            print('%05x %02x %s %s' % (p - CODE_BASE, op, arg.hex(' ') if op != 0x10 else '', txt))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
