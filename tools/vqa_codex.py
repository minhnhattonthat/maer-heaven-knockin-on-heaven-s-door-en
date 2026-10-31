"""Independent visual-QA read of one qa_gate chunk by `codex exec` (read-only sandbox, sheets attached as images),
per docs/visual-qa-brief.md. Writes the verdict file qa_gate.py reads.

    python -X utf8 tools/vqa_codex.py work/qa/chunks/chunk_001.txt work/qa/verdicts/chunk_001.tsv [--per 6]

Each call gets up to --per tour sheets and, where it exists, the original ROM's sheet of the same id
(work/qa/tour_jp/...). Ids missing from codex's answer are reported and left without a verdict (qa_gate fails).
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def ask(rows, brief):
    imgs, lines = [], []
    for k, (i, p) in enumerate(rows):
        imgs.append(p)
        lines.append('image %d = id %s (translated build)' % (len(imgs), i))
        jp = os.path.join(REPO, 'work', 'qa', 'tour_jp', *i.split('/')) + '.png'
        if os.path.exists(jp):
            imgs.append(jp)
            lines.append('image %d = id %s ORIGINAL Japanese ROM, same route (reference only)' % (len(imgs), i))
    prompt = (brief + '\n\n## This dispatch\nThe sheets are attached as images, in this order:\n' + '\n'.join(lines) +
              '\n\nGive one verdict per translated-build id. Answer with ONLY lines of the form\n'
              'id<TAB>ok<TAB>note   or   id<TAB>issue<TAB>which tile, which text, what is wrong\n'
              'No other text. Do not modify any file.')
    with tempfile.TemporaryDirectory() as t:
        out = os.path.join(t, 'last.txt')
        cmd = ['codex', 'exec', '--sandbox', 'read-only', '--skip-git-repo-check', '--ephemeral', '-C', REPO,
               '-o', out]
        for p in imgs:
            cmd += ['-i', p]
        cmd += ['--', prompt]
        subprocess.run(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       timeout=1800)
        return open(out, encoding='utf8').read() if os.path.exists(out) else ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('chunk')
    ap.add_argument('verdicts')
    ap.add_argument('--per', type=int, default=6)
    a = ap.parse_args()
    tour = os.path.join(REPO, 'work', 'qa', 'tour')
    rows = []
    for ln in open(a.chunk, encoding='utf8').read().splitlines():
        p = ln.split('\t')[-1].strip()  # chunk lines are paths; id = path under the tour dir, no extension
        if p:
            p = os.path.normpath(p if os.path.isabs(p) else os.path.join(REPO, p))
            rows.append((os.path.splitext(os.path.relpath(p, tour))[0].replace(os.sep, '/'), p))
    brief = open(os.path.join(REPO, 'docs', 'visual-qa-brief.md'), encoding='utf8').read()
    got = {}
    for k in range(0, len(rows), a.per):
        part = rows[k:k + a.per]
        ids = {i for i, _ in part}
        for ln in ask(part, brief).splitlines():
            m = re.match(r'\s*(\S+)\t(ok|issue)\t?(.*)', ln)
            if m and m.group(1) in ids:
                got[m.group(1)] = (m.group(2), m.group(3).strip())
    os.makedirs(os.path.dirname(os.path.abspath(a.verdicts)), exist_ok=True)
    with open(a.verdicts, 'w', encoding='utf8') as f:
        for i, _ in rows:
            if i in got:
                f.write('%s\t%s\t%s\n' % (i, *got[i]))
    missing = [i for i, _ in rows if i not in got]
    issues = [(i, n) for i, (v, n) in got.items() if v == 'issue']
    print('%s: %d ok, %d issue, %d missing' % (os.path.basename(a.chunk), len(got) - len(issues), len(issues),
                                                len(missing)))
    for i, n in issues:
        print('ISSUE %s: %s' % (i, n))
    for i in missing:
        print('MISSING %s' % i)
    return 1 if missing else 0


if __name__ == '__main__':
    sys.exit(main())
