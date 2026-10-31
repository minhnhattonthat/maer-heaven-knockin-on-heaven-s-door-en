"""Which code strings / records each scene draws, and with which renderer (tools/lua/drawlog.lua on a marker build).

    python -X utf8 tools/debug/drawmap.py [ROM] [--only scene[@route],..] [--jobs 4] [--frames 4000]

ROM defaults to build/marker.gba. A scene may carry extra presses after the warp: `shop_a1@6 a;60 -;6 a` (route
steps as in scenes.lua, ';'-separated; names with a route get the key `scene@N`). Writes
work/qa/drawmap/<key>/log.txt + shots (one per 120 frames) and work/qa/drawmap/map.tsv
(id, renderer, x, row, scene, frame) for every [cN] / [rN] drawn; prints the code ids never seen.
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import subprocess
import sys
import zlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from skill import SKILL  # noqa: E402

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(REPO, 'work', 'qa', 'drawmap')
DEFAULT = ['menu', 'menu_deck', 'menu_deck_edit', 'menu_item', 'menu_status', 'menu_arm_list', 'menu_get_arm',
           'world_map', 'shop_a1', 'shop_e1', 'engraver', 'battle_win', 'mode_versus', 'mode_arm_trade',
           'mode_dungeon', 'dungeon_menu', 'battle_arm_select', 'full_items', 'all_party']


def run(rom, spec, frames):
    name, _, route = spec.partition('@')
    key = name if not route else '%s@%04d' % (name, zlib.crc32(route.encode()) % 10000)
    out = os.path.join(OUT, key)
    os.makedirs(out, exist_ok=True)
    cmd = [sys.executable, '-X', 'utf8', os.path.join(SKILL, 'scripts', 'emu.py'), rom, '--out', out,
           '--script', os.path.join(REPO, 'tools', 'debug', 'warp.lua'),
           '--script', os.path.join(REPO, 'tools', 'lua', 'drawlog.lua'),
           '--var', "SCENE='%s'" % name, '--frames', str(frames), '--shot-every', '120', '--timeout', '600']
    if route:
        rf = out + '.route.txt'
        with open(rf, 'w', encoding='utf8') as f:
            f.write(''.join(s.strip() + '\n' for s in route.split(';')))
        cmd += ['--var', 'AFTER=[[%s]]' % rf.replace('\\', '/')]
    with open(out + '.out', 'w', encoding='utf8') as f:
        subprocess.call(cmd, stdout=f, stderr=subprocess.STDOUT)
    log = os.path.join(out, 'log.txt')
    rows = []
    for line in open(log, encoding='utf8', errors='replace') if os.path.exists(log) else []:
        m = re.match(r'draw (\w+) \w+ x=(\S+) y=(\S+) f(\d+) (.*)', line)
        if m:
            for i in re.findall(r'\[([cr]\d+)\]', m.group(5)):
                rows.append((i, m.group(1), m.group(2), m.group(3), key, m.group(4)))
    return key, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('rom', nargs='?', default=os.path.join(REPO, 'build', 'marker.gba'))
    ap.add_argument('--only')
    ap.add_argument('--jobs', type=int, default=4)
    ap.add_argument('--frames', type=int, default=4000)
    a = ap.parse_args()
    specs = a.only.split(',') if a.only else DEFAULT
    os.makedirs(OUT, exist_ok=True)
    allrows = []
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        for key, rows in ex.map(lambda s: run(os.path.abspath(a.rom), s, a.frames), specs):
            print('%-24s %d ids' % (key, len({r[0] for r in rows})), flush=True)
            allrows += rows
    path = os.path.join(OUT, 'map.tsv')
    old = [l.rstrip('\n').split('\t') for l in open(path, encoding='utf8')] if os.path.exists(path) else []
    keys = {r[4] for r in allrows} | {s.split('@')[0] for s in specs}
    rows = sorted({tuple(r) for r in old if r[4] not in keys} | set(allrows),
                  key=lambda r: (r[0][0], int(r[0][1:]), r[4]))
    with open(path, 'w', encoding='utf8') as f:
        f.writelines('\t'.join(r) + '\n' for r in rows)
    code = json.load(open(os.path.join(REPO, 'script', 'code.json'), encoding='utf8'))
    seen = {r[0] for r in rows}
    print('code strings never drawn:', ' '.join('c%d' % n for n in range(len(code)) if 'c%d' % n not in seen))


if __name__ == '__main__':
    sys.exit(main())
