"""
Shared helpers for the README asset generator  ·  tema CARMESIM / JAPONÊS.

Por que isso existe: o GitHub mostra SVGs via <img>, que bloqueia fontes externas.
Então toda fonte usada é recortada (só os glifos usados) e embutida em base64 dentro
de cada SVG. É isso que deixa a tipografia igual para todo mundo, em qualquer aparelho.
"""
import base64, io, math, os, random
from fontTools.ttLib import TTFont
from fontTools import subset

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")

# ---------------------------------------------------------------- palette (crimson)
HOT = ("#1d0409", "#3a0a15", "#650f1f")   # painel de destaque (hero / sobre nós); troque por tons mais claros se quiser mais vermelho

P = dict(
    bg0="#1d0409", bg1="#3a0a15", bg2="#650f1f", bg3="#8c1428",
    r="#dc143c", rb="#ff3b57", rd="#8a0f24", rk="#2a0509",
    w="#fff3ef", g1="#ffd6d6", g2="#f2a7ad", g3="#d98791", g4="#b0606c", g5="#7a2c38", g6="#4e1620",
    au="#f0c27b", pk="#ffc2cc",
)

# ---------------------------------------------------------------- fonts
FONTS = {
    "display": dict(family="MR Display", fallback="'Helvetica Neue',Arial,sans-serif",
                    files={400: "Outfit-Regular.ttf", 700: "Outfit-Bold.ttf"}),
    "sans":    dict(family="MR Sans", fallback="'Helvetica Neue',Arial,sans-serif",
                    files={500: "Inter-Medium.otf", 600: "Inter-SemiBold.otf"}),
    "mono":    dict(family="MR Mono", fallback="'SF Mono',Consolas,monospace",
                    files={400: "JetBrainsMono-Regular.ttf", 700: "JetBrainsMono-Bold.ttf"}),
    "kanji":   dict(family="MR Kanji", fallback="'Hiragino Mincho ProN','Yu Mincho',serif",
                    files={700: "kanji-subset.otf"}),
}
_font_cache = {}


def _load(key, weight):
    k = (key, weight)
    if k not in _font_cache:
        _font_cache[k] = TTFont(os.path.join(FONT_DIR, FONTS[key]["files"][weight]))
    return _font_cache[k]


def fam(key):
    f = FONTS[key]
    return f"'{f['family']}',{f['fallback']}"


def measure(key, weight, text, size, track=0.0):
    """Width in px of `text` (no kerning; fine for centering)."""
    f = _load(key, weight)
    cmap, hmtx, upm = f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
    w = 0.0
    for ch in text:
        g = cmap.get(ord(ch))
        w += (hmtx[g][0] if g else upm * 0.55) * size / upm
        w += track
    return w - track if text else 0.0


