"""Sprite lettering (tools/gfxtext.py): every spec row fits, relaid frames load as the game expects."""
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import gfxtext  # noqa: E402


def test_specs_fit_and_relayout_is_loadable():
    for bank in ('SYSTEM', 'EFFECT'):
        if not gfxtext.spec(bank):
            continue
        errs = []
        b = gfxtext._bank(bank)
        n = gfxtext.NCD(gfxtext.apply(bank + '.NCD', b, errs))
        assert not errs, errs
        for f in {f for f, _, _ in gfxtext.spec(bank)}:
            first, count = struct.unpack_from('<IH', n.b, n.frame_o + 8 * f)
            t = None
            for k in range(first, first + count):
                e = n.b[n.oam_o + 20 * k:n.oam_o + 20 * k + 20]
                x, y, w, h, tile, *_ = n.objs(f)[k - first]
                assert w == 32, (f, w)  # 16/8-wide objects show misplaced in game
                assert e[18:20] == struct.pack('>H', w * h // 64), f  # big-endian tile count: the loader's DMA size
                assert t is None or tile == t, f  # one run of consecutive tiles in OAM order
                t = tile + w * h // 64
