"""Phase 3 identity build (docs/re/nfp.md §Rebuild): unpack -> repack with no edits gives the original ROM;
script relocation and the archive's jump over the fixed data block are exact."""
import struct
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build  # noqa: E402
import gbalz  # noqa: E402
import nfp  # noqa: E402
import scrp  # noqa: E402

needs_rom = pytest.mark.skipif(not build.ROM.is_file(), reason="ROM not present")


@pytest.fixture(scope='module')
def rom():
    return build.ROM.read_bytes()


def decoded(b):
    return gbalz.decompress(b, 0)[0] if b[0] == 0x10 else b


@needs_rom
def test_identity_build(rom):
    assert build.build(rom) == rom


def strings(b):
    s, sz = scrp.chunks(b)['CODE']
    return [(p, arg[2:].split(b'\0')[0]) for p, op, arg in scrp.instrs(b[s:s + sz]) if op == 0x10]


@needs_rom
def test_relocation_roundtrip(rom):
    """Lengthen every string: the script still parses, jumps land, each string is pushed by the next op and natives
    keep their names; putting the old strings back gives the original bytes."""
    for _, b, name in scrp.load_rom_scripts(rom, True):
        old = strings(b)
        long = scrp.rebuild(b, {p: t + b'AB' for p, t in old})
        c = scrp.chunks(long)
        s, sz = c['CODE']
        ins = list(scrp.instrs(long[s:s + sz]))
        starts = {p - scrp.CODE_BASE for p, _, _ in ins} | {sz - scrp.CODE_BASE}
        assert all(t in starts for p, op, arg in ins for t in scrp.targets(op, arg)), name
        for i, (p, op, arg) in enumerate(ins):
            if op == 0x10:
                assert struct.unpack_from('<I', ins[i + 1][2], 1)[0] == p + 3 - scrp.CODE_BASE, name
        if 'FUNC' in c:
            f0, f1 = scrp.chunks(b)['FUNC'], c['FUNC']
            n0, n1 = scrp.natives(b[f0[0]:f0[0] + f0[1]]), scrp.natives(long[f1[0]:f1[0] + f1[1]])
            assert [n0[k] for k in sorted(n0)] == [n1[k] for k in sorted(n1)], name
            assert all(ins_op == 0x80 for ins_op in (long[s + k - 1 + scrp.CODE_BASE] for k in n1)), name
        new = strings(long)
        assert [t for _, t in new] == [t + b'AB' for _, t in old]
        assert scrp.rebuild(long, {p: t for (p, _), (_, t) in zip(new, old)}) == b, name


@needs_rom
def test_grown_archive_jumps_gap(rom):
    """Our compressor packs worse than the original, so recompressing every script overflows into GAP: the archive
    must jump it after an .SPC, keep every file's content, and leave the fixed data block alone."""
    out = build.build(rom, recompress=True)
    assert out[nfp.GAP[0]:nfp.GAP[1] - 8] == rom[nfp.GAP[0]:nfp.GAP[1] - 8]
    ents = nfp.entries(out)
    j = next(i for i, (_, off, _) in enumerate(ents) if off >= nfp.GAP[1])
    assert ents[j - 1][0].endswith('.SPC')
    a, b = nfp.unpack(rom), nfp.unpack(out)
    assert [n for n, _ in a] == [n for n, _ in b]
    assert all(decoded(x) == decoded(y) for (_, x), (_, y) in zip(a, b))
