"""gfxtext.py: English lettering for the Japanese sprite frames of the NCD banks (docs/re/graphics.md).

Spec: gfx/<BANK>.tsv (BANK = SYSTEM or EFFECT), one row per text area: `frames<TAB>English<TAB>options`.
  frames   0701, or 1878-1879 (each frame gets the same English in its own colours)
  options  space-separated: rect=x,y,w,h (frame pixels, default the whole frame); font=huge|big|mid|small|N (huge or N = Pixelify at N px only when named; grad=i,j,.. fills the glyphs
           top to bottom with those indices; default:
           the largest that fits on the frame's tiles); align=l|c|r (default c); dx=N dy=N (nudge);
           style=auto|outline|bevel|shadow|none; ol=N (outline / bevel top-left) ol2=N (bevel bottom-right)
           fill=N bg=N (palette indices instead of the detected ones); w=N (frame width, default the old one;
           centred), wr=N / wl=N (same, growing right / left from the old edge);
           bgfrom=N (restore the background from that text-free frame); bgrep=x,w (background = the frame's
           text-free columns x..x+w-1 repeated, for patterned bars); bgrow=N (with clear: erased pixels take
           the colour of row N in the same column, for text over a shaded ball)
Every lettered frame gets fresh sprites and tiles (NCD.relayout): frames share blank tiles and overlap objects.
The text area is cleared to its background colour, then the English is drawn in the original's style: the outline
colour (ink pixels touching the background) around the glyphs, the fill colour taken per row from the original
(gradients follow the rows). Tiles are rewritten in place: same tile count, same OAM, same palettes.

    python -X utf8 tools/gfxtext.py preview SYSTEM [0701 1878-1879 ..]   -> work/gfx/en/<frame>.png (orig | new, x3)
    python -X utf8 tools/gfxtext.py shared SYSTEM                        tiles of spec frames used by other frames
The build calls apply(name, bytes) for SYSTEM.NCD / EFFECT.NCD.
"""
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import engine  # noqa: E402

SHAPES = {(0, 0): (8, 8), (0, 1): (16, 16), (0, 2): (32, 32), (0, 3): (64, 64),
          (1, 0): (16, 8), (1, 1): (32, 8), (1, 2): (32, 16), (1, 3): (64, 32),
          (2, 0): (8, 16), (2, 1): (8, 32), (2, 2): (16, 32), (2, 3): (32, 64)}
BIG = ROOT / 'fonts' / 'PixelifySans.ttf'  # OFL, variable; Medium at 13/11 px keeps clean 1-px pixel strokes


