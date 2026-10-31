"""Warp to every scene in tools/debug/scenes.lua from a cold boot; keep a proof shot and a savestate per scene.

    python -X utf8 tools/debug/regen.py [ROM] [--only a,b] [--jobs 3]

Writes work/states/<scene>.mss, work/qa/scenes/<scene>.png and work/qa/scenes/sheet*.png (labelled contact sheet).
Exit 1 if any scene failed to warp (no "scene saved" in its log). Rerun after code, font or graphics changes:
savestates keep the old code and VRAM.
"""
import argparse
import concurrent.futures as cf
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from skill import SKILL  # noqa: E402

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ORIG = os.path.join(REPO, 'rom', "MAER Heaven - Knockin' on Heaven's Door (Japan).gba")


def scene_names():
    src = open(os.path.join(REPO, 'tools', 'debug', 'scenes.lua'), encoding='utf8').read()
    return re.findall(r'^(?:\s+|S\.list\.)(\w+)\s*=\s*\{', src, re.M)


def run(rom, name):
    out = os.path.join(REPO, 'work', 'qa', 'regen', name)
    state = os.path.join(REPO, 'work', 'states', name + '.mss').replace('\\', '/')
    cmd = [sys.executable, '-X', 'utf8', os.path.join(SKILL, 'scripts', 'emu.py'), rom, '--out', out,
           '--script', os.path.join(REPO, 'tools', 'debug', 'warp.lua'),
           '--var', "SCENE='%s'" % name, '--var', 'SAVE=[[%s]]' % state, '--frames', '12000', '--timeout', '400']
    with open(out + '.out', 'w', encoding='utf8') as f:
        rc = subprocess.call(cmd, stdout=f, stderr=subprocess.STDOUT)
    log = open(os.path.join(out, 'log.txt'), encoding='utf8').read() if os.path.exists(os.path.join(out, 'log.txt')) else ''
    ok = rc == 0 and 'scene saved' in log
    if ok:
        shutil.copy(os.path.join(out, 'scene.png'), os.path.join(REPO, 'work', 'qa', 'scenes', name + '.png'))
    return name, ok, rc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('rom', nargs='?', default=ORIG)
    ap.add_argument('--only')
    ap.add_argument('--jobs', type=int, default=3)
    a = ap.parse_args()
    names = a.only.split(',') if a.only else scene_names()
    for d in ('work/states', 'work/qa/scenes', 'work/qa/regen'):
        os.makedirs(os.path.join(REPO, d), exist_ok=True)
    bad = []
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        for name, ok, rc in ex.map(lambda n: run(os.path.abspath(a.rom), n), names):
            print('%-18s %s' % (name, 'ok' if ok else 'FAIL rc=%d' % rc), flush=True)
            if not ok:
                bad.append(name)
    shots = [os.path.join(REPO, 'work', 'qa', 'scenes', n + '.png') for n in names if n not in bad]
    if shots:
        subprocess.call([sys.executable, '-X', 'utf8', os.path.join(SKILL, 'scripts', 'sheet.py'), *shots, '--div', '1',
                         '--out', os.path.join(REPO, 'work', 'qa', 'scenes', 'sheet.png')])
    print('%d/%d scenes ok' % (len(names) - len(bad), len(names)), 'failed: ' + ','.join(bad) if bad else '')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
