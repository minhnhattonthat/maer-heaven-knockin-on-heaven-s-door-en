"""engine.py: English text engine patch (docs/re/vwf.md).

- Font: single-byte codes 0x20-0x7E already map to FONT.NFT glyphs 0x200-0x25E (lookup 0x0807AE10: byte + 0x1E0,
  Greek/Cyrillic slots this game never uses); `font()` overwrites them with fonts/vwf8.txt.
- Dialogue (MswStr window, 0x08011870): hooks make single-byte ASCII printable (the old code skipped it), keep
  ` C0F04 `-style codes only when C/c/T/t is followed by 4 hex digits, and advance x by the glyph's pixel width.

`patches()` -> [(rom offset, original bytes, new bytes)]; `apply()` asserts the originals before writing.
"""
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
from keystone import Ks, KS_ARCH_ARM, KS_MODE_THUMB

ROOT = Path(__file__).resolve().parents[1]
FREE = 0xFE4000            # 0xFF fill 0xFE4000-0xFFF000 (docs/re/nfp.md); archive spill stops at 0xFE0000
FREE_END = 0xFFF000
GLYPH0 = 0x1E0             # glyph index of single-byte code 0
WIDE_ADV = 9               # 2-byte glyphs keep the original 9 px (8 + shadow)
HEX = b'0123456789ABCDEFabcdef'


def glyphs(path=ROOT / 'fonts' / 'vwf8.txt'):
    """{code: (8 row bytes, width)} from the ASCII-art font file."""
    out, name, rows = {}, None, []
    for line in path.read_text(encoding='utf-8').splitlines() + ['== end']:
        if line.startswith('# '):  # comment (glyph rows have no spaces)
            continue
        if line.startswith('== '):
            if name is not None:
                assert len(rows) == 8 and len({len(r) for r in rows}) == 1, name
                w = len(rows[0])
                assert 1 <= w <= 8, name
                bits = [int(r.replace('#', '1').replace('.', '0').ljust(8, '0'), 2) for r in rows]
                out[0x20 if name == 'space' else ord(name)] = (bytes(bits), w)
            name, rows = line[3:], []
        elif line:
            rows.append(line)
    assert sorted(out) == list(range(0x20, 0x7F)), 'font must cover 0x20-0x7E'
    return out


def advance():
    """bytes 0x20-0x7E -> pixel advance (glyph width + 1 for the shadow)."""
    g = glyphs()
    return bytes(g[c][1] + 1 for c in range(0x20, 0x7F))


def is_code(b, i):
    """The dialogue reads C/c/T/t + 4 hex digits as a control code (colour / timing)."""
    return b[i] in b'CcTt' and i + 5 <= len(b) and all(x in HEX for x in b[i + 1:i + 5])


def width(b, adv=None):
    """Pixel width of an encoded string as the dialogue hook draws it (single bytes VWF, 2-byte glyphs 9 px)."""
    adv, i, w = adv or advance(), 0, 0
    while i < len(b):
        c = b[i]
        if is_code(b, i):
            i += 5
        elif 0x81 <= c <= 0x9F or 0xE0 <= c:
            w, i = w + WIDE_ADV, i + 2
        elif 0x20 <= c < 0x7F:
            w, i = w + adv[c - 0x20], i + 1
        else:
            w, i = w + (WIDE_ADV if c >= 0x7F else 0), i + 1
    return w


def font(nft):
    """FONT.NFT with the English glyphs in the single-byte slots."""
    assert nft[:3] == b'NFT' and nft[0x20] == 8 and nft[0x24] == 8 and nft[0x38] == 8
    out = bytearray(nft)
    for c, (rows, _) in glyphs().items():
        o = 0x60 + (GLYPH0 + c) * 8
        out[o:o + 8] = rows
    return bytes(out)


def asm(src, addr):
    """Thumb source -> bytes. Fails on any 32-bit Thumb-2 encoding except BL (the GBA's ARM7TDMI has none):
    keystone silently picks e.g. `subs.w` for a 3-operand subtract with a large immediate."""
    b = bytes(Ks(KS_ARCH_ARM, KS_MODE_THUMB).asm(src, addr)[0])
    code = len(b) - 4 * src.count('.word')
    for i in Cs(CS_ARCH_ARM, CS_MODE_THUMB).disasm(b[:code], addr):
        assert i.size == 2 or i.mnemonic == 'bl', ('Thumb-2 instruction', hex(i.address), i.mnemonic, i.op_str)
    return b


