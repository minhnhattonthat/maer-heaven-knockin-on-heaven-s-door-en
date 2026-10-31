"""lint.py: the text lint over script/ (run by tools/check.py; exit 1 on any error).

    python -X utf8 tools/lint.py

Checks every `en`:
- characters: printable ASCII, Ä and ♥ (2-byte glyphs), `{Cxxxx}` colour codes, `{pN}` pads; a run like `C0F04` or
  `t1234` in plain English would be read as a control code (engine.is_code), so it is an error;
- script lines: width <= the dialogue line (script/windows.json 'dialogue', engine.width); per box the colour codes of
  the English equal the Japanese ones in order;
- code strings: width per their window (dlg = engine.width, list/ctr = engine.list_width), byte limits, %s/%d kept;
- records: width (arm_name / arm_desc) and the field's byte limit.
"""
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import build  # noqa: E402
import engine  # noqa: E402
import text  # noqa: E402

SCRIPT = ROOT / 'script'
WIN = json.loads((SCRIPT / 'windows.json').read_text(encoding='utf-8'))
LINE_PX = WIN['dialogue']['px']
ADV = engine.advance()
TOKEN = re.compile(r'\{C[0-9A-F]{4}\}|\{p(?:[1-9]|[12][0-9]|3[01])\}')
CODES = re.compile(r'C[0-9A-F]{4}|%[sd]')  # braced or (6 Japanese strings) bare colour codes
OK_CHARS = re.compile(r'[\x20-\x7e]|Ä|♥')


def char_errors(en):
    """Problems with the characters of one English string (tokens removed first)."""
    errs = []
    plain = TOKEN.sub('\0', en)
    bad = {c for c in plain if c != '\0' and not OK_CHARS.fullmatch(c)}
    if bad:
        errs.append('bad characters %s' % ''.join(sorted(bad)))
    if '{' in plain or '}' in plain:
        errs.append('stray { or } (only {Cxxxx} and {pN} are codes)')
    # codes are written bare ({C0F04} -> C0F04), so "Ice{C0F04}" reads "ceC0F" as a code: check across the joins
    b, real = b'', set()
    for k, part in enumerate(re.split(r'(\{C[0-9A-F]{4}\})', re.sub(r'\{p\d+\}', ' ', en))):
        if k % 2:
            real.add(len(b))
            part = part[1:-1]
        b += part.encode('ascii', 'replace')
    i = 0
    while i < len(b):
        if engine.is_code(b, i):
            if i not in real:
                errs.append('text reads as a control code ([CcTt] + 4 hex digits) at %r' % b[i:i + 5].decode())
                break
            i += 5
        else:
            i += 1
    if re.search(r'%[sd](?:st|nd|rd|th)\b', en):
        errs.append('suffix glued to a placeholder (rephrase: "No. %d")')
    if re.search(r'\b(?:a|an) %s', en, re.I):
        errs.append('a/an right before %s')
    return errs


def width(en):
    return engine.width(text.encode_en(en), ADV)


def list_width(en):
    return engine.list_width(text.encode_en(en), 0, ADV)


def codes(s):
    return CODES.findall(s)


def wrap(en, lines, px=LINE_PX, widow=True):
    """English box text -> its lines. ' / ' forces a break; otherwise greedy word wrap at px, then a one-word last
    line takes the previous line's last word when that line keeps 2+ words and it fits. Returns (lines, error)."""
    if ' / ' in en:
        out = en.split(' / ')
    else:
        out, cur = [], ''
        for w in en.split(' '):
            t = cur + ' ' + w if cur else w
            if cur and width(t) > px:
                out.append(cur)
                cur = w
            else:
                cur = t
        out.append(cur)
        if widow and len(out) > 1 and ' ' not in out[-1]:
            head, _, last = out[-2].rpartition(' ')
            if head.count(' ') >= 1 and width(last + ' ' + out[-1]) <= px:
                out[-2:] = [head, last + ' ' + out[-1]]
    err = None
    if len(out) > lines:
        err = '%d lines > %d' % (len(out), lines)
    for ln in out:
        if width(ln) > px:
            err = (err + '; ' if err else '') + 'line %d px > %d: %r' % (width(ln), px, ln)
    return out, err


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def boxes():
    """OrderedDict {(SPC stem, box): [entries]} over every script file."""
    out = OrderedDict()
    for p in sorted((SCRIPT / 'spc').glob('*.json')):
        for e in load(p):
            out.setdefault((p.stem, e['box']), []).append(e)
    return out