def font_face(key, weight, chars):
    f = TTFont(os.path.join(FONT_DIR, FONTS[key]["files"][weight]))
    o = subset.Options()
    o.flavor = "woff"
    o.layout_features = ["kern", "liga", "calt"]
    o.notdef_outline = True
    s = subset.Subsetter(o)
    s.populate(text="".join(sorted(chars)) + " ")
    s.subset(f)
    buf = io.BytesIO()
    f.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return (f"@font-face{{font-family:'{FONTS[key]['family']}';font-weight:{weight};"
            f"src:url(data:font/woff;base64,{b64}) format('woff')}}")


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- icons
# 24x24, stroke based. Add your own: ICONS["name"] = "<path d='...'/>"
ICONS = {
    "code": "<path d='M16 18l6-6-6-6M8 6l-6 6 6 6'/>",
    "terminal": "<path d='M4 17l6-6-6-6M12 19h8'/>",
    "user": "<circle cx='12' cy='8' r='4'/><path d='M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7'/>",
    "users": "<circle cx='9' cy='8' r='3.5'/><path d='M2.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6'/><circle cx='17' cy='9' r='2.6'/><path d='M17 14c3 0 5 1.8 5 5'/>",
    "activity": "<path d='M22 12h-4l-3 9L9 3l-3 9H2'/>",
    "coffee": "<path d='M4 9h12v6a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4z'/><path d='M16 11h2a2.5 2.5 0 0 1 0 5h-2'/><path d='M8 3v3M12 3v3'/>",
    "gamepad": "<path d='M7 8h10a5 5 0 0 1 5 5v1.5a2.5 2.5 0 0 1-4.4 1.6L16 14.5a2 2 0 0 0-1.5-.7h-5a2 2 0 0 0-1.5.7l-1.6 1.6A2.5 2.5 0 0 1 2 14.5V13a5 5 0 0 1 5-5z'/><path d='M7.5 11v3M6 12.5h3'/><circle cx='16' cy='11.2' r='.6'/><circle cx='18' cy='13.2' r='.6'/>",
    "film": "<rect x='3' y='3' width='18' height='18' rx='2'/><path d='M7 3v18M17 3v18M3 8h4M3 12h4M3 16h4M17 8h4M17 12h4M17 16h4'/>",
    "cap": "<path d='M2 9l10-5 10 5-10 5z'/><path d='M6 11.5V16c0 1.4 2.7 3 6 3s6-1.6 6-3v-4.5M22 9v6'/>",
    "cube": "<path d='M12 2.5l8.5 4.8v9.4L12 21.5l-8.5-4.8V7.3z'/><path d='M12 12l8.5-4.7M12 12v9.5M12 12L3.5 7.3'/>",
    "globe": "<circle cx='12' cy='12' r='9'/><path d='M3 12h18'/><path d='M12 3c2.6 2.6 4 5.6 4 9s-1.4 6.4-4 9c-2.6-2.6-4-5.6-4-9s1.4-6.4 4-9z'/>",
    "database": "<ellipse cx='12' cy='5.5' rx='8' ry='3'/><path d='M4 5.5v13c0 1.7 3.6 3 8 3s8-1.3 8-3v-13M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3'/>",
    "server": "<rect x='3' y='3' width='18' height='7' rx='2'/><rect x='3' y='14' width='18' height='7' rx='2'/><circle cx='7' cy='6.5' r='.6'/><circle cx='7' cy='17.5' r='.6'/>",
    "monitor": "<rect x='2.5' y='4' width='19' height='12' rx='2'/><path d='M8 21h8M12 16v5'/>",
    "heart": "<path d='M12 20.5s-8-4.8-8-10.8A4.4 4.4 0 0 1 12 7a4.4 4.4 0 0 1 8 2.7c0 6-8 10.8-8 10.8z'/>",
    "spark": "<path d='M12 2.5l2.2 7.3L21.5 12l-7.3 2.2L12 21.5l-2.2-7.3L2.5 12l7.3-2.2z'/>",
    "pen": "<path d='M12 20h9'/><path d='M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z'/>",
    "drop": "<path d='M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z'/>",
    "camera": "<rect x='3' y='3' width='18' height='18' rx='5.5'/><circle cx='12' cy='12' r='4.2'/><circle cx='17.4' cy='6.6' r='.7'/>",
    "chat": "<path d='M21 11.5a8.5 8.5 0 0 1-12.4 7.5L3 20.5l1.6-5A8.5 8.5 0 1 1 21 11.5z'/><path d='M8.5 11.5h.01M12 11.5h.01M15.5 11.5h.01'/>",
    "send": "<path d='M22 2L11 13M22 2l-7 20-4-9-9-4z'/>",
    "shield": "<path d='M12 3l8 3v6c0 4.5-3.4 7.8-8 9-4.6-1.2-8-4.5-8-9V6z'/><path d='M8.5 12l2.5 2.5 4.5-5'/>",
    "lock": "<rect x='5' y='11' width='14' height='9' rx='2'/><path d='M8 11V8a4 4 0 0 1 8 0v3'/>",
    "book": "<path d='M4 4.5A2.5 2.5 0 0 1 6.5 2H20v17H6.5A2.5 2.5 0 0 0 4 21.5z'/><path d='M4 21.5V4.5'/>",
    "flame": "<path d='M12 3c1 3.5 5 5.5 5 10a5 5 0 0 1-10 0c0-2 1-3 2-4 .3 1.5 1 2 2 2 0-3-1-5 1-8z'/>",
    "branch": "<circle cx='6' cy='5.5' r='2.4'/><circle cx='6' cy='18.5' r='2.4'/><circle cx='18' cy='9' r='2.4'/><path d='M6 8v8M18 11.4c0 4-9 2.6-11.2 6.2'/>",
    "phone": "<rect x='6.5' y='2.5' width='11' height='19' rx='2.6'/><path d='M11 18.5h2'/>",
}


