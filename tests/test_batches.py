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


def test_wrap_moves_a_word_onto_a_one_word_last_line():
    text = 'What, you wanna go?!!! ...Don\'t mess with us!!!'
    greedy = lint.wrap(text, 2, widow=False)[0]
    assert len(greedy) == 2 and ' ' not in greedy[-1]  # the case the fix is for
    lines, err = lint.wrap(text, 2)
    assert not err and ' ' in lines[-1] and ' '.join(lines) == text


def test_text_reading_as_a_code_across_a_colour_code():
    assert lint.char_errors('{C0D04}Melt Ice{C0F04} and')  # "ceC0F" reads as c + 4 hex digits
    assert not lint.char_errors('{C0D04}Melt Ice{p1}{C0F04} and')
    assert not lint.char_errors('{C0D04}Melt Ice Stone{C0F04}')


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


def test_check_unit_rejects_near_misses():
    """Review probes: misspelt names, misplaced/missing honorifics, suffixes glued to placeholders."""
    us, rows = batches.units(), batches.glossary()
    assert batches.check_unit(us['arm001.name'], 'Babbob', rows)
    assert not batches.check_unit(us['arm001.name'], 'Babbo', rows)
    u = dict(us['CH_M00A:002af'], jp='{C0F04}ギンタとジャックさん')
    assert batches.check_unit(u, '{C0F04}Ginta-san and Jack', rows)
    assert not batches.check_unit(u, '{C0F04}Ginta and Jack-san', rows)
    u = dict(u, jp='{C0F04}ギンタどの！')
    assert batches.check_unit(u, '{C0F04}Ginta!', rows)
    assert not batches.check_unit(u, '{C0F04}Ginta-dono!', rows)
    u = dict(u, jp='{C0F04}ギンタぁ！！')
    assert not batches.check_unit(u, '{C0F04}Gintaaa!!', rows)
    assert batches.check_unit(us['code:087538'], '%sth obtained!!', rows)
    assert lint.char_errors('Got a %s!')
    assert not lint.char_errors('Contest No. %d')
