"""Text codec for the game's Shift-JIS strings (docs/re/text.md).

decode(bytes) -> str and encode(str) -> bytes are exact inverses on every string in the ROM (tests/test_extract.py):
- Shift-JIS (cp932), NUL not included;
- the font's user-defined glyphs: F0 40 -> '♥', F0 56 -> 'Ä' (the Ä of MÄR); any other F0xx-F9xx -> '{Fxxx}';
- colour codes as stored ' C0F04 ' (space, C, 4 hex digits, space) -> '{C0F04}'. The 6 codes stored with other
  spacing stay literal ASCII, so they roundtrip too.
"""
import re

GLYPHS = {'': '♥', '': 'Ä'}  # cp932 maps F040.. to U+E000..
UNGLYPHS = {v: k for k, v in GLYPHS.items()}
CODE = re.compile(r' C([0-9A-F]{4}) ')
TOKEN = re.compile(r'\{(C[0-9A-F]{4}|F[0-9A-F]{3})\}')


def decode(b):
    s = ''.join(GLYPHS.get(c) or ('{%s}' % _pua(c) if '' <= c <= '' else c) for c in b.decode('cp932'))
    return CODE.sub(lambda m: '{C%s}' % m.group(1), s)


def _pua(c):
    """cp932 user-defined char -> its two Shift-JIS bytes as 'Fxxx'."""
    return c.encode('cp932').hex().upper()


def encode_en(s):
    """English text -> bytes for the patched engine (tools/engine.py): ASCII is single-byte, colour codes are
    written without the surrounding spaces (`{C0F04}` -> `C0F04`), `{p5}` is a pad byte (blank, 5 px in list
    windows and centred labels; 1-31), anything else goes through encode()."""
    return b''.join(m.group(1).encode('ascii') if m.group(1) else bytes([int(m.group(2))]) if m.group(2)
                    else encode(m.group(3))
                    for m in re.finditer(r'\{(C[0-9A-F]{4})\}|\{p([1-9]|[12][0-9]|3[01])\}|(\{F[0-9A-F]{3}\}|[^{]+|\{)', s))


def encode(s):
    out = []
    pos = 0
    for m in TOKEN.finditer(s):
        out.append(s[pos:m.start()])
        t = m.group(1)
        out.append(' %s ' % t if t[0] == 'C' else bytes.fromhex(t).decode('cp932'))
        pos = m.end()
    out.append(s[pos:])
    return ''.join(UNGLYPHS.get(c, c) for c in ''.join(out)).encode('cp932')
