"""Phase 7 ROM-level checks on the English build (references: skill pipeline.md §Checks).

Every byte the build changes is logged by build.put(); romdiff.check fails on overlapping writes, writes that later
writes overwrote, wrong original bytes and changed bytes no write explains. On top: every write lies in a range we
mean to touch, every table writes all its entries, every repointed code-string pointer lands on its English, and
no hook swallows a branch target."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build  # noqa: E402
import engine  # noqa: E402
import nfp  # noqa: E402
import romdiff  # noqa: E402
import text  # noqa: E402

needs_rom = pytest.mark.skipif(not build.ROM.is_file(), reason="ROM not present")


@pytest.fixture(scope='module')
def built():
    rom = build.ROM.read_bytes()
    code, records = build.load_tables()
    log = []
    new = build.make(rom, build.script_lines(), code, records, log=log)
    return rom, new, log, code, records


def allowed(code, records):
    """[(lo, hi, what)]: the only places the English build may write."""
    out = [(nfp.BASE, nfp.END, 'archive'), (nfp.GAP[1], nfp.SPILL_END, 'archive spill'),
           (engine.FREE, build.STRINGS[0], 'engine hooks'), (build.STRINGS[0], build.STRINGS[1], 'code strings')]
    out += [(off, off + len(bytes.fromhex(o)), 'hook site') for off, o, _ in engine.SITES]
    out += [(off, off + len(s) + 1, 'sprintf format') for off, s in engine.FORMATS.items()]
    out += [(int(r, 16), int(r, 16) + 4, e['id'] + ' ref') for e in code
            for r in e['refs'] + [x for v in e.get('subrefs', {}).values() for x in v]]
    out += [(int(e['addr'], 16), int(e['addr'], 16) + e['max'] + 1, e['id']) for e in records]
    return out


@needs_rom
def test_writes_logged_and_in_range(built):
    rom, new, log, code, records = built
    errs, _ = romdiff.check(rom, new, [], log)
    assert not errs, errs[:20]
    spans = allowed(code, records)
    outside = [(hex(off), by) for off, o, n, by in log
               if not any(lo <= off and off + len(n) <= hi for lo, hi, _ in spans)]
    assert not outside, outside[:20]
    # the engine's two areas stay apart (romdiff would see an overlap only when both are full)
    assert max(off + len(n) for off, o, n, by in log if by == 'engine' and off >= engine.FREE) <= build.STRINGS[0]


@needs_rom
def test_every_table_entry_written(built):
    rom, new, log, code, records = built
    for e in records:
        if e.get('en'):
            a, b = int(e['addr'], 16), text.encode_en(e['en'])
            assert new[a:a + e['max'] + 1] == b.ljust(e['max'] + 1, b'\0'), e['id']
    assert sum(by in {e['id'] for e in records} for *_, by in log) == sum(bool(e.get('en')) for e in records)
    for e in code:
        if not e.get('en'):
            continue
        want = text.encode_en(e['en']) + b'\0'
        for r in e['refs']:
            p = int.from_bytes(new[int(r, 16):int(r, 16) + 4], 'little') - 0x08000000
            assert build.STRINGS[0] <= p < build.STRINGS[1] and new[p:p + len(want)] == want, (e['id'], r)
        for k, refs in e.get('subrefs', {}).items():
            for r in refs:
                p = int.from_bytes(new[int(r, 16):int(r, 16) + 4], 'little') - 0x08000000
                assert build.STRINGS[0] <= p < build.STRINGS[1] and new[p:].split(b'\0')[0], (e['id'], r)


@needs_rom
def test_no_hook_swallows_a_branch_target(built):
    """Thumb B/Bcc/BL in the original code within 4 KB of a hook site must not land strictly inside the bytes the
    hook wrote (the game would jump into the middle of our code). Branches from inside a rewritten or dead span
    don't count."""
    cs = pytest.importorskip('capstone')
    rom, new, log, code, records = built
    md = cs.Cs(cs.CS_ARCH_ARM, cs.CS_MODE_THUMB)
    md.skipdata = True
    sites = [(off, off + len(n)) for off, o, n, by in log if by == 'engine' and off < nfp.BASE
             and off not in engine.FORMATS]
    dead = [(off, off + len(bytes.fromhex(o))) for off, o, _ in engine.SITES]
    bad = []
    for lo, hi in sites:
        start = max(0, lo - 0x1000) & ~1
        for i in md.disasm(rom[start:hi + 0x1000], 0x08000000 + start):
            src = i.address - 0x08000000
            if not i.mnemonic.startswith('b') or i.mnemonic.startswith(('bx', 'blx', 'bic')) or any(a <= src < b for a, b in dead):
                continue
            try:
                t = int(i.op_str.lstrip('#'), 16) - 0x08000000
            except ValueError:
                continue
            if lo < t < hi:
                bad.append((hex(src), i.mnemonic, hex(t)))
    assert not bad, bad
