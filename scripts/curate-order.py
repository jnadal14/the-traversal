#!/usr/bin/env python3
"""Re-sequence the mosaic for visual variety.

Run this after adding work, when the running order needs rebalancing:

    python3 scripts/curate-order.py            # propose an order, print it
    python3 scripts/curate-order.py --write    # rewrite gallery-manifest.js

WHY THIS EXISTS

The grid is CSS `column-count`, which fills COLUMN-major. With 70 tiles over 3
columns the browser puts items 0-21 in the first column, 22-45 in the second and
46-69 in the third, balancing on height. Two consequences follow, and both are
counter-intuitive enough to be worth stating:

  * Neighbours are not what the manifest order suggests. Item 1 sits *below*
    item 0; the tile beside item 0 is item ~22.
  * The first screenful is the top of every column at once. Sequencing by hand
    therefore cannot control the opening impression at all.

So this does not guess. It measures each photograph (mean CIELAB colour, tonal
range, saturation, hue, aspect), reproduces the browser's balanced fill at every
breakpoint the stylesheet defines, derives the true neighbour pairs from that
geometry, and anneals the order to maximise contrast across all of them at once.

What it optimises for, in order of weight:
  - no two similar tiles touching, at any breakpoint (colour, tone, hue, shape)
  - the worst adjacency, not just the average — one dull pair is what the eye finds
  - films spread evenly through the run, never bunched
  - the tops of the columns differing strongly from one another, since together
    they are the entire first impression
"""
import json, math, os, random, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
MANIFEST = 'gallery-manifest.js'

# (columns, typical grid width) — must track the @media rules in mosaic.html
BREAKPOINTS = [(2, 900), (3, 1264), (4, 1800)]
GAP = 8
SEED = 7

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required:  python3 -m pip install Pillow")


def to_lab(rgb):
    def inv(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (inv(v) for v in rgb)
    X = r * .4124 + g * .3576 + b * .1805
    Y = r * .2126 + g * .7152 + b * .0722
    Z = r * .0193 + g * .1192 + b * .9505
    def f(t): return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(X / .95047), f(Y / 1.0), f(Z / 1.08883)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def measure():
    """Read the manifest, then sample every tile's colour and shape."""
    import colorsys
    man = open(MANIFEST, encoding='utf-8').read()
    entries = [(k, p) for k, p in re.findall(r"(image|video)\('(assets/[^']+)'", man)
               if 'name.' not in p]
    tiles = []
    for kind, path in entries:
        # A film is represented by its poster, which is its own first frame.
        src = path if kind == 'image' else (
            path.replace('assets/video/', 'assets/posters/').replace('.mp4', '.jpg'))
        with Image.open(src) as im:
            small = im.convert('RGB').resize((64, 64), Image.LANCZOS)
        if kind == 'image':
            with Image.open(path) as im:
                w, h = im.size
        else:
            out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                                  '-show_entries', 'stream=width,height',
                                  '-of', 'csv=p=0:s=x', path],
                                 capture_output=True, text=True).stdout.strip()
            w, h = (int(x) for x in out.split('x'))
        px = list(small.getdata()); n = len(px)
        mean = tuple(sum(p[i] for p in px) / n for i in range(3))
        L, A, B = to_lab(mean)
        hsv = [colorsys.rgb_to_hsv(*(c / 255 for c in p)) for p in px]
        sat = sum(s for _, s, _ in hsv) / n
        sx = sum(math.cos(2 * math.pi * hh) * ss for hh, ss, _ in hsv)
        sy = sum(math.sin(2 * math.pi * hh) * ss for hh, ss, _ in hsv)
        tiles.append(dict(kind=kind, path=path, w=w, h=h, ar=w / h,
                          L=L, A=A, B=B, sat=sat,
                          hue=math.degrees(math.atan2(sy, sx)) % 360))
    return tiles


