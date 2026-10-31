import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import check_rom  # noqa: E402

ROM = ROOT / "rom" / "MAER Heaven - Knockin' on Heaven's Door (Japan).gba"


@pytest.mark.skipif(not ROM.is_file(), reason="ROM not present")
def test_rom_matches_sha1():
    check_rom.check()


def test_rom_sha1_listing_is_filled():
    lines = [l for l in (ROOT / "rom.sha1").read_text(encoding="utf-8").splitlines() if l and not l.startswith("#")]
    assert lines and len(lines[0].split()[0]) == 40
