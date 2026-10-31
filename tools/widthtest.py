"""widthtest.py: build the width-gate / glyph-torture ROM (phase 5; docs/re/vwf.md, script/windows.json).

    python -X utf8 tools/widthtest.py [OUT]   (default build/widthtest.gba)

Marker build plus these OPEN.SPC boxes (reached with the `newgame` warp and A presses):
  box 86: label = longest name tag, lines 1-2 = exactly LIMIT px ending in '|' (shows the last visible column)
  box 88, 90: every printable ASCII character with double spaces (torture lines)
  box 134 line 1: LIMIT + 4 px (must clip or show the overflow)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402
import engine  # noqa: E402

LIMIT = 192


def exact(px, head):
    """head + filler + '|' whose drawn width is exactly px."""
    adv = engine.advance()
    w = lambda s: engine.width(s.encode('ascii'), adv)  # noqa: E731
    s = head
    for ch in ' Mmw iI.' * 60:
        if w(s + ch) + w('|') > px:
            break
        s += ch
    while w(s) + w('|') < px:
        s += '.' if w(s + '.') + w('|') <= px else ''
        if w(s) + w('|') < px and w(s + '.') + w('|') > px:
            s = s[:-1] + ' '  # 3 px instead of 2
    s += '|'
    assert w(s) == px, (w(s), px)
    return s


def tests():
    asc = ''.join(map(chr, range(0x21, 0x7F)))
    return {
        'OPEN:00d83': '{C0D04}[Dorothy-chan]{C0F04}',
        'OPEN:00da7': exact(LIMIT, '%d px ' % LIMIT),
        'OPEN:00db9': exact(LIMIT, '%d px line 2 ' % LIMIT),
        'OPEN:00e21': asc[:32].replace('C', 'C ') + '  x',
        'OPEN:00e3f': asc[32:64] + '  x',
        'OPEN:00ea5': asc[64:] + '  x',
        'OPEN:00ec1': 'The quick brown fox jumps over the lazy dog.',
        'OPEN:015b7': exact(LIMIT + 4, '%d px ' % (LIMIT + 4)),
    }


def record_tests(records):
    """ARM/item names cycle 80-136 px and descriptions 150-200 px, each labelled with its width and ending in '|'
    (byte-limited to the field: max 33)."""
    out = {}
    for n, e in enumerate(records):
        px = (80 + 8 * (n // 2 % 8)) if e['id'].endswith('.name') else (150 + 10 * (n // 2 % 6))
        s = exact(px, '%d ' % px)
        out[e['id']] = s if len(s) <= e['max'] else s[:e['max'] - 1] + '|'
    return out


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else str(build.ROOT / 'build' / 'widthtest.gba')
    build.main([out, '--marker', '--records-test'] + ['--qa=%s=%s' % kv for kv in tests().items()])
