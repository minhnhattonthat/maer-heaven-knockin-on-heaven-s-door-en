"""engine.py: English text engine patch (docs/re/vwf.md).

- Font: single-byte codes 0x20-0x7E already map to FONT.NFT glyphs 0x200-0x25E (lookup 0x0807AE10: byte + 0x1E0,
  Greek/Cyrillic slots this game never uses); `font()` overwrites them with fonts/vwf8.txt.
- Dialogue (MswStr window, 0x08011870): hooks make single-byte ASCII printable (the old code skipped it), keep
  ` C0F04 `-style codes only when C/c/T/t is followed by 4 hex digits, and advance x by the glyph's pixel width.

`patches()` -> [(rom offset, original bytes, new bytes)]; `apply()` asserts the originals before writing.
"""
import re
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
            if b[i - 5] in b'Tt' and b[i - 4:i].isdigit() and b[i:i + 1] == b' ':  # 'T0000 ': fetch skips the space
                i += 1
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
    for c, (rows, _) in list(glyphs().items()) + [(c, (bytes(8), 0)) for c in range(1, 0x20)]:  # 0x01-0x1F: pads
        o = 0x60 + (GLYPH0 + c) * 8
        out[o:o + 8] = rows
    return bytes(out)


def list_width(b, spacing=0, adv=None):
    """Pixel width as the list/centred-label hooks measure it (`measure`): ASCII its advance (no window spacing:
    the advance already holds the shadow gap), 2-byte glyphs 8 + spacing, other single bytes >= 0x7F 8 + spacing,
    pad bytes 0x01-0x1F their own value in px (blank glyphs; text.encode_en `{p5}`), no codes."""
    adv, i, w = adv or advance(), 0, 0
    while i < len(b) and b[i]:
        c = b[i]
        if 0x81 <= c <= 0x9F or 0xE0 <= c:
            w, i = w + 8 + spacing, i + 2
        elif c < 0x20:
            w, i = w + c, i + 1
        elif c < 0x7F:
            w, i = w + adv[c - 0x20], i + 1
        else:
            w, i = w + 8 + spacing, i + 1
    return w


def pxlen(b, adv=None):
    """What the `pxlen` hook hands the game's byte-count layout code instead of strlen: an even length whose
    len / 2 * 8 is the pixel width rounded up to 8 (Japanese strings: their byte length)."""
    return (list_width(b, 0, adv) + 7) // 8 * 2


def asm(src, addr):
    """Thumb source -> bytes. Fails on any 32-bit Thumb-2 encoding except BL (the GBA's ARM7TDMI has none):
    keystone silently picks e.g. `subs.w` for a 3-operand subtract with a large immediate."""
    b = bytes(Ks(KS_ARCH_ARM, KS_MODE_THUMB).asm(src, addr)[0])
    code = len(b) - 4 * src.count('.word')
    for i in Cs(CS_ARCH_ARM, CS_MODE_THUMB).disasm(b[:code], addr):
        assert i.size == 2 or i.mnemonic == 'bl', ('Thumb-2 instruction', hex(i.address), i.mnemonic, i.op_str)
        if i.mnemonic == 'bl':  # ARMv4T BL pair: F000 | hi, F800 | lo (+-4 MiB)
            assert i.bytes[1] & 0xF8 == 0xF0 and i.bytes[3] & 0xF8 == 0xF8, ('BL out of ARMv4T range', hex(i.address))
    return b


def far(target, reg='r0'):
    """Jump from game code to a hook: ldr reg,[pc]; bx reg; literal (Thumb BL reaches only +-4 MiB)."""
    return 'ldr %s, farlit\nbx %s\n.align 2\nfarlit: .word 0x%X\n' % (reg, reg, target | 1)


