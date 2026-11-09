#!/usr/bin/env python3
"""Adiciona o glifo ☰ (U+2630) às fontes usadas nos SVGs (as originais não têm esse símbolo).
Gera fonts/<Nome>-nexus.<ext>; o lib.py usa essas versões."""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.t2CharStringPen import T2CharStringPen

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
FILES = ["Outfit-Regular.ttf", "Outfit-Bold.ttf", "Inter-Medium.otf", "Inter-SemiBold.otf",
         "JetBrainsMono-Regular.ttf", "JetBrainsMono-Bold.ttf"]
NAME = "uni2630"


def draw(pen, upm, cap, adv, bold):
    x0, x1 = adv * .14, adv * .86
    h = cap * (.13 if bold else .10)
    total = cap * .62
    gap = (total - 3 * h) / 2
    base = cap * .19
    for i in range(3):
        y = base + i * (h + gap)
        pen.moveTo((x0, y)); pen.lineTo((x0, y + h)); pen.lineTo((x1, y + h)); pen.lineTo((x1, y)); pen.closePath()


for fn in FILES:
    f = TTFont(os.path.join(D, fn))
    upm = f["head"].unitsPerEm
    cap = getattr(f["OS/2"], "sCapHeight", 0) or int(upm * .7)
    mono = fn.startswith("JetBrains")
    adv = f["hmtx"]["A"][0] if mono else int(upm * .76)
    bold = "Bold" in fn or "SemiBold" in fn
    order = f.getGlyphOrder() + [NAME]
    if "glyf" in f:
        pen = TTGlyphPen(None); draw(pen, upm, cap, adv, bold); g = pen.glyph()
        f.setGlyphOrder(order); f["glyf"].glyphs[NAME] = g; f["glyf"].glyphOrder = order
        g.recalcBounds(f["glyf"])
    else:
        cff = f["CFF "].cff; top = cff.topDictIndex[0]; cs = top.CharStrings
        pen = T2CharStringPen(adv, None); draw(pen, upm, cap, adv, bold)
        ch = pen.getCharString(private=top.Private, globalSubrs=cff.GlobalSubrs)
        cs.charStringsIndex.append(ch)
        cs.charStrings[NAME] = len(cs.charStringsIndex) - 1
        top.charset.append(NAME)
        f.setGlyphOrder(order)
        if hasattr(top, "FDSelect") and top.FDSelect is not None:
            top.FDSelect.append(0) if hasattr(top.FDSelect, "append") else None
    f["hmtx"].metrics[NAME] = (int(adv), int(adv * .14))
    for t in f["cmap"].tables:
        if t.isUnicode():
            t.cmap[0x2630] = NAME
    f["maxp"].numGlyphs = len(order)
    b, e = os.path.splitext(fn)
    f.save(os.path.join(D, f"{b}-nexus{e}"))
    print("ok", fn)