def icon(name, cx, cy, size=22, color=P["g2"], sw=1.6, extra="", fill="none"):
    s = size / 24
    return (f"<g transform='translate({cx - size / 2:.1f} {cy - size / 2:.1f}) scale({s:.4f})' fill='{fill}' "
            f"stroke='{color}' stroke-width='{sw / s:.2f}' stroke-linecap='round' stroke-linejoin='round' {extra}>"
            f"{ICONS[name]}</g>")


# ---------------------------------------------------------------- japanese motifs (pure functions -> svg strings)
PETAL = "M0 0C-5.5-3-6.5-10.5-2.4-13.2L0-11L2.4-13.2C6.5-10.5 5.5-3 0 0Z"


def petals(n, seed, x0, x1, y0, y1, size=1.0, colors=None, dur=(9, 16), fall=None, sway=46):
    """Sakura petals drifting down (SMIL). Negative `begin` => already mid-air on load."""
    colors = colors or ["#ffc2cc", "#ff8fa3", "#ffd9df", "#ff6b82"]
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x = rnd.uniform(x0, x1)
        fall_ = fall or (y1 - y0)
        d = rnd.uniform(*dur)
        dx = rnd.uniform(-70, 90)
        sw = rnd.choice([-1, 1]) * rnd.uniform(.6, 1) * sway
        sc = rnd.uniform(.55, 1.15) * size
        col = rnd.choice(colors)
        b = -rnd.uniform(0, d)
        rot0 = rnd.uniform(0, 360)
        path = (f"M{x:.0f} {y0} C{x + sw:.0f} {y0 + fall_ * .3:.0f} {x - sw:.0f} {y0 + fall_ * .65:.0f} {x + dx:.0f} {y0 + fall_:.0f}")
        out.append(
            f"<g opacity='0'><animateMotion path='{path}' dur='{d:.1f}s' begin='{b:.1f}s' repeatCount='indefinite'/>"
            f"<animate attributeName='opacity' values='0;.9;.9;0' keyTimes='0;.12;.85;1' dur='{d:.1f}s' begin='{b:.1f}s' repeatCount='indefinite'/>"
            f"<g><animateTransform attributeName='transform' type='rotate' from='{rot0:.0f}' to='{rot0 + rnd.choice([-1, 1]) * 360:.0f}' "
            f"dur='{rnd.uniform(4, 8):.1f}s' repeatCount='indefinite'/>"
            f"<path d='{PETAL}' transform='scale({sc:.2f})' fill='{col}'/></g></g>")
    return "".join(out)


def embers(n, seed, x0, x1, y0, y1, colors=None, dur=(5, 10)):
    """Small glowing sparks rising up."""
    colors = colors or ["#ff3b57", "#ff7a5c", "#ffb3b9", "#ff2a3a"]
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        d = rnd.uniform(*dur)
        b = -rnd.uniform(0, d)
        rise = rnd.uniform(60, 150)
        drift = rnd.uniform(-30, 30)
        r = rnd.choice([.9, 1.2, 1.6, 2.1])
        c = rnd.choice(colors)
        out.append(
            f"<circle cx='{x:.0f}' cy='{y:.0f}' r='{r}' fill='{c}' opacity='0'>"
            f"<animateTransform attributeName='transform' type='translate' values='0 0;{drift:.0f} -{rise:.0f}' dur='{d:.1f}s' begin='{b:.1f}s' repeatCount='indefinite'/>"
            f"<animate attributeName='opacity' values='0;.95;.5;0' keyTimes='0;.2;.7;1' dur='{d:.1f}s' begin='{b:.1f}s' repeatCount='indefinite'/></circle>")
    return "".join(out)


