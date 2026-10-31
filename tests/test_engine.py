"""Phase 5 engine patch (docs/re/vwf.md): font, hooks, English encoding, marker build."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build  # noqa: E402
import engine  # noqa: E402
import nfp  # noqa: E402
import gbalz  # noqa: E402
import scrp  # noqa: E402
import text  # noqa: E402

needs_rom = pytest.mark.skipif(not build.ROM.is_file(), reason="ROM not present")


def test_font_and_widths():
    g = engine.glyphs()
    assert all(rows[7] == 0 or c in b'gjpqy,;_' for c, (rows, _) in g.items())  # row 7: descenders only
    adv = engine.advance()
    assert engine.width(b'Hi', adv) == adv[ord('H') - 32] + adv[ord('i') - 32]
    assert engine.width(b'C0D04[A]C0F04', adv) == engine.width(b'[A]', adv)  # codes take no room
    assert engine.width(b'Cafe!', adv) == sum(adv[c - 32] for c in b'Cafe!')  # C + non-hex is a letter


def test_encode_en():
    assert text.encode_en('{C0D04}[Ginta]{C0F04}') == b'C0D04[Ginta]C0F04'
    assert text.encode_en('MÄR…') == b'M' + bytes.fromhex('f056') + 'R…'.encode('cp932')


@needs_rom
def test_patches_apply_to_original():
    rom = bytearray(build.ROM.read_bytes())
    engine.apply(rom)  # asserts the original bytes at every site and that free space is unused


@needs_rom
def test_marker_build_scripts():
    """Every script of the marker build parses and keeps CODE size 2 mod 4 (the VM's stack-top write)."""
    rom = build.ROM.read_bytes()
    lines, _ = build.marker(build.script_lines())
    out = build.build(rom, build.edits_from(lines), patch_engine=True)
    for name, b in nfp.unpack(out):
        if name.endswith('.SPC'):
            raw = gbalz.decompress(b, 0)[0] if b[0] == 0x10 else b
            assert scrp.chunks(raw)['CODE'][1] % 4 == 2, name
