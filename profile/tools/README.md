# Gerador dos assets do README (tema carmesim · japonês)

SVGs animados: `build.py`, com fontes **embutidas**. GIFs: `gifs.py` (canvas + ffmpeg).

```bash
pip install fonttools playwright && playwright install chromium
python3 tools/make_kanji.py     # recorta o Noto Serif CJK JP só com os glifos usados (rode ao mudar texto japonês)
python3 tools/build.py          # regenera assets/*.svg
python3 tools/gifs.py [sakura|slash|rain|torii]   # regenera assets/gif-*.gif (precisa de ffmpeg)
python3 tools/preview.py out/ assets/banner.svg   # PNG de preview
```

Personalize no bloco `CFG` de `build.py` (textos, JP, stack, links, equipe, rodapé/copyright).
Ícones: code, terminal, user, users, activity, coffee, gamepad, film, cap, cube, globe, database, server, monitor,
heart, spark, pen, drop, send, shield, lock, book, flame, branch, phone (novos em `ICONS` no `lib.py`).

Fontes (SIL OFL 1.1): Outfit, Inter, JetBrains Mono, Noto Serif CJK JP.
Fotos da equipe: `tools/src/photos/` (jpg quadrado ~240px).
