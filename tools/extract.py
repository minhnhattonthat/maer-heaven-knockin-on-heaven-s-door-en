"""extract.py: original ROM -> script/*.json (docs/re/text.md §Script files).

    python -X utf8 tools/extract.py            write script/ (existing files: en/status/notes kept per id)

Sources (every Japanese string in the ROM; tests/test_extract.py proves roundtrip and coverage):
- script/spc/<NAME>.json: display strings of each event script (0x10 ops that contain Shift-JIS; pure-ASCII 0x10
  strings are identifiers: file/label/flag names). id = '<NAME>:<CODE pos of the 0x10 op, hex>' (scrp.rebuild key).
  call/box/line: the native call that consumes the string (MswStr = message box), its index in the file, and the
  string's index among the pushes before it (MswStr line 0 is the speaker label); speaker: name from line 0.
- script/code.json: strings in the code's string block (CODE_BLOCK). refs = ROM offsets of the u32 pointers to the
  string (literal pools and pointer tables); subrefs = pointers into its middle, by byte offset; slot = bytes up
  to the next string (NUL padding included).
- script/records.json: name/description fields of the fixed-size ARM and item records (TABLES); max = bytes.
"""
import json
import struct
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import scrp  # noqa: E402
import text  # noqa: E402

ROM = ROOT / "rom" / "MAER Heaven - Knockin' on Heaven's Door (Japan).gba"
OUT = ROOT / "script"
CODE_END = 0x1C0920  # code + data before MAR.NFP
CODE_BLOCK = (0x87300, 0x89538)  # string block: native/file names and every code-side Japanese string
# (name, base, count, record size, ((field, offset, size), ...))
TABLES = [('arm', 0x1B0970, 445, 0x80, (('name', 0x0C, 0x22), ('desc', 0x2E, 0x22))),  # stats from +0x50
          ('item', 0x1BE7E0, 14, 0x50, (('name', 0x0C, 0x22), ('desc', 0x2E, 0x22)))]
KEEP = ('en', 'status', 'notes')  # translator-owned fields carried over on re-extract


def is_text(b):
    return any(c >= 0x80 for c in b)


def spc_entries(rom):
    """{file stem: [entry]} for every script with display strings."""
    out = {}
    for _, b, name in scrp.load_rom_scripts(rom, True):
        c = scrp.chunks(b)
        s, sz = c['CODE']
        nat = scrp.natives(b[c['FUNC'][0]:sum(c['FUNC'])]) if 'FUNC' in c else {}
        ents, pending, box = [], [], 0
        for p, op, arg in scrp.instrs(b[s:s + sz]):
            if op == 0x10:
                t = arg[2:-1]
                e = {'id': '%s:%05x' % (name[:-4], p), 'jp': text.decode(t), 'en': ''} if is_text(t) else None
                if e:
                    ents.append(e)
                pending.append(e)
            elif op == 0x80:
                call = nat.get(p + 1 - scrp.CODE_BASE, '?')
                spk = None
                for i, e in enumerate(pending):
                    if e:
                        e.update(call=call, box=box, line=i)
                        if call == 'MswStr' and i == 0 and e['jp'].startswith('{C0D04}［'):
                            spk = e['jp'][8:e['jp'].index('］')]
                        elif spk:
                            e['speaker'] = spk
                pending = []
                box += 1
        if ents:
            out[name[:-4]] = ents
    return out


def pointers(rom, lo, hi):
    """{ROM offset in [lo, hi): [ROM offsets of 4-aligned u32 pointers to it]} over the code area."""
    out = defaultdict(list)
    for p in range(0, CODE_END, 4):
        v = struct.unpack_from('<I', rom, p)[0] - 0x08000000
        if lo <= v < hi:
            out[v].append(p)
    return out


def code_entries(rom):
    lo, hi = CODE_BLOCK
    ptrs = pointers(rom, lo, hi)
    ents, i = [], lo
    while i < hi:
        j = rom.index(b'\0', i)
        if is_text(rom[i:j]):
            k = j
            while k < hi and not rom[k]:
                k += 1
            e = {'id': 'code:%06x' % i, 'jp': text.decode(rom[i:j]), 'en': '', 'slot': k - i,
                 'refs': ['%06x' % p for p in ptrs.get(i, [])]}
            sub = {str(o - i): ['%06x' % p for p in ptrs[o]] for o in range(i + 1, j) if o in ptrs}
            if sub:
                e['subrefs'] = sub
            ents.append(e)
        i = j + 1
    return ents


def record_entries(rom):
    ents = []
    for tab, base, n, size, fields in TABLES:
        for k in range(n):
            for f, off, ln in fields:
                a = base + k * size + off
                s = rom[a:a + ln].split(b'\0')[0]
                if s:
                    ents.append({'id': '%s%03d.%s' % (tab, k, f), 'jp': text.decode(s), 'en': '',
                                 'addr': '%06x' % a, 'max': ln - 1})
    return ents


def extract(rom):
    """{path relative to script/: [entry]}"""
    files = {'spc/%s.json' % k: v for k, v in spc_entries(rom).items()}
    files['code.json'] = code_entries(rom)
    files['records.json'] = record_entries(rom)
    return files


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, ents):
    """Write fresh extractor entries, keeping translator fields of an existing file; an entry whose jp changed under an existing
    translation gets status 'jp-changed'. Returns the number of such entries."""
    changed = 0
    if path.exists():
        old = {e['id']: e for e in load(path)}
        for e in ents:
            o = old.get(e['id'])
            if o:
                e.update({k: o[k] for k in KEEP if k in o})
                if o['jp'] != e['jp'] and o.get('en'):
                    e['status'] = 'jp-changed'
                    changed += 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ents, ensure_ascii=False, indent=1) + '\n', encoding='utf-8', newline='\n')
    return changed


def main(a):
    rom = ROM.read_bytes()
    files = extract(rom)
    changed = sum(write(OUT / k, v) for k, v in files.items())
    print('%d files, %d strings -> %s%s' % (len(files), sum(map(len, files.values())), OUT,
                                             ', %d translated strings have changed jp' % changed if changed else ''))


if __name__ == '__main__':
    main(sys.argv[1:])
