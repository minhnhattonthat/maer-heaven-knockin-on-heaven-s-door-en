"""List the debug chapter-select questions in CH_ESC.SPC with the code offset of each "yes" branch.

CH_ESC.SPC runs when the player talks to an NPC in the debug room AD0_R_3A (set up by DBG_ESC.SPC). Each NPC asks
yes/no questions in turn: MswStr(question), PopMenu, jump to a switch whose case 1 is the "yes" block. warp.lua
patches the first instruction of the loaded CH_ESC to `11 <yes block>` so any NPC runs the chosen block.

    python -X utf8 tools/debug/chesc.py      offset (rel. CODE_BASE, as in `scrp.py dis`) + question text
"""
import os
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import scrp  # noqa: E402

ROM = os.path.join(os.path.dirname(__file__), '..', '..', 'rom', "MAER Heaven - Knockin' on Heaven's Door (Japan).gba")


def questions(b):
    """Yield (yes_offset, question text, npc case) for each PopMenu in CH_ESC."""
    c = scrp.chunks(b)
    s, sz = c['CODE']
    code = b[s:s + sz]
    nat = scrp.natives(b[c['FUNC'][0]:c['FUNC'][0] + c['FUNC'][1]])
    ins = list(scrp.instrs(code))
    at = {p - scrp.CODE_BASE: (op, arg) for p, op, arg in ins}
    texts, pending = [], None
    for p, op, arg in ins:
        if op == 0x10 and arg[2:-1]:
            texts.append(arg[2:-1].decode('cp932', 'replace'))
        elif op == 0x80 and nat.get(p + 1 - scrp.CODE_BASE) == 'PopMenu':
            pending = texts[-2:]
            texts = []
        elif op == 0x80 and nat.get(p + 1 - scrp.CODE_BASE) == 'MswStr':
            pass
        elif op == 0x11 and pending is not None:
            sw = at.get(struct.unpack_from('<I', arg)[0])
            if sw and sw[0] == 0x15:
                cases = {struct.unpack_from('<I', sw[1], 2 + 8 * i)[0]: struct.unpack_from('<I', sw[1], 6 + 8 * i)[0]
                         for i in range(sw[1][1])}
                if 1 in cases:
                    yield cases[1], ''.join(t for t in pending if not t.isascii())
            pending = None


def main():
    rom = open(ROM, 'rb').read()
    b = next(x for _, x, n in scrp.load_rom_scripts(rom, True) if n == 'CH_ESC.SPC')
    for off, q in questions(b):
        print('0x%04X  %s' % (off, q))


if __name__ == '__main__':
    main()
