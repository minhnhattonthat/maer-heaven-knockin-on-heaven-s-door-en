"""Debug tool (docs/re/debug.md): every chesc offset in scenes.lua is a "yes" block of CH_ESC.SPC; FUNC names parse."""
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tools" / "debug"))
import chesc  # noqa: E402
import scrp  # noqa: E402

ROM = ROOT / "rom" / "MAER Heaven - Knockin' on Heaven's Door (Japan).gba"
needs_rom = pytest.mark.skipif(not ROM.is_file(), reason="ROM not present")


def test_natives():
    func = b'SetCrtFade\x00\x0b\x00\x00\x00\x00\x00\x00\x00chain\x001\x00\x00\x00\x00\x00\x00\x00\x00'  # S_MAIN.SPC
    assert scrp.natives(func) == {0x0b: 'SetCrtFade', 0x31: 'chain'}


@needs_rom
def test_scene_offsets_are_chesc_yes_blocks():
    rom = ROM.read_bytes()
    b = next(x for _, x, n in scrp.load_rom_scripts(rom, True) if n == 'CH_ESC.SPC')
    yes = {off for off, _ in chesc.questions(b)}
    assert len(yes) == 40
    used = {int(h, 16) for h in re.findall(r'chesc = (0x[0-9A-F]+)', (ROOT / 'tools/debug/scenes.lua').read_text('utf8'))}
    assert used and used <= yes, sorted(hex(x) for x in used - yes)


@needs_rom
def test_scene_scripts_exist():
    import nfp
    names = {n for n, _, _ in nfp.entries(ROM.read_bytes())}
    src = (ROOT / 'tools/debug/scenes.lua').read_text('utf8')
    for n in re.findall(r'(?:npc|script) = "([A-Z0-9_]+\.SPC)"', src):
        assert n in names, n