def is_label(e):
    return e['line'] == 0 and e['jp'].startswith('{C0D04}［')


def code_errors(e, en, win):
    """Errors for one code string's English against its window spec."""
    errs = char_errors(en)
    if codes(en) != codes(e['jp']):
        errs.append('codes %s != jp %s' % (codes(en), codes(e['jp'])))
    if win.get('keep'):
        return errs
    w = width(en) if win.get('renderer') == 'dlg' else list_width(en)
    if 'px' in win and w > win['px']:
        errs.append('%d px > %d (%s)' % (w, win['px'], win['name']))
    lim = win.get('bytes')
    if isinstance(lim, dict):
        lim = lim.get(e['id'], lim.get('_other'))
    if lim:
        n = len(text.encode_en(en)) + (-(-(win.get('pad_to', 0) - list_width(en)) // 31) if win.get('pad_to') else 0)
        if n > lim:
            errs.append('%d bytes > %d' % (n, lim))
    return errs


def record_errors(e, en):
    errs = char_errors(en)
    px = WIN['arm_name' if e['id'].endswith('.name') else 'arm_desc']['px']
    if list_width(en) > px:
        errs.append('%d px > %d' % (list_width(en), px))
    if len(text.encode_en(en)) > e['max']:
        errs.append('%d bytes > %d' % (len(text.encode_en(en)), e['max']))
    return errs


def lint():
    errs = []
    for (spc, box), v in boxes().items():
        done = [e for e in v if e.get('en')]
        if not done:
            continue
        for e in done:
            errs += ['%s: %s' % (e['id'], x) for x in char_errors(e['en'])]
            if width(e['en']) > LINE_PX:
                errs.append('%s: %d px > %d' % (e['id'], width(e['en']), LINE_PX))
        if all(e.get('en') or not e['jp'] for e in v):
            jc, ec = sum((codes(e['jp']) for e in v), []), sum((codes(e['en']) for e in v), [])
            if jc != ec:
                errs.append('%s:%d box: codes %s != jp %s' % (spc, box, ec, jc))
    # Japanese left untranslated: only the debug chapter select, `keep` windows and blank (fullwidth-space) fields
    keep_spc = {s[:-4] for s in build.KEEP_SCRIPTS}
    wins = build.code_windows()
    errs += ['%s: jp without en' % e['id'] for p in sorted((SCRIPT / 'spc').glob('*.json')) if p.stem not in keep_spc
             for e in load(p) if e['jp'].strip('　') and not e.get('en')]
    errs += ['%s: jp without en' % e['id'] for e in load(SCRIPT / 'code.json')
             if not e.get('en') and not wins.get(e['id'], {}).get('keep')]
    errs += ['%s: jp without en' % e['id'] for e in load(SCRIPT / 'records.json')
             if e['jp'].strip('　') and not e.get('en')]
    for e in load(SCRIPT / 'code.json'):
        if e.get('en'):
            errs += ['%s: %s' % (e['id'], x) for x in code_errors(e, e['en'], wins.get(e['id'], {'name': '?'}))]
    for e in load(SCRIPT / 'records.json'):
        if e.get('en'):
            errs += ['%s: %s' % (e['id'], x) for x in record_errors(e, e['en'])]
    return errs


def main():
    errs = lint()
    for x in errs:
        print(x)
    print('lint: %d errors' % len(errs) if errs else 'lint: OK')
    return 1 if errs else 0


if __name__ == '__main__':
    sys.exit(main())
