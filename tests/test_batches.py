"""Batch tool and lint helpers (tools/batches.py, tools/lint.py)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import batches  # noqa: E402
import lint  # noqa: E402


def test_has_term_whole_runs():
    assert batches.has_term('ギンタ！', 'ギンタ')
    assert not batches.has_term('タイミング', 'ミン')
    assert not batches.has_term('ぼくも', 'くも')
    assert batches.has_term('ÄＲＭをくむ', 'ÄＲＭ')


def test_wrap_and_codes():
    lines, err = lint.wrap('word ' * 30, 2)
    assert err and len(lines) > 2
    lines, err = lint.wrap('Short line. / Second line.', 2)
    assert lines == ['Short line.', 'Second line.'] and not err
    assert lint.codes('{C0D04}x{C0F04} %s') == ['C0D04', 'C0F04', '%s']
    assert lint.codes('C0F04 を') == ['C0F04']


def test_char_errors():
    assert not lint.char_errors('MÄR ♥ {C0F04}ok{p5}')
    assert lint.char_errors('café')
    assert lint.char_errors('Cabbed')  # reads as a control code
    assert lint.char_errors('{x}')


def test_units_cover_every_box():
    """Every translatable script box is in exactly one unit; debug CH_ESC and composed boxes are not."""
    us = batches.units()
    ids = [e['id'] for u in us.values() if u['kind'] == 'script' for m in u['members'] for e in m]
    assert len(ids) == len(set(ids))
    assert not any(i.startswith('CH_ESC:') for i in ids)
    assert sum(u['kind'] == 'code' for u in us.values()) == 122
