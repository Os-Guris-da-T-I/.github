#!/usr/bin/env python3
"""Adiciona o glifo ☰ (U+2630) ao Outfit-Bold -> fonts/Outfit-Bold-nexus.ttf (o original não tem esse glifo)."""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
f = TTFont(os.path.join(D, "Outfit-Bold.ttf"))
upm = f["head"].unitsPerEm
s = upm / 1000
adv, x0, x1 = 760 * s, 110 * s, 650 * s
bar, gap, base = 92 * s, 82 * s, 150 * s
pen = TTGlyphPen(None)
for i in range(3):
    y = base + i * (bar + gap)
    pen.moveTo((x0, y)); pen.lineTo((x0, y + bar)); pen.lineTo((x1, y + bar)); pen.lineTo((x1, y)); pen.closePath()
g = pen.glyph()
name = "uni2630"
order = f.getGlyphOrder() + [name]
f.setGlyphOrder(order)
f["glyf"].glyphs[name] = g
f["glyf"].glyphOrder = order
g.recalcBounds(f["glyf"])
f["hmtx"].metrics[name] = (int(adv), int(x0))
for t in f["cmap"].tables:
    if t.isUnicode():
        t.cmap[0x2630] = name
f["maxp"].numGlyphs = len(order)
f.save(os.path.join(D, "Outfit-Bold-nexus.ttf"))
print("ok")