def sun(cx, cy, r, rays=True, op=1.0, uid="sun", rot_dur=90, ray_len=2.4):
    """Rising-sun disc (hinomaru) with slowly rotating rays. Needs defs from sun_defs()."""
    out = [f"<g opacity='{op}'>"]
    if rays:
        n = 24
        paths = []
        for i in range(n):
            a0, a1 = math.radians(i * 360 / n - 3.2), math.radians(i * 360 / n + 3.2)
            r0, r1 = r * 1.06, r * ray_len
            paths.append(f"M{cx + r0 * math.cos(a0):.1f} {cy + r0 * math.sin(a0):.1f}L{cx + r1 * math.cos(a0):.1f} {cy + r1 * math.sin(a0):.1f}"
                         f"L{cx + r1 * math.cos(a1):.1f} {cy + r1 * math.sin(a1):.1f}L{cx + r0 * math.cos(a1):.1f} {cy + r0 * math.sin(a1):.1f}Z")
        out.append(f"<g><animateTransform attributeName='transform' type='rotate' from='0 {cx} {cy}' to='360 {cx} {cy}' dur='{rot_dur}s' repeatCount='indefinite'/>"
                   f"<path d='{''.join(paths)}' fill='url(#{uid}r)'/></g>")
    out.append(f"<circle cx='{cx}' cy='{cy}' r='{r * 1.5:.0f}' fill='url(#{uid}h)'/>")
    out.append(f"<circle cx='{cx}' cy='{cy}' r='{r}' fill='url(#{uid}d)'><animate attributeName='r' values='{r};{r * 1.025:.1f};{r}' dur='6s' repeatCount='indefinite'/></circle>")
    out.append("</g>")
    return "".join(out)


def sun_defs(uid="sun"):
    return (f"<radialGradient id='{uid}d'><stop offset='0' stop-color='#ff5a6e'/><stop offset='.7' stop-color='#e01a3c'/><stop offset='1' stop-color='#b30f2b'/></radialGradient>"
            f"<radialGradient id='{uid}h'><stop offset='.55' stop-color='#ff2a45' stop-opacity='.38'/><stop offset='1' stop-color='#ff2a45' stop-opacity='0'/></radialGradient>"
            f"<radialGradient id='{uid}r' gradientUnits='userSpaceOnUse' r='600'><stop offset='0' stop-color='#ff3b57' stop-opacity='.30'/><stop offset='1' stop-color='#ff3b57' stop-opacity='0'/></radialGradient>")


def fuji(cx, base_y, scale=1.0, fill="#6e1428", snow="#ffe3e6", snow_op=.9):
    """Mount Fuji silhouette with a snow cap that follows the slopes."""
    body = "M-230 0C-150-6-100-60-40-108Q0-122 40-108C100-60 150-6 230 0Z"
    cap = ("M-40-108L-75-79L-58-84L-48-76L-36-90L-24-78L-10-92L2-80L14-92L26-78L38-90L48-76L58-84L75-79L40-108Q0-122-40-108Z")
    return (f"<g transform='translate({cx} {base_y}) scale({scale})'>"
            f"<path d='{body}' fill='{fill}'/><path d='{body}' fill='none' stroke='#ffb3b9' stroke-opacity='.18' stroke-width='1.2'/>"
            f"<path d='{cap}' fill='{snow}' opacity='{snow_op}'/></g>")


def torii(cx, base_y, scale=1.0, fill="#2a0509", accent="#ff3b57", op=1.0):
    """Torii gate silhouette. ~140 wide x ~100 tall at scale 1."""
    return (f"<g transform='translate({cx} {base_y}) scale({scale})' opacity='{op}'>"
            f"<path d='M-70-98Q0-82 70-98L66-86Q0-72-66-86Z' fill='{fill}'/>"
            f"<path d='M-70-98Q0-82 70-98' fill='none' stroke='{accent}' stroke-width='1.4' stroke-opacity='.65'/>"
            f"<rect x='-58' y='-84' width='116' height='6' fill='{fill}'/>"
            f"<rect x='-50' y='-66' width='100' height='8' fill='{fill}'/>"
            f"<rect x='-42' y='-80' width='10' height='80' fill='{fill}'/><rect x='32' y='-80' width='10' height='80' fill='{fill}'/>"
            f"<rect x='-3' y='-82' width='6' height='16' fill='{fill}'/></g>")