# Hooks (Thumb, in free space); each returns to game code with ldr/bx.
HOOKS = {
    # from 0x08011B2E (dialogue fetch, single-byte path): r4 -> char, r6 window, r7 -> line index byte.
    # A space right after T/t + 4 decimal digits ('T0000 ' timing code + separator) is skipped like a code (the
    # original skipped every single byte; menu-help / shop lines start 'T0000 C0F04'; T0000 is the only T code).
    'fetch': """
    ldrb r5, [r4]
    cmp r5, #0x20
    blo f_ctrl
    bne f_chk
    subs r3, r4, #5
    ldrb r0, [r3]
    movs r2, #0x20
    orrs r0, r2
    cmp r0, #0x74
    bne f_print
    movs r1, #1
f_sp:
    ldrb r0, [r3, r1]
    subs r0, #0x30
    cmp r0, #9
    bhi f_print
    adds r1, #1
    cmp r1, #5
    blo f_sp
    b f_ctrl
f_chk:
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

# Shared helpers for the list and centred-label hooks; `{measure}` etc. are filled with entry addresses.
HOOKS['measure'] = """
    push {r4, r5, r6, lr}
    adds r4, r0, r1
    movs r5, #0
    ldr r6, m_widths
m_loop:
    cmp r0, r4
    bhs m_done
    ldrb r3, [r0]
    cmp r3, #0
    beq m_done
    adds r0, #1
    cmp r3, #0x81
    blo m_one
    cmp r3, #0x9f
    bls m_two
    cmp r3, #0xe0
    blo m_one
m_two:
    adds r0, #1
    adds r5, #8
    b m_next
m_one:
    subs r3, #0x20
    blo m_pad
    cmp r3, #0x5e
    bhi m_wide
    ldrb r3, [r6, r3]
    adds r5, r5, r3
    b m_loop
m_pad:
    adds r5, r5, r3
    adds r5, #0x20
    b m_loop
m_wide:
    adds r5, #8
m_next:
    adds r5, r5, r2
    b m_loop
m_done:
    adds r0, r5, #0
    pop {r4, r5, r6}
    pop {r1}
    bx r1
    .align 2
m_widths: .word {widths}
"""
HOOKS['calls'] = """
    bx r3
    bx ip
"""
# list windows 0x080532A4 (obj r5, string i*4 at [sp+0x14]) and 0x080533F0 (obj r4, x from [sb]): x = base +
# measured pixel width of the bytes before index r8; step r8 by the character's byte length.
_LIST_X = """
    ldr r0, [{obj}]
    ldr r1, [sp, #0x14]
    ldr r0, [r0, r1]
    mov r1, r8
    movs r3, #0x12
    ldrsh r2, [{obj}, r3]
    bl {measure}
    {base}
    adds r6, r0, r1
    ldr r0, x_back
    bx r0
    .align 2
x_back: .word {back}
"""
HOOKS['list1_x'] = _LIST_X.replace('{obj}', 'r5').replace('{base}', 'movs r3, #0x1c\n    ldrsh r1, [r5, r3]').replace('{back}', '0x08053323')
HOOKS['list2_x'] = _LIST_X.replace('{obj}', 'r4').replace('{base}', 'mov r2, sb\n    movs r3, #0\n    ldrsh r1, [r2, r3]').replace('{back}', '0x08053473')
_LIST_STEP = """
    ldr r0, [{obj}]
    ldr r1, [sp, #0x14]
    ldr r0, [r0, r1]
    mov r1, r8
    ldrb r0, [r0, r1]
    movs r2, #1
    cmp r0, #0x81
    blo s_one
    cmp r0, #0x9f
    bls s_two
    cmp r0, #0xe0
    blo s_one
s_two:
    movs r2, #2
s_one:
    adds r1, r1, r2
    mov r8, r1
    ldr r0, s_back
    bx r0
    .align 2
s_back: .word {back}
"""
HOOKS['list1_step'] = _LIST_STEP.replace('{obj}', 'r5').replace('{back}', '0x080533A1')
HOOKS['list2_step'] = _LIST_STEP.replace('{obj}', 'r4').replace('{back}', '0x080534E5')
# centred label 0x0801E168(str, centre x, y), drawn ink 0xF at VRAM 0x06008000, 32 tiles per row (no shadow)
HOOKS['center'] = """
    push {r4, r5, r6, r7, lr}
    sub sp, #0xc
    adds r5, r0, #0
    adds r4, r1, #0
    adds r7, r2, #0
    movs r1, #0
c_len:
    ldrb r2, [r0, r1]
    cmp r2, #0
    beq c_m
    adds r1, #1
    b c_len
c_m:
    movs r2, #0
    bl {measure}
    lsrs r0, r0, #1
    subs r4, r4, r0
c_loop:
    ldrb r1, [r5]
    cmp r1, #0
    beq c_done
    movs r6, #1
    cmp r1, #0x81
    blo c_one
    cmp r1, #0x9f
    bls c_two
    cmp r1, #0xe0
    blo c_one
c_two:
    lsls r1, r1, #8
    ldrb r0, [r5, #1]
    orrs r1, r0
    movs r6, #2
c_one:
    ldr r0, c_font
    ldr r3, c_glyph
    bl {calls}
    adds r1, r0, #0
    movs r0, #0xf
    str r0, [sp]
    movs r0, #0
    str r0, [sp, #4]
    movs r0, #0x20
    str r0, [sp, #8]
    ldr r0, c_blit
    mov ip, r0
    ldr r0, c_vram
    adds r2, r4, #0
    adds r3, r7, #0
    bl {calls_ip}
    adds r0, r5, #0
    adds r1, r6, #0
    movs r2, #0
    bl {measure}
    adds r4, r4, r0
    adds r5, r5, r6
    b c_loop
c_done:
    add sp, #0xc
    pop {r4, r5, r6, r7}
    pop {r0}
    bx r0
    .align 2
c_font: .word 0x030032E4
c_glyph: .word 0x0807AE11
c_blit: .word 0x08011689
c_vram: .word 0x06008000
"""
# strlen stand-in for the game's byte-count layout code (centring / right-aligning as len / 2 * 8 px): returns an
# even length whose len / 2 * 8 is the measured pixel width rounded up to 8 (engine.pxlen). Reached by BL through
# the veneer at 0x0801B988, so lr is the game's return address.
HOOKS['pxlen'] = """
    push {lr}
    movs r1, #1
    lsls r1, r1, #12
    movs r2, #0
    bl {measure}
    adds r0, #7
    lsrs r0, r0, #3
    lsls r0, r0, #1
    pop {r1}
    bx r1
"""
PXLEN_VENEER = 0x0801B988  # dead code after the 0x01B97C rewrite (it branches over 0x01B988-0x01B9C5)
# bl strlen -> bl veneer: name tabs (right-aligned in 7 cells, 0x08053C48 / 0x08053D9C), 104-px centred names,
# 128-px centred area names (world map)
PXLEN_SITES = {0x053C2C: '2ef042fe', 0x053D7E: '2ef099fd', 0x05AF04: '27f0d6fc', 0x05B108: '27f0d4fb',
               0x0641A0: '1ef088fb', 0x0643AA: '1ef083fa', 0x06BBC2: '16f077fe', 0x06BE1E: '16f049fd',
               0x06D7CA: '15f073f8', 0x06D810: '15f050f8'}

# (rom offset, original bytes, replacement: asm source or ('far', hook name[, register]))
SITES = [
    # list windows: x calc -> list*_x, byte step -> list*_step
    (0x05330C, '1223e95e08314246d00f4044401041431c23e85e0e18', ('far', 'list1_x')),
    (0x053396, '40460230000400148046', ('far', 'list1_step')),
    (0x05345A, '1222a15e08314346d80f4044401041434a460023d05e0e18', ('far', 'list2_x')),
    (0x0534DA, '40460230000400148046', ('far', 'list2_step')),
    # centred label function -> center (r3 is free at entry; args r0-r2)
    (0x01E168, 'f0b583b0051c0c1c', ('far', 'center', 'r3')),
    # 0x0801B95C draws its fixed string the same way: call 0x0801E168(stack copy, r4, r7) and return
    (0x01B97C, '03a866f099ff41088800221a03ae00291bd0141c0d1c301ce6f712fe011c0904090c0d485ff036fa011c0f20009000'
               '200190202002900948221c3b1cf5f766fe02360834013d002de5d1',
     'add r0, sp, #0xc\nadds r1, r4, #0\nadds r2, r7, #0\nbl 0x0801E168\nb 0x0801B9C6\n'),
    # fetch: `adds r0,r4,#0; bl 0x080025BC; lsls r0,#16` -> jump to the hook (resumes at the cmp chain 0x08011B38)
    (0x011B2E, '201cf0f744fd0004050c', ('far', 'fetch')),
    # draw x = the line's pixel x byte (was (col / 2) * 9)
    (0x011936, '414600200856c10f40184010c5002d18', 'mov r1, r8\nldrb r5, [r1]\nb 0x08011946\n'),
    # after drawing: x += glyph width, index += 1 or 2 (resumes 0x080119A2)
    (0x011990, '42461078023010701a483918087802300870', ('far', 'adv')),
    (PXLEN_VENEER - 0x08000000, '03ae00291bd0141c', ('far', 'pxlen', 'r3')),
] + [(off, orig, 'bl 0x%X' % PXLEN_VENEER) for off, orig in PXLEN_SITES.items()]

# ASCII sprintf formats of the string block that open menu-help / shop / item lines: the original fetch skipped
# their separator spaces, ours draws them (3 px each), so drop the space after the colour code (in place,
# NUL-padded; the one after T0000 must stay). Spaces between fields (`%md %s`) stay: English wants them.
FORMATS = {0x87868: b'T0000 C0905 %s', 0x87878: b'T0000 C0F04 %s', 0x88450: b'T0000 C0F04 %s',
           0x88814: b'T0000 C0F04 %md %s', 0x88828: b'T0000 C0F04 %s', 0x88838: b'T0000 C0F04 %s%s',
           0x8896C: b'T0000 C0F04', 0x88B5C: b'T0000 C0F04', 0x88BB0: b'T0000 C0F04 %s',
           0x88BC0: b'T0000 C0F04 %s  %md  %s', 0x88D30: b'T0000 C0F04', 0x88D8C: b'T0000 C0F04 %s',
           0x88E38: b'T0000 C0F04 %s', 0x88E5C: b'T0000 C0F04 %s', 0x89180: b'T0000 C0F04 %s %s',
           0x89194: b'T0000 C0F04 %s', 0x89408: b'T0000 C0F04 %s'}


def format_patches():
    out = []
    for off, s in FORMATS.items():
        new = re.sub(rb'^(T0000 C[0-9A-F]{4}) ', rb'\1', s)  # 'T0000C0F04' (no space) blanked the line
        out.append((off, s + b'\0', new.ljust(len(s) + 1, b'\0')))
    return out


def patches():
    """[(rom offset, original bytes, new bytes)] for the engine."""
    adv = advance()
    out = [(FREE, b'\xff' * len(adv), adv)]
    at, entry = FREE + ((len(adv) + 3) & ~3), {}
    for name, src in HOOKS.items():
        fill = dict(widths='0x%X' % (0x08000000 + FREE), wide=WIDE_ADV)
        if 'measure' in entry:
            fill.update(measure='0x%X' % entry['measure'])
        if 'calls' in entry:
            fill.update(calls='0x%X' % entry['calls'], calls_ip='0x%X' % (entry['calls'] + 2))
        for k, v in fill.items():  # not str.format: register lists use braces
            src = src.replace('{%s}' % k, str(v))
        code = asm(src, 0x08000000 + at)
        out.append((at, b'\xff' * len(code), code))
        entry[name] = 0x08000000 + at
        at = (at + len(code) + 3) & ~3
    assert at <= FREE_END
    for off, orig, src in SITES:
        orig = bytes.fromhex(orig)
        if isinstance(src, tuple):
            src = far(entry[src[1]], *src[2:])
        new = asm(src, 0x08000000 + off)
        assert len(new) <= len(orig), (hex(off), len(new), len(orig))
        out.append((off, orig[:len(new)], new))
    return out + format_patches()


def apply(rom):
    """Write every patch into a bytearray ROM, asserting the original bytes."""
    for off, orig, new in patches():
        assert rom[off:off + len(orig)] == orig, ('unexpected bytes at %X' % off, rom[off:off + len(orig)].hex(), orig.hex())
        rom[off:off + len(new)] = new
    return rom
