"""bgtext.py: English lettering on KMP background screens (KCG tiles + KCL palette + KMP map, docs/re/nfp.md).

Spec gfx/BG.tsv, one row per text area: `KMP<TAB>English<TAB>options`. Options as gfxtext.letter: rect=x,y,w,h (map
pixels, layer 0; default the whole map), font, align, style, ol, ol2, fill, bg, clear, bgrow, bold, dx, dy, grad;
plus pal=N (palette bank of the rewritten cells; default each cell keeps its own). English `-` only erases the rect
(the `clear` colours, else every pixel) to the background.
The rect's cells are drawn from the map, lettered, then re-tiled: each 8x8 cell reuses an identical tile or gets a
new one appended to the KCG (re-compressed); the map entries of the cells covering the rect point at them, no flips.

    python -X utf8 tools/bgtext.py preview [KMP..]   -> work/gfx/en/bg/<KMP>.png (orig | new, x2)
    python -X utf8 tools/bgtext.py check             every row fits (tests/test_gfxtext.py)
The build calls apply(files) on the archive's [(name, bytes)].
"""
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import gbalz  # noqa: E402
import gfxtext  # noqa: E402

SPEC = ROOT / 'gfx' / 'BG.tsv'


def spec():
    rows = []
    for ln in SPEC.read_text(encoding='utf-8').splitlines() if SPEC.exists() else []:
        if ln.strip() and not ln.startswith('#'):
            kmp, text, *opt = ln.split('\t')
            o = dict(kv.split('=', 1) for kv in (opt[0].split() if opt else []))
            kw = {k: o.pop(k) for k in ('font', 'align', 'style') if k in o}
            if 'rect' in o:
                kw['rect'] = tuple(map(int, o.pop('rect').split(',')))
            if 'grad' in o:
                kw['grad'] = [int(v) for v in o.pop('grad').split(',')]
            if 'clear' in o:
                kw['clear'] = {int(v) for v in o.pop('clear').split(',')}
                kw.setdefault('align', 'l')  # text on a box starts where the Japanese did (as gfxtext.spec)
            kw.update({k: int(v) for k, v in o.items()})  # pal dx dy ol ol2 fill bg bgrow bold
            rows.append((kmp, text, kw))
    return rows


