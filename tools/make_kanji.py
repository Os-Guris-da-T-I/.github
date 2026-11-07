#!/usr/bin/env python3
"""Gera tools/fonts/kanji-subset.otf: recorta o Noto Serif CJK JP Bold só com os glifos japoneses
usados em build.py / gifs.py (+ todo o hiragana/katakana). Rode de novo quando adicionar texto japonês.
Precisa da fonte no sistema:  /usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc  (ou passe o caminho)."""
import os, re, sys
from fontTools.ttLib import TTCollection
from fontTools import subset

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
CJK = re.compile(r"[\u3000-\u30ff\u4e00-\u9fff\uff00-\uffef]")

chars = set(chr(c) for c in range(0x3041, 0x3097)) | set(chr(c) for c in range(0x30A1, 0x30FB)) | set("・ー「」、。")
for fn in ("build.py", "gifs.py"):
    p = os.path.join(HERE, fn)
    if os.path.exists(p):
        chars |= set(CJK.findall(open(p, encoding="utf-8").read()))

ttc = TTCollection(SRC)
font = next(f for f in ttc.fonts if "JP" in str(f["name"].getDebugName(1)))
o = subset.Options(); o.layout_features = ["*"]; o.notdef_outline = True
s = subset.Subsetter(o); s.populate(text="".join(sorted(chars)) + " "); s.subset(font)
out = os.path.join(HERE, "fonts", "kanji-subset.otf")
font.save(out)
print(len(chars), "glifos ->", out, os.path.getsize(out), "bytes")
