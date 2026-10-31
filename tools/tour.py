"""Screen tour for visual QA: every scene of tools/debug/scenes.lua from a cold boot, A pressed every 30 frames after
the warp (dialogue advances, first choices taken), one shot per finished dialogue box (tools/lua/boxshot.lua) plus
one every 600 frames; contact sheets per scene.

    python -X utf8 tools/tour.py [ROM] [--out work/qa/tour] [--only a,b] [--frames 6000] [--jobs 3]

Sheets: OUT/<scene>/sheet*.png (box_<frame> shots first, then f<frame>). Then (docs/re/debug.md, emulator-qa):
    qa_gate.py init work/qa/manifest.tsv work/qa/tour      the original ROM's tour goes to work/qa/tour_jp
"""
import argparse
import concurrent.futures as cf
import glob
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from skill import SKILL  # noqa: E402
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'debug'))
from regen import REPO, scene_names  # noqa: E402

SKIP = {'debug_room'}  # unpatched CH_ESC NPC menu: stays Japanese by design (build.KEEP_SCRIPTS)


def run(rom, out, name, frames):
    d = os.path.join(out, name)
    shutil.rmtree(d, ignore_errors=True)
    cmd = [sys.executable, '-X', 'utf8', os.path.join(SKILL, 'scripts', 'emu.py'), rom, '--out', d,
           '--script', os.path.join(REPO, 'tools', 'debug', 'warp.lua'),
           '--script', os.path.join(REPO, 'tools', 'lua', 'boxshot.lua'),
           '--var', "SCENE='%s'" % name, '--var', 'TOUR_MASH=30', '--var', 'BOXDELAY=20', '--var', 'GOD=1',
           '--frames', str(frames), '--shot-every', '600', '--timeout', '600']
    with open(d + '.out', 'w', encoding='utf8') as f:
        rc = subprocess.call(cmd, stdout=f, stderr=subprocess.STDOUT)
    shots = sorted(glob.glob(os.path.join(d, 'box_*.png'))) + sorted(glob.glob(os.path.join(d, 'f*.png')))
    if shots:
        subprocess.call([sys.executable, '-X', 'utf8', os.path.join(SKILL, 'scripts', 'sheet.py'), *shots,
                         '--changed', '0.01', '--div', '1', '--max', '16', '--out', os.path.join(d, 'sheet.png')],
                        stdout=subprocess.DEVNULL)
    return name, rc, len(glob.glob(os.path.join(d, 'box_*.png')))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('rom', nargs='?', default=os.path.join(REPO, 'build', 'maer_en.gba'))
    ap.add_argument('--out', default=os.path.join(REPO, 'work', 'qa', 'tour'))
    ap.add_argument('--only')
    ap.add_argument('--frames', type=int, default=6000)
    ap.add_argument('--jobs', type=int, default=3)
    a = ap.parse_args()
    names = a.only.split(',') if a.only else [n for n in scene_names() if n not in SKIP]
    os.makedirs(a.out, exist_ok=True)
    bad = []
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        for name, rc, boxes in ex.map(lambda n: run(os.path.abspath(a.rom), a.out, n, a.frames), names):
            print('%-18s rc=%d boxes=%d' % (name, rc, boxes), flush=True)
            if rc:
                bad.append(name)
    print('%d/%d scenes ran' % (len(names) - len(bad), len(names)), 'failed: ' + ','.join(bad) if bad else '')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