def hue_gap(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


def build(tiles):
    N = len(tiles)

    def dissim(x, y):
        dE = math.dist((x['L'], x['A'], x['B']), (y['L'], y['A'], y['B']))
        s = (dE / 40) * 1.0 + (abs(x['L'] - y['L']) / 40) * 0.9 \
            + (hue_gap(x['hue'], y['hue']) / 180) * 0.8 \
            + abs(x['sat'] - y['sat']) * 0.6 \
            + min(abs(math.log(x['ar']) - math.log(y['ar'])), 1.2) * 1.1
        if x['kind'] == y['kind'] == 'video':
            s -= 2.5          # two films touching reads as a cluster regardless
        return s

    def layout(order, cols, width):
        colw = (width - GAP * (cols - 1)) / cols
        heights = [colw / tiles[i]['ar'] + GAP for i in order]
        target = sum(heights) / cols
        runs, cur, acc = [], [], 0.0
        for pos, h in enumerate(heights):
            cur.append(pos); acc += h
            if acc >= target and len(runs) < cols - 1:
                runs.append(cur); cur, acc = [], 0.0
        runs.append(cur)
        while len(runs) < cols:
            runs.append([])
        spans = []
        for run in runs:
            y, col = 0.0, []
            for pos in run:
                col.append((pos, y, y + heights[pos])); y += heights[pos]
            spans.append(col)
        pairs = []
        for col in spans:
            for k in range(len(col) - 1):
                pairs.append((col[k][0], col[k + 1][0], 1.0))
        for c in range(len(spans) - 1):
            for pos, y0, y1 in spans[c]:
                for pos2, z0, z1 in spans[c + 1]:
                    ov = min(y1, z1) - max(y0, z0)
                    if ov > 0:
                        pairs.append((pos, pos2, 0.75 * min(1.0, ov / (y1 - y0))))
        return pairs, [col[0][0] for col in spans if col]

    def score(order):
        total = 0.0
        for cols, width in BREAKPOINTS:
            pairs, tops = layout(order, cols, width)
            for a, b, w in pairs:
                d = dissim(tiles[order[a]], tiles[order[b]])
                total += w * d
                if d < 1.2:                       # punish the worst pairs hardest
                    total -= 3.0 * (1.2 - d) ** 2
            for i, t_i in enumerate(tops):
                t = tiles[order[t_i]]
                total += 2.0 * (t['sat'] + abs(t['L'] - 35) / 50)
                for t_j in tops[i + 1:]:
                    total += 3.0 * dissim(t, tiles[order[t_j]])
        vids = sorted(i for i, p in enumerate(order) if tiles[p]['kind'] == 'video')
        if len(vids) > 1:
            gaps = [vids[k + 1] - vids[k] for k in range(len(vids) - 1)]
            ideal = N / len(vids)
            total -= 1.4 * sum(abs(g - ideal) for g in gaps)
            total -= 6.0 * sum(max(0, 4 - g) ** 2 for g in gaps)
            total -= 0.8 * abs(vids[0] - ideal / 2)
            total -= 0.8 * abs((N - 1 - vids[-1]) - ideal / 2)
        return total

    return dissim, layout, score


def main():
    random.seed(SEED)
    tiles = measure()
    N = len(tiles)
    dissim, layout, score = build(tiles)

    order = list(range(N)); random.shuffle(order)
    best = cur = order[:]
    best_s = cur_s = score(order)
    T0, T1, STEPS = 3.0, 0.015, 220000
    for step in range(STEPS):
        T = T0 * (T1 / T0) ** (step / STEPS)
        a, b = random.randrange(N), random.randrange(N)
        if a == b:
            continue
        cand = cur[:]
        if random.random() < 0.75:
            cand[a], cand[b] = cand[b], cand[a]
        else:
            lo, hi = min(a, b), max(a, b)
            cand[lo:hi + 1] = reversed(cand[lo:hi + 1])
        s = score(cand)
        if s > cur_s or random.random() < math.exp((s - cur_s) / max(T, 1e-6)):
            cur, cur_s = cand, s
            if s > best_s:
                best, best_s = cand[:], s

    print(f"score {best_s:.1f}\n")
    for cols, width in BREAKPOINTS:
        pairs, tops = layout(best, cols, width)
        vals = [dissim(tiles[best[a]], tiles[best[b]]) for a, b, _ in pairs]
        print(f"  {cols} columns: {len(pairs)} adjacencies, "
              f"mean contrast {sum(vals)/len(vals):.2f}, worst {min(vals):.2f}")
        print("     opens with " + ", ".join(
            os.path.basename(tiles[best[t]]['path']) for t in tops))
    vids = [i for i, p in enumerate(best) if tiles[p]['kind'] == 'video']
    print(f"\n  films at {vids}")
    print(f"  gaps      {[vids[k+1]-vids[k] for k in range(len(vids)-1)]}"
          f"   (ideal {N/len(vids):.1f})")

    lines = []
    for i in best:
        t = tiles[i]
        fn = 'image' if t['kind'] == 'image' else 'video'
        lines.append(f"        {fn}('{t['path']}', {t['w']}, {t['h']}),")
    body = "\n".join(lines)

    if '--write' in sys.argv:
        s = open(MANIFEST, encoding='utf-8').read()
        a = s.index('    return [')
        b = s.index('    ];', a)
        open(MANIFEST, 'w', encoding='utf-8').write(
            s[:a] + "    return [\n" + body + "\n" + s[b:])
        print(f"\n  wrote {len(best)} entries to {MANIFEST}")
    else:
        print("\n  (--write to apply)\n")
        print(body)


if __name__ == '__main__':
    main()