def far(target, reg='r0'):
    """Jump from game code to a hook: ldr reg,[pc]; bx reg; literal (Thumb BL reaches only +-4 MiB)."""
    return 'ldr %s, farlit\nbx %s\n.align 2\nfarlit: .word 0x%X\n' % (reg, reg, target | 1)


# Hooks (Thumb, in free space); each returns to game code with ldr/bx.
HOOKS = {
    # from 0x08011B2E (dialogue fetch, single-byte path): r4 -> char, r6 window, r7 -> line index byte
    'fetch': """
    ldrb r5, [r4]
    cmp r5, #0x20
    blo f_ctrl
    cmp r5, #0x43
    beq f_code
    cmp r5, #0x63
    beq f_code
    cmp r5, #0x54
    beq f_code
    cmp r5, #0x74
    bne f_print
f_code:
    movs r1, #1
f_hex:
    ldrb r0, [r4, r1]
    movs r2, r0
    subs r2, #0x30
    cmp r2, #9
    bls f_ok
    movs r2, r0
    subs r2, #0x41
    cmp r2, #5
    bls f_ok
    movs r2, r0
    subs r2, #0x61
    cmp r2, #5
    bhi f_print
f_ok:
    adds r1, #1
    cmp r1, #5
    blo f_hex
f_ctrl:
    ldr r0, f_dispatch
    bx r0
f_print:
    ldr r0, f_char
    bx r0
    .align 2
f_dispatch: .word 0x08011B39
f_char: .word 0x08011C05
""",
    # from 0x08011990 (dialogue, after both draws): sb -> char code, r8 -> x byte, r7 window
    'adv': """
    mov r2, sb
    ldrh r0, [r2]
    mov r2, r8
    ldrb r1, [r2]
    movs r3, #2
    cmp r0, #0xff
    bhi a_wide
    movs r3, #1
    subs r0, #0x20
    blo a_wide
    cmp r0, #0x5e
    bhi a_wide
    ldr r2, a_widths
    ldrb r0, [r2, r0]
    adds r1, r1, r0
    b a_store
a_wide:
    adds r1, #{wide}
a_store:
    mov r2, r8
    strb r1, [r2]
    ldr r0, a_off
    adds r1, r7, r0
    ldrb r0, [r1]
    adds r0, r0, r3
    strb r0, [r1]
    ldr r0, a_back
    bx r0
    .align 2
a_widths: .word {widths}
a_off: .word 0x1E3
a_back: .word 0x080119A3
""",
}

# (rom offset, original bytes, replacement: asm source or ('far', hook name))
SITES = [
    # fetch: `adds r0,r4,#0; bl 0x080025BC; lsls r0,#16` -> jump to the hook (resumes at the cmp chain 0x08011B38)
    (0x011B2E, '201cf0f744fd0004050c', ('far', 'fetch')),
    # draw x = the line's pixel x byte (was (col / 2) * 9)
    (0x011936, '414600200856c10f40184010c5002d18', 'mov r1, r8\nldrb r5, [r1]\nb 0x08011946\n'),
    # after drawing: x += glyph width, index += 1 or 2 (resumes 0x080119A2)
    (0x011990, '42461078023010701a483918087802300870', ('far', 'adv')),
]


def patches():
    """[(rom offset, original bytes, new bytes)] for the engine."""
    adv = advance()
    out = [(FREE, b'\xff' * len(adv), adv)]
    at, entry = FREE + ((len(adv) + 3) & ~3), {}
    for name, src in HOOKS.items():
        code = asm(src.format(widths='0x%X' % (0x08000000 + FREE), wide=WIDE_ADV), 0x08000000 + at)
        out.append((at, b'\xff' * len(code), code))
        entry[name] = 0x08000000 + at
        at = (at + len(code) + 3) & ~3
    assert at <= FREE_END
    for off, orig, src in SITES:
        orig = bytes.fromhex(orig)
        if isinstance(src, tuple):
            src = far(entry[src[1]])
        new = asm(src, 0x08000000 + off)
        assert len(new) <= len(orig), (hex(off), len(new), len(orig))
        out.append((off, orig[:len(new)], new))
    return out


def apply(rom):
    """Write every patch into a bytearray ROM, asserting the original bytes."""
    for off, orig, new in patches():
        assert rom[off:off + len(orig)] == orig, ('unexpected bytes at %X' % off, rom[off:off + len(orig)].hex(), orig.hex())
        rom[off:off + len(new)] = new
    return rom