def waves(w, y, R, rows, c0="#a31630", c1="#3a0a15", ring="#ff3b57", ring_op=.35, dur=16, uid="wv", ring_n=3, glow=None):
    """Seigaiha (青海波) strip drifting sideways; loops seamlessly every 2R."""
    out = []
    for r in range(rows):
        t = r / max(1, rows - 1)
        fill = _mix(c0, c1, t)
        cy = y + R * .5 * r + R * .5
        shift = R if r % 2 else 0
        for c in range(-2, int(w / (2 * R)) + 3):
            cx = c * 2 * R + shift
            rings = f"<circle cx='{cx}' cy='{cy}' r='{R}' fill='{fill}' stroke='{ring}' stroke-opacity='{ring_op}' stroke-width='1'/>"
            for k in range(1, ring_n):
                rings += f"<circle cx='{cx}' cy='{cy}' r='{R * (1 - k / (ring_n + .4)):.1f}' fill='none' stroke='{ring}' stroke-opacity='{ring_op * .8:.2f}' stroke-width='.9'/>"
            out.append(rings)
    h = R * .5 * rows + R * 1.2
    return (f"<clipPath id='{uid}c'><rect x='0' y='{y}' width='{w}' height='{h}'/></clipPath>"
            f"<g clip-path='url(#{uid}c)'><g><animateTransform attributeName='transform' type='translate' from='0 0' to='-{2 * R} 0' dur='{dur}s' repeatCount='indefinite'/>"
            f"{''.join(out)}</g></g>")


def _mix(a, b, t):
    pa = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    pb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{int(pa[i] + (pb[i] - pa[i]) * t):02x}" for i in range(3))


def lantern(x, y, h=52, delay=0, char="玄", used=None, swing=4):
    """Chōchin lantern swaying from a string at (x, top)."""
    w = h * .78
    top = y
    body_y = top + 16
    ribs = "".join(f"<ellipse cx='{x}' cy='{body_y + h / 2}' rx='{w / 2}' ry='{h * (.5 - i * .0)}' fill='none' stroke='#5a0a18' stroke-opacity='.0'/>" for i in range(0))
    lines = "".join(f"<path d='M{x - w / 2 + 1} {body_y + h * k:.1f}Q{x} {body_y + h * k + 4:.1f} {x + w / 2 - 1} {body_y + h * k:.1f}' fill='none' stroke='#6b0d1d' stroke-opacity='.75' stroke-width='1.1'/>"
                    for k in (.18, .34, .5, .66, .82))
    if used is not None:
        used.setdefault(("kanji", 700), set()).add(char)
    return (f"<g><animateTransform attributeName='transform' type='rotate' values='-{swing} {x} {top};{swing} {x} {top};-{swing} {x} {top}' "
            f"keyTimes='0;.5;1' calcMode='spline' keySplines='.45 0 .55 1;.45 0 .55 1' dur='5.4s' begin='{delay}s' repeatCount='indefinite'/>"
            f"<line x1='{x}' y1='{top - 200}' x2='{x}' y2='{body_y}' stroke='{P['g5']}' stroke-width='1'/>"
            f"<circle cx='{x}' cy='{body_y + h / 2}' r='{h * .95:.0f}' fill='url(#lg)'><animate attributeName='opacity' values='.55;1;.55' dur='3.6s' begin='{delay}s' repeatCount='indefinite'/></circle>"
            f"<rect x='{x - w * .3:.1f}' y='{body_y - 4}' width='{w * .6:.1f}' height='6' rx='1.5' fill='#1d0409' stroke='{P['au']}' stroke-opacity='.6' stroke-width='.7'/>"
            f"<ellipse cx='{x}' cy='{body_y + h / 2}' rx='{w / 2}' ry='{h / 2}' fill='url(#lb)'/>{lines}"
            f"<rect x='{x - w * .3:.1f}' y='{body_y + h - 2}' width='{w * .6:.1f}' height='6' rx='1.5' fill='#1d0409' stroke='{P['au']}' stroke-opacity='.6' stroke-width='.7'/>"
            f"<path d='M{x} {body_y + h + 4}v10' stroke='{P['au']}' stroke-opacity='.8' stroke-width='1.2'/><circle cx='{x}' cy='{body_y + h + 16}' r='1.8' fill='{P['au']}'/>"
            f"<text x='{x}' y='{body_y + h / 2 + h * .17:.1f}' text-anchor='middle' font-family=\"{fam('kanji')}\" font-weight='700' font-size='{h * .5:.0f}' fill='#fff3ef' fill-opacity='.92'>{char}</text></g>")


