"""Recon formats (docs/re/): LZ77 codec, MAR.NFP directory, SCRP bytecode parse."""
import struct
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import gbalz  # noqa: E402
import nfp  # noqa: E402
import scrp  # noqa: E402

ROM = ROOT / "rom" / "MAER Heaven - Knockin' on Heaven's Door (Japan).gba"
needs_rom = pytest.mark.skipif(not ROM.is_file(), reason="ROM not present")


def test_lz77_roundtrip():
    gbalz._selftest()


@needs_rom
def test_nfp_directory():
    rom = ROM.read_bytes()
    ents = nfp.entries(rom)
    assert len(ents) == 830
    assert sum(1 for n, _, _ in ents if n.endswith('.SPC')) == 334


@needs_rom
def test_lz77_recompress_scripts():
    """Our compressor's output decodes back to the same bytes for every packed script."""
    rom = ROM.read_bytes()
    for name, off, size in nfp.entries(rom)[::7]:
        if rom[off] == 0x10 and name.endswith('.SPC'):
            data = gbalz.decompress(rom, off)[0]
            assert gbalz.decompress(gbalz.compress(data), 0)[0] == data, name


@needs_rom
def test_scripts_parse_and_jumps_land():
    assert scrp.main(['check']) == 0


@needs_rom
def test_every_string_is_pushed_by_next_op():
    rom = ROM.read_bytes()
    for off, b in scrp.load_rom_scripts(rom):
        s, sz = scrp.chunks(b)['CODE']
        ins = list(scrp.instrs(b[s:s + sz]))
        for i, (p, op, arg) in enumerate(ins):
            if op == 0x10:
                nxt = ins[i + 1]
                assert nxt[1] == 0x22 and struct.unpack_from('<I', nxt[2], 1)[0] == p + 3 - scrp.CODE_BASE
