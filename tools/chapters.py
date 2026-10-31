"""Story-pass chapter files: one per `### N. Title (SPC, SPC, EV_RT01-03, ...)` heading of docs/synopsis.md, every
dialogue box of those scripts in file order as `>> id | speaker | JP` / `   EN` (box lines joined with ' / ').

    python -X utf8 tools/chapters.py   -> work/qa/story/chapters/chNN.txt
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'work' / 'qa' / 'story' / 'chapters'


def expand(name):
    """EV_RT01-03 -> EV_RT01, EV_RT02, EV_RT03; anything else as is."""
    m = re.fullmatch(r'(.*?)(\d+)-(\d+)', name)
    if not m:
        return [name]
    pre, a, b = m.groups()
    return ['%s%0*d' % (pre, len(a), k) for k in range(int(a), int(b) + 1)]


def chapters():
    out = []
    for m in re.finditer(r'^### (\d+)\. (.+?) \(([^)]*)\)\s*$', (ROOT / 'docs' / 'synopsis.md').read_text('utf-8'), re.M):
        names = [n for x in m.group(3).split(',') for n in expand(x.strip())]
        out.append((int(m.group(1)), m.group(2), names))
    return out


def boxes(name):
    p = ROOT / 'script' / 'spc' / (name + '.json')
    if not p.exists():
        return None
    bx = {}
    for e in json.loads(p.read_text('utf-8')):
        bx.setdefault(e['box'], []).append(e)
    for v in bx.values():
        lab = [e for e in v if e['line'] == 0 and e['jp'].startswith('{C0D04}［')]
        body = [e for e in v if e not in lab and e['jp']]
        if body:
            spk = lab[0]['en'].strip() if lab else '-'
            yield body[0]['id'], spk, ' / '.join(e['jp'] for e in body), ' / '.join(e['en'].strip() for e in body
                                                                                       if e['en'].strip())


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    missing = []
    for n, title, names in chapters():
        lines = ['# Chapter %d. %s' % (n, title), '']
        for name in names:
            got = list(boxes(name) or [])
            if not got:
                missing.append(name)
                continue
            lines.append('## %s' % name)
            for i, spk, jp, en in got:
                lines += ['>> %s | %s | %s' % (i, spk, jp), '   ' + en]
        (OUT / ('ch%02d.txt' % n)).write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')
        print('ch%02d %-45s %5d lines' % (n, title[:45], len(lines)))
    if missing:
        print('no dialogue / no file:', ' '.join(missing))


if __name__ == '__main__':
    main()
