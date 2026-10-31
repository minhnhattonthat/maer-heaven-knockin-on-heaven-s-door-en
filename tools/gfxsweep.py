"""Static graphics sweep for the graphics-text survey (docs/re/graphics.md).

    python -X utf8 tools/gfxsweep.py OUTDIR

Renders from MAR.NFP (needs `tools/nfp.py extract work/nfp` first):
- every *.KMP background (with the KCG tiles and KCL palette its header names) -> OUTDIR/bg/<name>.png
- every *.TCG/*.KCG tile set without a map, as a 16-wide tile sheet -> OUTDIR/tiles/<name>.png
- every sprite frame of the three NCD sprite banks -> OUTDIR/ncd/<bank>_<frame>.png
and prints every file it skipped, with the reason. Then build contact sheets with $SKILL/scripts/sheet.py.
"""
import os
import struct
import sys

from PIL import Image

SRC = 'work/nfp'


def pal(raw, n=16):
    cols = []
    for i in range(0, min(len(raw), n * 2 * 16), 2):
        v = struct.unpack_from('<H', raw, i)[0]
        cols.append(((v & 31) * 255 // 31, (v >> 5 & 31) * 255 // 31, (v >> 10 & 31) * 255 // 31))
    return cols


GREY = [(i * 17, i * 17, i * 17) for i in range(16)]


def tile4(data, t):
    o = t * 32
    px = []
    for y in range(8):
        row = []
        for x in range(4):
            b = data[o + y * 4 + x] if o + y * 4 + x < len(data) else 0
            row += [b & 15, b >> 4]
        px.append(row)
    return px


def put(img, data, t, x0, y0, colors, base, hf=False, vf=False, transparent=True):
    px = tile4(data, t)
    for y in range(8):
        for x in range(8):
            c = px[7 - y if vf else y][7 - x if hf else x]
            if c == 0 and transparent:
                continue
            col = colors[base + c] if base + c < len(colors) else GREY[c]
            xx, yy = x0 + x, y0 + y
            if 0 <= xx < img.width and 0 <= yy < img.height:
                img.putpixel((xx, yy), col)


def load(name):
    p = os.path.join(SRC, name)
    if os.path.exists(p):  # decompressed copy
        return open(p, 'rb').read()
    p = os.path.join(SRC, name + '.bin')
    return open(p, 'rb').read() if os.path.exists(p) else None


def render_bgs(out, skipped):
    used = set()
    os.makedirs(os.path.join(out, 'bg'), exist_ok=True)
    for f in sorted(os.listdir(SRC)):
        if not f.endswith('.KMP.bin'):
            continue
        b = open(os.path.join(SRC, f), 'rb').read()
        w, h = struct.unpack_from('<II', b, 0x14)
        kcg = b[0x1c:0x5c].split(b'\0')[0].decode('ascii', 'replace')
        kcl = b[0x5c:0x9c].split(b'\0')[0].decode('ascii', 'replace')
        tiles, colors = load(kcg), load(kcl)
        if tiles is None or w * h == 0:
            skipped.append((f, 'missing tiles %s or empty map' % kcg))
            continue
        used.add(kcg)
        used.add(kcl)
        colors = pal(colors) if colors else GREY
        layers = (len(b) - 0xc0) // (w * h * 2)
        if layers < 1:
            skipped.append((f, 'map shorter than %dx%d' % (w, h)))
            continue
        img = Image.new('RGB', (w * 8, h * 8 * layers), (40, 0, 40))
        for L in range(layers):
            for i in range(w * h):
                e = struct.unpack_from('<H', b, 0xc0 + L * w * h * 2 + i * 2)[0]
                put(img, tiles, e & 0x3ff, (i % w) * 8, (i // w) * 8 + L * h * 8, colors, (e >> 12) * 16,
                    bool(e & 0x400), bool(e & 0x800), transparent=False)
        if img.width > 512 or img.height > 512:
            img.thumbnail((512, 512 * layers))
        img.save(os.path.join(out, 'bg', f[:-8] + '.png'))
    return used


def render_tilesets(out, used, skipped):
    os.makedirs(os.path.join(out, 'tiles'), exist_ok=True)
    for f in sorted(os.listdir(SRC)):
        if not (f.endswith('.TCG') or f.endswith('.KCG')) or f in used:
            continue
        data = open(os.path.join(SRC, f), 'rb').read()
        n = len(data) // 32
        clr = load(f[:-4] + ('.TCL' if f.endswith('.TCG') else '.KCL'))
        colors = pal(clr) if clr else GREY
        cols = 32
        img = Image.new('RGB', (cols * 8, ((n + cols - 1) // cols) * 8), (40, 0, 40))
        for t in range(n):
            put(img, data, t, (t % cols) * 8, (t // cols) * 8, colors, 0, transparent=False)
        img.save(os.path.join(out, 'tiles', f + '.png'))
    for f in sorted(os.listdir(SRC)):
        if f.endswith(('.TCG.bin', '.KCG.bin')) and not os.path.exists(os.path.join(SRC, f[:-4])):
            skipped.append((f, 'LZ77 decode failed'))


SHAPES = {(0, 0): (8, 8), (0, 1): (16, 16), (0, 2): (32, 32), (0, 3): (64, 64),
          (1, 0): (16, 8), (1, 1): (32, 8), (1, 2): (32, 16), (1, 3): (64, 32),
          (2, 0): (8, 16), (2, 1): (8, 32), (2, 2): (16, 32), (2, 3): (32, 64)}


def render_ncd(out, name, skipped):
    b = load(name)
    os.makedirs(os.path.join(out, 'ncd'), exist_ok=True)
    offs = struct.unpack_from('<6I', b, 0x20)
    cnt = struct.unpack_from('<8I', b, 0x40)
    _, anim_o, frame_o, oam_o, pal_o, tile_o = offs
    nframes, noam, npal = cnt[2], cnt[3], cnt[5]
    tiles = b[tile_o:]
    colors_all = pal(b[pal_o:pal_o + npal * 32], npal)
    tag = name.split('.')[0]
    for fr in range(nframes):
        first, count = struct.unpack_from('<IH', b, frame_o + 8 * fr)
        objs = []
        for k in range(first, first + count):
            if k >= noam:
                skipped.append(('%s frame %d' % (name, fr), 'oam index %d out of range' % k))
                break
            e = b[oam_o + 20 * k:oam_o + 20 * k + 20]
            a0, a1 = struct.unpack_from('<HH', e)
            p, t = struct.unpack_from('<II', e, 4)
            y = a0 & 0xff
            y = y - 256 if y >= 128 else y
            x = a1 & 0x1ff
            x = x - 512 if x >= 256 else x
            wh = SHAPES.get((a0 >> 14, a1 >> 14))
            if wh is None:
                continue
            objs.append((x, y, wh, t, p, bool(a1 & 0x1000), bool(a1 & 0x2000)))
        if not objs:
            continue
        x0 = min(o[0] for o in objs)
        y0 = min(o[1] for o in objs)
        x1 = max(o[0] + o[2][0] for o in objs)
        y1 = max(o[1] + o[2][1] for o in objs)
        if x1 - x0 > 512 or y1 - y0 > 512:
            skipped.append(('%s frame %d' % (name, fr), 'bbox too large'))
            continue
        img = Image.new('RGB', (x1 - x0, y1 - y0), (40, 0, 40))
        for x, y, (w, h), t, p, hf, vf in objs:
            colors = colors_all[p * 16:p * 16 + 16] if p < npal else GREY
            tw, th = w // 8, h // 8
            for ty in range(th):
                for tx in range(tw):
                    sx = (tw - 1 - tx) if hf else tx
                    sy = (th - 1 - ty) if vf else ty
                    put(img, tiles, t + sy * tw + sx, x - x0 + tx * 8, y - y0 + ty * 8, colors, 0, hf, vf)
        img.save(os.path.join(out, 'ncd', '%s_%04d.png' % (tag, fr)))


def pack(src_dir, prefix, out_dir, page=(1400, 1000), zoom=2):
    """Pack variable-size PNGs (deduplicated) into labelled pages; returns the page count."""
    import hashlib
    from PIL import ImageDraw
    os.makedirs(out_dir, exist_ok=True)
    seen, items = set(), []
    for f in sorted(os.listdir(src_dir)):
        if not f.startswith(prefix) or not f.endswith('.png'):
            continue
        im = Image.open(os.path.join(src_dir, f)).convert('RGB')
        h = hashlib.md5(im.tobytes() + bytes(str(im.size), 'ascii')).hexdigest()
        if h in seen:
            continue
        seen.add(h)
        items.append((f[:-4], im.resize((im.width * zoom, im.height * zoom), Image.NEAREST)))
    pages, cur, x, y, rowh = [], None, 0, 0, 0
    for label, im in items:
        w, h = min(im.width, page[0]), min(im.height, page[1] - 12)
        if cur is None or x + w > page[0]:
            x, y, rowh = 0, y + rowh + 12, 0
        if cur is None or y + h + 12 > page[1]:
            cur = Image.new('RGB', page, (255, 255, 255))
            pages.append(cur)
            x, y, rowh = 0, 0, 0
        cur.paste(im.crop((0, 0, w, h)), (x, y + 12))
        ImageDraw.Draw(cur).text((x, y), label.split('_')[-1] if prefix else label, fill=(255, 0, 0))
        x += w + 6
        rowh = max(rowh, h)
    for i, p in enumerate(pages):
        p.save(os.path.join(out_dir, '%s_p%02d.png' % (prefix.rstrip('_') or 'all', i + 1)))
    return len(pages)


def main(out):
    skipped = []
    used = render_bgs(out, skipped)
    render_tilesets(out, used, skipped)
    for n in ('SYSTEM.NCD', 'CHR.NCD', 'EFFECT.NCD'):
        render_ncd(out, n, skipped)
    for f, why in skipped:
        print('skipped', f, '-', why)
    pages(out)


def pages(out):
    for pre in ('SYSTEM_', 'CHR_', 'EFFECT_'):
        print(pre, pack(os.path.join(out, 'ncd'), pre, os.path.join(out, 'pages')), 'pages')
    print('bg', pack(os.path.join(out, 'bg'), '', os.path.join(out, 'pages_bg'), zoom=1), 'pages')
    print('tiles', pack(os.path.join(out, 'tiles'), '', os.path.join(out, 'pages_tiles'), zoom=2), 'pages')


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[2] == 'pages':
        pages(sys.argv[1])
    else:
        main(sys.argv[1] if len(sys.argv) > 1 else 'work/gfx')