def lantern_defs():
    return ("<radialGradient id='lg'><stop offset='0' stop-color='#ff3b57' stop-opacity='.45'/><stop offset='1' stop-color='#ff3b57' stop-opacity='0'/></radialGradient>"
            "<linearGradient id='lb' x1='0' x2='1'><stop offset='0' stop-color='#a50f2a'/><stop offset='.45' stop-color='#ff4560'/><stop offset='1' stop-color='#9c0e27'/></linearGradient>")


def corners(w, h, inset=10, ln=22, color=P["rb"], op=.75, sw=1.4):
    d = (f"M{inset} {inset + ln}V{inset}H{inset + ln}M{w - inset - ln} {inset}H{w - inset}V{inset + ln}"
         f"M{w - inset} {h - inset - ln}V{h - inset}H{w - inset - ln}M{inset + ln} {h - inset}H{inset}V{h - inset - ln}")
    return f"<path d='{d}' fill='none' stroke='{color}' stroke-width='{sw}' stroke-opacity='{op}' stroke-linecap='square'/>"


def sakura_flower(cx, cy, r=9, fill="#ffc2cc", centre="#ff3b57", spin=None):
    """Five-petal sakura blossom (for dividers/ornaments)."""
    pet = "".join(f"<path d='{PETAL}' transform='rotate({i * 72}) translate(0 -1) scale({r / 12.5:.3f})' fill='{fill}'/>" for i in range(5))
    anim = (f"<animateTransform attributeName='transform' type='rotate' from='0' to='360' dur='{spin}s' repeatCount='indefinite'/>" if spin else "")
    return (f"<g transform='translate({cx} {cy})'><g>{anim}{pet}</g>"
            f"<circle r='{r * .2:.1f}' fill='{centre}'/></g>")