class Screen:
    def __init__(self, kmp, kcg):
        self.kmp = bytearray(kmp)
        self.w, self.h = struct.unpack_from('<II', kmp, 0x14)
        self.lz = kcg[0] == 0x10
        raw = gbalz.decompress(kcg, 0)[0] if self.lz else kcg
        self.tiles = [raw[i:i + 32] for i in range(0, len(raw) - 31, 32)]
        self.tail = raw[32 * len(self.tiles):]

    def entry(self, cx, cy):
        return struct.unpack_from('<H', self.kmp, 0xC0 + 2 * (cy * self.w + cx))[0]

    def pixels(self):
        """{(x, y): colour index in its bank} of layer 0, and {(cx, cy): palette bank}."""
        img, pals = {}, {}
        for cy in range(self.h):
            for cx in range(self.w):
                e = self.entry(cx, cy)
                t, hf, vf = self.tiles[e & 0x3FF] if (e & 0x3FF) < len(self.tiles) else bytes(32), e & 0x400, e & 0x800
                pals[(cx, cy)] = e >> 12
                for y in range(8):
                    for x in range(8):
                        sx, sy = (7 - x if hf else x), (7 - y if vf else y)
                        b = t[sy * 4 + sx // 2]
                        img[(cx * 8 + x, cy * 8 + y)] = b >> 4 if sx & 1 else b & 15
        return img, pals

    def put(self, img, rect, pal=None):
        """Re-tile the cells covering rect from img (reuse identical tiles, else append); each cell keeps its
        palette bank unless pal is given."""
        index = {}
        for i, t in enumerate(self.tiles):
            index.setdefault(bytes(t), i)
        x, y, w, h = rect
        for cy in range(y // 8, -(-(y + h) // 8)):
            for cx in range(x // 8, -(-(x + w) // 8)):
                t = bytes((img[(cx * 8 + 2 * i % 8 + 1, cy * 8 + 2 * i // 8)] << 4) | img[(cx * 8 + 2 * i % 8, cy * 8 + 2 * i // 8)]
                          for i in range(32))
                if t not in index:
                    index[t] = len(self.tiles)
                    self.tiles.append(t)
                k = index[t]
                assert k < 1024, 'tile index past 10 bits'
                bank = self.entry(cx, cy) >> 12 if pal is None else pal
                struct.pack_into('<H', self.kmp, 0xC0 + 2 * (cy * self.w + cx), k | bank << 12)

    def kcg(self):
        raw = b''.join(self.tiles) + self.tail
        return gbalz.compress(raw) if self.lz else raw


def letter(scr, text, kw):
    img, pals = scr.pixels()
    kw = dict(kw)
    rect = kw.get('rect') or (0, 0, scr.w * 8, scr.h * 8)
    x, y, w, h = rect
    pal = kw.pop('pal', None)
    if text == '-':
        bg = kw.get('bg', 0)
        out = dict(img)
        for p in ((a, b) for b in range(y, y + h) for a in range(x, x + w)):
            if 'clear' not in kw or img[p] in kw['clear']:
                out[p] = bg
    else:
        out = gfxtext.letter(img, text, **kw)
    scr.put(out, rect, pal)
    return img, out


def apply(files, errors=None, log=None):
    """[(name, bytes)] with every BG.tsv row lettered (KMP map + its KCG rewritten)."""
    rows = spec()
    if not rows:
        return files
    d = dict(files)
    screens = {}
    for kmp, text, kw in rows:
        name = kmp + '.KMP'
        if name not in screens:
            kcg = d[name][0x1C:0x5C].split(b'\0')[0].decode('ascii')
            screens[name] = (kcg, Screen(d[name], d[kcg]))
        try:
            before, after = letter(screens[name][1], text, kw)
        except ValueError as e:
            if errors is None:
                raise
            errors.append('%s: %s' % (kmp, e))
            continue
        if log is not None:
            log.append((kmp, before, after, dict(gfxtext.LAST) if text != '-' else {'text': '-'}))
    for name, (kcg, scr) in screens.items():
        d[name], d[kcg] = bytes(scr.kmp), scr.kcg()
    return [(n, d[n]) for n, _ in files]


def _files():
    import nfp
    return nfp.unpack(open(nfp.ROM, 'rb').read())


def preview(only):
    from PIL import Image
    files = _files()
    errs, log = [], []
    new = dict(apply(files, errs, log))
    print('\n'.join(errs))
    out = ROOT / 'work' / 'gfx' / 'en' / 'bg'
    out.mkdir(parents=True, exist_ok=True)
    for kmp, _, _, x in log:
        print('%-8s %-24s %s' % (kmp, x.get('text', '-')[:24], {k: x[k] for k in ('font', 'style', 'bg', 'fill') if k in x}))
    for kmp in {k for k, *_ in log}:
        if only and kmp not in only:
            continue
        img = Image.new('RGB', (2 * 256 + 4, 256), (64, 0, 64))
        for i, d in enumerate((dict(files), new)):
            k = d[kmp + '.KMP']
            raw = d[k[0x5C:0x9C].split(b'\0')[0].decode('ascii')]
            pal = [((c & 31) * 8, (c >> 5 & 31) * 8, (c >> 10 & 31) * 8)
                   for c in struct.unpack_from('<%dH' % (len(raw) // 2), raw)]
            px, banks = Screen(k, d[k[0x1C:0x5C].split(b'\0')[0].decode('ascii')]).pixels()
            for (x, y), v in px.items():
                img.putpixel((i * 260 + x, y), pal[16 * banks[(x // 8, y // 8)] + v])
        img.resize((img.width * 2, img.height * 2), Image.NEAREST).save(out / (kmp + '.png'))
    print(out)


if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        preview(sys.argv[2:])
    elif sys.argv[1] == 'check':
        errs = []
        apply(_files(), errs)
        print('\n'.join(errs) or 'BG: OK')
        sys.exit(1 if errs else 0)