class NCD:
    def __init__(self, b):
        self.b = bytearray(b)
        _, _, self.frame_o, self.oam_o, self.pal_o, self.tile_o = struct.unpack_from('<6I', b, 0x20)
        cnt = struct.unpack_from('<8I', b, 0x40)
        self.nframes, self.noam = cnt[2], cnt[3]
        self.shift = {}  # frame -> how far relayout moved its left edge
        self.free = set()  # tiles no frame uses any more (freed by relayout)

    def objs(self, fr):
        first, count = struct.unpack_from('<IH', self.b, self.frame_o + 8 * fr)
        out = []
        for k in range(first, min(first + count, self.noam)):
            a0, a1 = struct.unpack_from('<HH', self.b, self.oam_o + 20 * k)
            p, t = struct.unpack_from('<II', self.b, self.oam_o + 20 * k + 4)
            wh = SHAPES.get((a0 >> 14, a1 >> 14))
            if wh:
                y, x = a0 & 0xff, a1 & 0x1ff
                out.append((x - 512 if x >= 256 else x, y - 256 if y >= 128 else y, wh[0], wh[1], t, p,
                            bool(a1 & 0x1000), bool(a1 & 0x2000)))
        return out

    def _pixels(self, fr, every=False):
        """[(frame x, frame y, byte offset, high nibble, tile)] per covered pixel, frame origin at the bbox top
        left; the first OAM entry covering a pixel wins (lowest index is drawn on top), unless every."""
        objs = self.objs(fr)
        x0, y0 = min(o[0] for o in objs), min(o[1] for o in objs)
        seen, out = set(), []
        for x, y, w, h, t, p, hf, vf in objs:
            tw = w // 8
            for py in range(h):
                for px in range(w):
                    fx, fy = x - x0 + px, y - y0 + py
                    if (fx, fy) in seen and not every:
                        continue
                    seen.add((fx, fy))
                    sx, sy = (w - 1 - px if hf else px), (h - 1 - py if vf else py)
                    tile = t + (sy // 8) * tw + sx // 8
                    off = self.tile_o + 32 * tile + (sy % 8) * 4 + (sx % 8) // 2
                    out.append((fx, fy, off, sx & 1, tile))
        return out

    def get(self, fr):
        """{(x, y): palette index} as shown: the first OAM entry with a non-transparent pixel there."""
        out = {}
        for x, y, o, hi, _ in self._pixels(fr, every=True):
            if not out.get((x, y)):
                out[(x, y)] = self.b[o] >> 4 if hi else self.b[o] & 15
        return out

    def put(self, fr, img):
        for x, y, o, hi, _ in self._pixels(fr):
            v = img[(x, y)]
            self.b[o] = (self.b[o] & 0x0F) | (v << 4) if hi else (self.b[o] & 0xF0) | v

    def relayout(self, fr, width, anchor='c'):
        """Give frame fr fresh sprites: rows of 16 px (8 for a last row) of 32/16/8-wide objects, `width` px wide
        (default the old bbox, rounded up to 8), centred on the old bbox, same top, height and palette, on one run of
        consecutive tiles (the frame's own old tiles when they are enough, else appended to the bank); the new OAM
        entries go after the old ones (the palette and tile sections move, header offsets and counts follow).
        Returns the old image moved onto the new layout, {(x, y): index} (0 where the old frame had no pixel)."""
        old, objs = self.get(fr), self.objs(fr)
        x0, y0 = min(o[0] for o in objs), min(o[1] for o in objs)
        x1, y1 = max(o[0] + o[2] for o in objs), max(o[1] + o[3] for o in objs)
        # shortcut: 32-wide objects only; 16/8-wide ones showed 8-16 px right of their x in game (cause unknown)
        H, W = -(-(y1 - y0) // 8) * 8, -(-(width or x1 - x0) // 32) * 32
        # anchor l: grow to the right (button hints keep their icon); r: grow to the left (right-aligned credits)
        nx0 = x0 if anchor == 'l' else x1 - W if anchor == 'r' else (x0 + x1) // 2 - W // 2
        blocks = [(bx, by, 32, min(16, H - by)) for by in range(0, H, 16) for bx in range(0, W, 32)]
        N = sum(w * h // 64 for _, _, w, h in blocks)
        first = struct.unpack_from('<I', self.b, self.frame_o + 8 * fr)[0]
        tpl = self.b[self.oam_o + 20 * first:self.oam_o + 20 * first + 20]
        a0t, a1t = struct.unpack_from('<HH', tpl)
        ntiles = (len(self.b) - self.tile_o) // 32
        use = self.tile_use()
        for o in objs:  # fr lets go of its old tiles; ones nobody uses any more join the free pool
            for k in range(o[4], o[4] + o[2] * o[3] // 64):
                use[k].discard(fr)
                if not use[k]:
                    self.free.add(k)
        # one run of consecutive tiles in OAM order (each object's DMA takes its own tile + count); the smallest
        # free run that fits, else appended: the bank may only grow by the slack before the fixed ROM block
        runs, start = [], None
        for k in sorted(self.free) + [None]:
            if start is not None and k == prev + 1:
                prev = k
                continue
            if start is not None:
                runs.append((prev - start + 1, start))
            start = prev = k
        fit = min((r for r in runs if r[0] >= N), default=None)
        at, t = (fit[1], ntiles) if fit else (ntiles, ntiles + N)
        self.free -= set(range(at, at + N))
        ent = bytearray()
        for bx, by, bw, bh in blocks:
            shape, size = {(32, 16): (1, 2), (16, 16): (0, 1), (8, 16): (2, 0),
                           (32, 8): (1, 1), (16, 8): (1, 0), (8, 8): (0, 0)}[(bw, bh)]
            need = bw * bh // 64
            a0 = (a0t & 0x3F00) | (shape << 14) | ((y0 + by) & 0xFF)
            a1 = (size << 14) | ((nx0 + bx) & 0x1FF)
            ent += struct.pack('<HHII', a0, a1, objs[0][5], at) + tpl[12:18] + struct.pack('>H', need)  # BE count
            for k in range(at, at + need):
                use.setdefault(k, set()).add(fr)
            at += need
        k = len(ent) // 20
        end = self.oam_o + 20 * self.noam  # 8 pad bytes may follow before the palettes
        self.b[end:end] = ent
        self.pal_o, self.tile_o = self.pal_o + len(ent), self.tile_o + len(ent)
        self.b += bytes(32 * (t - ntiles))
        struct.pack_into('<2I', self.b, 0x30, self.pal_o, self.tile_o)
        c = list(struct.unpack_from('<8I', self.b, 0x40))
        c[3] += k
        c[4] += k
        c[7] += t - ntiles
        struct.pack_into('<8I', self.b, 0x40, *c)
        struct.pack_into('<IH', self.b, self.frame_o + 8 * fr, self.noam, k)
        self.noam += k
        self.shift[fr] = nx0 - x0
        return {(x, y): old.get((x + nx0 - x0, y), 0) for x, y in self.get(fr)}

    def tile_use(self):
        """{tile: frames whose OAM entries use it} (computed once, kept current by relayout)."""
        if not hasattr(self, '_use'):
            self._use = {}
            for f in range(self.nframes):
                for o in self.objs(f):
                    for k in range(o[4], o[4] + o[2] * o[3] // 64):
                        self._use.setdefault(k, set()).add(f)
        return self._use

    def tiles(self, fr):
        return {p[4] for p in self._pixels(fr)}

    def palette(self, fr):
        p = self.objs(fr)[0][5]
        raw = self.b[self.pal_o + 32 * p:self.pal_o + 32 * p + 32]
        return [((c & 31) * 8, (c >> 5 & 31) * 8, (c >> 10 & 31) * 8) for c in struct.unpack('<16H', raw)]


# --- fonts: a mask is a list of rows of 0/1 --------------------------------------------------------------------

def mask_small(text):
    g = engine.glyphs()
    rows = [[] for _ in range(8)]
    a, aw = g[ord('A')]
    g[ord('Ä')] = (bytes([0x80 | 0x80 >> (aw - 1)]) + a[:7], aw)  # A one row down, dots over its outer columns
    g[ord('©')] = (bytes([0x38, 0x44, 0xBA, 0xA2, 0xBA, 0x44, 0x38, 0]), 7)  # copyright screen (T_C01)
    g[ord('・')] = (bytes([0, 0, 0, 0xC0, 0xC0, 0, 0, 0]), 2)  # Japanese middle dot, as in the copyright line
    for ch in text:
        if ord(ch) not in g:
            raise ValueError('small font has no %r' % ch)
        bits, w = g[ord(ch)]
        for r in range(8):
            rows[r] += [(bits[r] >> (7 - i)) & 1 for i in range(w)] + [0]
    return [r[:-1] for r in rows], 0  # (mask, cap top)


def mask_ttf(text, size):
    from PIL import Image, ImageDraw, ImageFont
    f = ImageFont.truetype(str(BIG), size)
    f.set_variation_by_name(b'Medium')
    img = Image.new('L', (len(text) * size + 8, size * 2), 0)
    d = ImageDraw.Draw(img)
    d.fontmode = '1'
    d.text((2, 0), text, font=f, fill=255)
    cap = Image.new('L', img.size, 0)
    ImageDraw.Draw(cap).text((2, 0), 'H', font=f, fill=255)
    _, ctop, _, cbot = cap.getbbox()
    x0, _, x1, _ = img.getbbox()
    top = min(ctop, img.getbbox()[1])
    bot = max(cbot, img.getbbox()[3])
    px = img.load()
    return [[1 if px[x, y] else 0 for x in range(x0, x1)] for y in range(top, bot)], ctop - top, cbot - ctop


FONTS = {'huge': lambda t: mask_ttf(t, 26), 'big': lambda t: mask_ttf(t, 13), 'mid': lambda t: mask_ttf(t, 11), 'small': mask_small}


# --- relettering ------------------------------------------------------------------------------------------------

def _common(vals):
    return max(set(vals), key=vals.count) if vals else None


RING = {'outline': [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if a or b],
        'shadow': [(1, 0), (0, 1), (1, 1)], 'none': [],
        'bevel_tl': [(-1, 0), (0, -1), (-1, -1), (1, -1)], 'bevel_br': [(1, 0), (0, 1), (1, 1), (-1, 1)]}


def letter(img, text, rect=None, font=None, align='c', dx=0, dy=0, style='auto', ol=None, fill=None, bg=None,
           under=None, ol2=None, bold=0, clear=None, bgrow=None, grad=None):
    """img {(x, y): index} -> new dict with the English drawn in rect (frame pixels the OAM covers only).
    style auto/outline/shadow/none: the ring drawn in colour `ol` around the glyphs (auto: outline when the
    original's edge pixels share one colour not used inside). fill: one colour instead of the per-row fill.
    under: {(x, y): index} of a text-free frame, put back instead of the flat background (banner textures)."""
    W = max(x for x, _ in img) + 1
    H = max(y for _, y in img) + 1
    rx, ry, rw, rh = rect or (0, 0, W, H)
    area = {(x, y): v for (x, y), v in img.items() if rx <= x < rx + rw and ry <= y < ry + rh}
    border = [v for (x, y), v in area.items() if x in (rx, rx + rw - 1) or y in (ry, ry + rh - 1)]
    bg = bg if bg is not None else 0 if 0 in area.values() else _common(border)
    ink = {p for p, v in area.items() if v != bg}
    erase = set(area)
    if clear:  # text on a box: erase only these colours (+ a 1-px rim when there's an outline), keep the box
        ink = {p for p, v in area.items() if v in clear}
        erase = ink | ({(x + a, y + b) for x, y in ink for a in (-1, 0, 1) for b in (-1, 0, 1)} & area.keys()
                       if style != 'none' else set())
        style = 'none' if style == 'auto' and ol is None else style
    edge = {(x, y) for x, y in ink if any(area.get((x + a, y + b), bg) == bg
                                          for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
    inner = [area[p] for p in ink - edge]
    def side(d):  # colour of the ink pixels whose neighbours in directions d are background
        return _common([area[(x, y)] for x, y in ink if any(area.get((x + a, y + b), bg) == bg for a, b in d)])
    tl, br = side(((-1, 0), (0, -1))), side(((1, 0), (0, 1)))
    if ol is None:
        ol = _common([area[p] for p in edge])
        if style == 'auto':
            ok = ol is not None and inner and inner.count(ol) < 0.25 * len(inner) and \
                [area[p] for p in edge].count(ol) > 0.5 * len(edge)
            bev = tl != br and inner and inner.count(tl) + inner.count(br) < 0.25 * len(inner)
            style = 'bevel' if bev and not ok else 'outline' if ok else 'none'
    elif style == 'auto':
        style = 'outline'
    if ol2 is not None:
        br = ol2
    rings = [(RING['bevel_tl'], tl), (RING['bevel_br'], br)] if style == 'bevel' else [(RING[style], ol)]
    ring = [d for r, _ in rings for d in r]
    fill_rows = {}
    core = ink - edge
    for y in sorted({y for _, y in core}):
        r = [v for (x, yy), v in area.items() if yy == y and (x, yy) in core and v not in (ol, tl, br)]
        if r:
            fill_rows[y] = _common(r)
    gfill = fill if fill is not None else _common([v for v in inner if v != ol]) or \
        _common([v for p, v in area.items() if p in ink and v != ol]) or 15
    if fill is not None:
        fill_rows = {}
    tried = []
    for name in ([font] if font else ['big', 'mid', 'small']):
        try:
            m = FONTS[name](text) if name in FONTS else mask_ttf(text, int(name))  # font=39: Pixelify at 39 px
        except ValueError as e:
            tried.append('%s: %s' % (name, e))
            continue
        mask, ctop = m[0], m[1]
        capw = m[2] if len(m) > 2 else 7
        mw, mh = len(mask[0]) if mask and mask[0] else 0, len(mask)
        mw += 1 if bold and name != 'small' else 0  # placement width includes the bold column
        if align == 'l':
            ox = rx + 1 + (min(x for x, _ in ink) - rx - 1 if ink else 0)
        elif align == 'r' and ink and rect is None and not clear:  # end where the old text (+ its ring) ended
            ox = max(x for x, _ in ink) + 1 - mw - (1 if ring else 0)
        elif align == 'r':
            ox = (max(x for x, _ in ink) + 1 if clear and ink else rx + rw - 1) - mw
        else:
            ox = rx + (rw - mw) // 2
        ox = max(rx + (1 if ring else 0), min(ox, rx + rw - (1 if ring else 0) - mw)) + dx
        vy, vh = (min(y for _, y in ink), max(y for _, y in ink) - min(y for _, y in ink) + 1) if clear and ink \
            else (ry, rh)
        oy = vy + (vh - capw) // 2 - ctop + dy  # caps centred in the rect (clear: on the old text's rows)
        glyph = {(ox + x, oy + y) for y in range(mh) for x, v in enumerate(mask[y]) if v}
        if bold and name != 'small':  # 2-px stems like the Japanese art; a 1-px gap stays open
            glyph |= {(x + 1, y) for x, y in glyph if (x + 2, y) not in glyph and (x + 1, y) not in glyph}
        halo = {(x + a, y + b) for x, y in glyph for a, b in ring} - glyph
        halo = {(x, y) for x, y in halo if not ({(x - 1, y), (x + 1, y)} <= glyph or {(x, y - 1), (x, y + 1)} <= glyph)}
        if glyph <= area.keys() and halo <= area.keys():
            break
        tried.append('%s: %d px wide, %d off the tiles' % (name, mw, len((glyph | halo) - area.keys())))
    else:
        raise ValueError('%r does not fit %d,%d,%d,%d (%s)' % (text, rx, ry, rw, rh, '; '.join(tried)))
    out = dict(img)
    for x, y in erase:
        if under:
            out[(x, y)] = under.get((x, y), bg)
        elif bgrow is not None:  # text over a ball: the ball's colour from row bgrow of the same column
            out[(x, y)] = img.get((x, bgrow)) or bg
        elif clear:  # nearest kept pixel of the same row and column parity (dithers and gradients survive)
            out[(x, y)] = next((img[q] for d in range(2, 512, 2) for q in ((x - d, y), (x + d, y))
                                if q in area and q not in erase), bg)
        else:
            out[(x, y)] = bg
    t0, t1 = min(y for _, y in glyph), max(y for _, y in glyph)
    f0, f1 = (min(fill_rows), max(fill_rows)) if fill_rows else (t0, t1)
    for x, y in glyph:
        src = f0 + round((y - t0) * (f1 - f0) / max(1, t1 - t0))
        out[(x, y)] = grad[(y - t0) * len(grad) // (t1 - t0 + 1)] if grad else fill_rows.get(src, gfill)
    for r, c in rings:  # bevel: the bottom-right colour wins where both reach
        for p in halo & {(x + a, y + b) for x, y in glyph for a, b in r}:
            out[p] = c
    LAST.update(text=text, font=name, style=style, bg=bg, ring=[c for _, c in rings],
                fill=sorted(set(fill_rows.values())) or [gfill])
    return out


LAST = {}  # what the last letter() call chose (preview prints it)


def spec(bank):
    p = ROOT / 'gfx' / (bank + '.tsv')
    rows = []
    for ln in p.read_text(encoding='utf-8').splitlines() if p.exists() else []:
        if not ln.strip() or ln.startswith('#'):
            continue
        fr, text, *opt = ln.split('\t')
        a, _, b = fr.partition('-')
        o = dict(kv.split('=', 1) for kv in (opt[0].split() if opt else []))
        kw = {'rect': tuple(map(int, o.pop('rect').split(','))) if 'rect' in o else None, 'font': o.pop('font', None),
              'style': o.pop('style', 'auto')}
        if 'align' in o:
            kw['align'] = o.pop('align')
        if 'keep' in o:
            kw['keep'] = o.pop('keep')
        if 'clear' in o:
            kw['clear'] = {int(v) for v in o.pop('clear').split(',')}
            kw.setdefault('align', 'l')  # text on a box starts where the Japanese did
        for k in ('grad', 'bgrep'):
            if k in o:
                kw[k] = [int(v) for v in o.pop(k).split(',')]
        kw.update({k: int(v) for k, v in o.items()})  # dx dy ol ol2 fill bg w bgfrom
        for f in range(int(a), int(b or a) + 1):
            rows.append((f, text, kw))
    return rows


def apply(name, b, errors=None, log=None):
    """NCD bytes with every spec row of its bank lettered (unchanged when the bank has no spec).
    errors: a list to collect rows that don't fit instead of raising; log: gets (frame, what letter() chose)."""
    rows = spec(name.split('.')[0])
    if not rows:
        return b
    n = NCD(b)
    orig = NCD(b)
    imgs = {}
    for f, text, kw in rows:
        kw = dict(kw)
        if f not in imgs:  # fresh tiles always: frames reuse blank tiles and overlap objects
            imgs[f] = n.relayout(f, kw.get('wr') or kw.get('wl') or kw.get('w'),
                                 'l' if 'wr' in kw else 'r' if 'wl' in kw else 'c')
        for k in ('w', 'wr', 'wl'):
            kw.pop(k, None)
        if kw.get('rect'):  # rect is in the original frame's pixels
            x, y, w, h = kw['rect']
            kw['rect'] = (x - n.shift[f], y, w, h)
        if 'bgrep' in kw:  # background = the frame's own text-free columns x..x+w-1 repeated (patterned bars)
            x0, w = kw.pop('bgrep')
            x0 -= n.shift[f]
            kw['under'] = {(x, y): imgs[f].get((x0 + (x - x0) % w, y), 0) for x, y in imgs[f]}
        if 'bgfrom' in kw:  # same bbox as f: move it like f was moved
            u, s = orig.get(kw.pop('bgfrom')), n.shift[f]
            kw['under'] = {(x, y): u.get((x + s, y), 0) for x, y in imgs[f]}
        if 'keep' in kw:  # leave the last N glyphs (floor 'B F', where the game draws the digit) and letter left of them
            img = imgs[f]
            cols = sorted({x for (x, y), v in img.items() if v})
            runs = [[cols[0]]]
            for x in cols[1:]:
                runs.append([x]) if x > runs[-1][-1] + 1 else runs[-1].append(x)
            # keep=f: the last glyph; keep=bf: also the 13-px B 3 px before it (B touches ス in some frames)
            x = runs[-1][0] - (16 if kw.pop('keep') == 'bf' else 0)
            kw['rect'] = (0, 0, x - 2, max(y for _, y in img) + 1)
            kw.setdefault('align', 'r')
        try:
            imgs[f] = letter(imgs[f], text, **kw)
        except ValueError as e:
            if errors is None:
                raise
            errors.append('%04d: %s' % (f, e))
            continue
        if log is not None:
            log.append((f, dict(LAST)))
    for f, img in imgs.items():
        n.put(f, img)
    return bytes(n.b)


def shared(bank, n):
    """{frame: tiles shared with a frame outside the spec whose pixels would change}"""
    frames = {f for f, _, _ in spec(bank)}
    use = {}
    for f in range(n.nframes):
        if n.objs(f):
            for t in n.tiles(f):
                use.setdefault(t, set()).add(f)
    return {f: sorted(t for t in n.tiles(f) if use[t] - frames) for f in sorted(frames)}


def _bank(bank):
    import nfp
    rom = nfp.ROM
    data = dict(nfp.unpack(open(rom, 'rb').read()))
    return data[bank + '.NCD']


def preview(bank, frames):
    from PIL import Image
    b = _bank(bank)
    errs, log = [], []
    n, new = NCD(b), NCD(apply(bank + '.NCD', b, errs, log))
    for f, x in log:
        if f in frames:
            print('%04d %-18s %-5s %-7s bg %s ring %s fill %s' % (f, x['text'][:18], x['font'], x['style'], x['bg'],
                                                                 x['ring'], x['fill']))
    print('\n'.join(errs))
    out = ROOT / 'work' / 'gfx' / 'en' / bank
    out.mkdir(parents=True, exist_ok=True)
    for f in frames:
        pal, a, c = n.palette(f), n.get(f), new.get(f)
        W, H = max(x for x, _ in a) + 1, max(y for _, y in list(a) + list(c)) + 1
        img = Image.new('RGB', (W + 4 + max(x for x, _ in c) + 1, H), (64, 0, 64))
        for (x, y), v in a.items():
            if v:
                img.putpixel((x, y), pal[v])
        for (x, y), v in c.items():
            if v:
                img.putpixel((W + 4 + x, y), pal[v])
        img.resize((img.width * 3, img.height * 3), Image.NEAREST).save(out / ('f%04d.png' % f))
    print(out)  # read with: sheet.py work/gfx/en/<BANK> --div 1 --from N --to M


def frange(args):
    out = []
    for a in args:
        x, _, y = a.partition('-')
        out += range(int(x), int(y or x) + 1)
    return out


if __name__ == '__main__':
    cmd, bank = sys.argv[1], sys.argv[2]
    if cmd == 'preview':
        preview(bank, frange(sys.argv[3:]) or sorted({f for f, _, _ in spec(bank)}))
    elif cmd == 'check':  # every spec row fits (tests/test_gfxtext.py)
        errs = []
        apply(bank + '.NCD', _bank(bank), errs)
        print('\n'.join(errs) or '%s: OK' % bank)
        sys.exit(1 if errs else 0)
    elif cmd == 'colors':  # index: RGB, pixel count, per frame
        n = NCD(_bank(bank))
        for f in frange(sys.argv[3:]):
            v, pal = list(n.get(f).values()), n.palette(f)
            print('%04d' % f, ' '.join('%d:%02x%02x%02x*%d' % (i, *pal[i], v.count(i)) for i in sorted(set(v))))
    elif cmd == 'shared':
        for f, t in shared(bank, NCD(_bank(bank))).items():
            if t:
                print('%04d shares %s' % (f, t))