# ---------------------------------------------------------------- document
class Svg:
    def __init__(self, w, h, title="", rx=14):
        self.w, self.h, self.title, self.rx = w, h, title, rx
        self.defs, self.css, self.body = [], [], []
        self.used = {}
        self._ids = 0

    def uid(self, p="i"):
        self._ids += 1
        return f"{p}{self._ids}"

    def add(self, s):
        self.body.append(s)

    def d(self, s):
        self.defs.append(s)

    def style(self, s):
        self.css.append(s)

    def text(self, x, y, txt, font="sans", weight=600, size=14, fill=P["g1"], anchor="middle",
             track=0, cls="", style="", extra=""):
        self.used.setdefault((font, weight), set()).update(txt)
        a = f" class='{cls}'" if cls else ""
        st = f" style='{style}'" if style else ""
        tr = f" letter-spacing='{track}'" if track else ""
        return (f"<text{a}{st} x='{x}' y='{y}' text-anchor='{anchor}' font-family=\"{fam(font)}\" "
                f"font-weight='{weight}' font-size='{size}'{tr} fill='{fill}' {extra}>{esc(txt)}</text>")

    def w_(self, font, weight, txt, size, track=0):
        self.used.setdefault((font, weight), set()).update(txt)
        return measure(font, weight, txt, size, track)

    def jp(self, x, y, txt, size=14, fill=P["g2"], anchor="middle", track=0, cls="", style="", extra=""):
        return self.text(x, y, txt, "kanji", 700, size, fill, anchor, track, cls, style, extra)

    # --- recurring defs ---------------------------------------------------
    def grain(self):
        self.d("<filter id='grain' x='0' y='0' width='100%' height='100%'><feTurbulence type='fractalNoise' "
               "baseFrequency='0.9' numOctaves='2' seed='4' result='n'/><feColorMatrix in='n' type='matrix' "
               "values='0 0 0 0 1  0 0 0 0 .8  0 0 0 0 .8  0 0 0 0.05 0'/></filter>")
        return f"<rect width='{self.w}' height='{self.h}' rx='{self.rx}' filter='url(#grain)'/>"

    def shimmer(self, gid="sh", dur=6, a=None, b="#ffffff"):
        a = a or P["g1"]
        self.d(f"<linearGradient id='{gid}' gradientUnits='userSpaceOnUse' x1='0' y1='0' x2='520' y2='0'>"
               f"<animateTransform attributeName='gradientTransform' type='translate' from='-520 0' to='{self.w + 520} 0' "
               f"dur='{dur}s' repeatCount='indefinite'/>"
               f"<stop offset='0' stop-color='{a}'/><stop offset='.5' stop-color='{b}'/>"
               f"<stop offset='1' stop-color='{a}'/></linearGradient>")

    def panel(self, fill_id="bg", pattern=True, colors=None):
        """Crimson lacquer panel + shippo texture. colors=(c0,c1,c2) overrides the gradient (e.g. HOT = redder)."""
        c0, c1, c2 = colors or (P['bg0'], P['bg1'], P['bg2'])
        self.d(f"<linearGradient id='{fill_id}' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='{c0}'/>"
               f"<stop offset='.55' stop-color='{c1}'/><stop offset='1' stop-color='{c2}'/></linearGradient>")
        self.d("<pattern id='shippo' width='36' height='36' patternUnits='userSpaceOnUse'><g fill='none' stroke='#ff3b57' stroke-opacity='.08' stroke-width='1'>"
               "<circle cx='0' cy='0' r='18'/><circle cx='36' cy='0' r='18'/><circle cx='0' cy='36' r='18'/><circle cx='36' cy='36' r='18'/><circle cx='18' cy='18' r='18'/></g></pattern>")
        out = f"<rect width='{self.w}' height='{self.h}' rx='{self.rx}' fill='url(#{fill_id})'/>"
        if pattern:
            out += f"<rect width='{self.w}' height='{self.h}' rx='{self.rx}' fill='url(#shippo)'/>"
        return out

    def border(self, inner=True, brackets=True):
        """Gradient border + inner hairline + corner brackets (draw this LAST so scenery never covers it)."""
        self.d("<linearGradient id='bd' x1='0' x2='1'><stop offset='0' stop-color='#8a0f24' stop-opacity='.25'/>"
               "<stop offset='.5' stop-color='#ff3b57' stop-opacity='.9'/><stop offset='1' stop-color='#8a0f24' stop-opacity='.25'/></linearGradient>")
        r = self.rx
        out = f"<rect x='.5' y='.5' width='{self.w - 1}' height='{self.h - 1}' rx='{r}' fill='none' stroke='url(#bd)' stroke-width='1.2'/>"
        if inner:
            out += (f"<rect x='6.5' y='6.5' width='{self.w - 13}' height='{self.h - 13}' rx='{max(r - 5, 2)}' fill='none' "
                    f"stroke='#ff3b57' stroke-opacity='.14'/>")
        if brackets:
            out += corners(self.w, self.h, 12, 18, P["rb"], .6, 1.3)
        return out

    def frame(self, fill_id="bg", pattern=True, inner=True, brackets=True):
        return self.panel(fill_id, pattern) + self.border(inner, brackets)

    def clip_round(self, cid="cl"):
        """Clip scenery to the rounded panel."""
        self.d(f"<clipPath id='{cid}'><rect width='{self.w}' height='{self.h}' rx='{self.rx}'/></clipPath>")
        return cid

    def stars(self, n, seed, avoid=None, opacity=.6, rows=None):
        rnd = random.Random(seed)
        out = []
        for _ in range(n):
            for _try in range(20):
                x, y = rnd.randint(30, self.w - 30), rnd.randint(14, (rows or self.h) - 14)
                if not avoid or not any(a <= x <= b and c <= y <= e for a, c, b, e in
                                        [(av[0], av[1], av[2], av[3]) for av in avoid]):
                    break
            r = rnd.choice([.8, 1.1, 1.4])
            out.append(f"<circle cx='{x}' cy='{y}' r='{r}' fill='{rnd.choice(['#ffd6d6', '#ff9aa8', '#fff'])}'><animate attributeName='opacity' "
                       f"values='.05;{opacity};.05' dur='{rnd.uniform(2.4, 5):.1f}s' begin='{rnd.uniform(0, 3):.1f}s' "
                       f"repeatCount='indefinite'/></circle>")
        return "".join(out)

    def extrude(self, x, y, w, h, rx, face, n=10, ex=-.9, ey=.9, c0=(40, 6, 12), c1=(150, 22, 44), edge=True):
        """The 3D 'stack' look. ex/ey = direction of the depth (default: toward bottom-left)."""
        out = []
        for i in range(n, 0, -1):
            t = (n - i) / max(1, n - 1)
            col = "rgb({},{},{})".format(*[int(c0[k] + (c1[k] - c0[k]) * t) for k in range(3)])
            out.append(f"<rect x='{x - i * ex * -1 + 0:.1f}' y='{y + i * ey:.1f}' width='{w}' height='{h}' rx='{rx}' fill='{col}'/>")
        out.append(f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{rx}' fill='{face}'/>")
        if edge:
            out.append(f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{rx}' fill='none' stroke='#ffb3b9' stroke-opacity='.3'/>")
        return "".join(out)

    def seal(self, cx, cy, size=26, char="玄", rot=-4):
        """Hanko (判子) stamp."""
        self.used.setdefault(("kanji", 700), set()).add(char)
        return (f"<g class='seal' transform='rotate({rot} {cx} {cy})'><rect x='{cx - size / 2}' y='{cy - size / 2}' width='{size}' height='{size}' rx='3' fill='{P['r']}'/>"
                f"<rect x='{cx - size / 2 + 2}' y='{cy - size / 2 + 2}' width='{size - 4}' height='{size - 4}' rx='1.8' fill='none' stroke='#fff' stroke-opacity='.45' stroke-width='.9'/>"
                f"<text x='{cx}' y='{cy + size * .27:.1f}' text-anchor='middle' font-family=\"{fam('kanji')}\" font-weight='700' "
                f"font-size='{size * .62:.1f}' fill='#fff'>{char}</text></g>")

    # --- output -----------------------------------------------------------
    def render(self):
        faces = "".join(font_face(k, wt, ch) for (k, wt), ch in sorted(self.used.items()))
        style = f"<style>{faces}{''.join(self.css)}</style>"
        t = f"<title>{esc(self.title)}</title>" if self.title else ""
        return (f"<svg xmlns='http://www.w3.org/2000/svg' width='{self.w}' height='{self.h}' viewBox='0 0 {self.w} {self.h}' "
                f"role='img'>{t}<defs>{''.join(self.defs)}{style}</defs>{''.join(self.body)}</svg>")


COMMON_CSS = (
    ".fade{opacity:0;animation:fi 1.2s ease forwards}@keyframes fi{to{opacity:1}}"
    ".seal{animation:pulse 3.2s ease-in-out infinite}@keyframes pulse{0%,100%{opacity:1}50%{opacity:.62}}"
    "@keyframes track{from{letter-spacing:var(--t0);opacity:0}to{letter-spacing:var(--t1);opacity:1}}"
    "@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}"
    ".bob{animation:bob 6s ease-in-out infinite}"
)
