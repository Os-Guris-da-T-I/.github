#!/usr/bin/env python3
"""
Rebuilds every SVG in ../assets.   Usage:  python3 tools/make_kanji.py && python3 tools/build.py
Needs:  pip install fonttools

Tema: CARMESIM + JAPONÊS (sol nascente, Fuji, torii, ondas seigaiha, sakura, lanternas, hanko).
Edit the CFG block below (texts, icons, stack, links) and run again.
"""
import math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")

# =============================================================== EDIT HERE
CFG = dict(
    name="GURIS DA T.I",
    kana="グリス・ダ・ティー・アイ",
    eyebrow="GENNISCODE  ·  COMUNIDADE BRASILEIRA DE T.I.",
    role=("Tecnologia", "·", "Educação · Criação de conteúdo"),
    sub="Coletivo de amigos universitários · Co-fundadores do GennisCode · Universidade Braz Cubas",
    tagline="// aprenda. construa. compartilhe.",
    side_text="COLETIVO  ·  UNIVERSITÁRIO",
    vertical_jp="継続は力なり",
    vertical_jp_l="仲間と共に",
    chips=[("code", "DEVS"), ("monitor", "STREAMERS"), ("film", "EDITORES"), ("pen", "DESIGNERS"), ("cap", "ESTUDANTES")],
    # section headers: file -> (number, title, icon, japanese subtitle, watermark kanji)
    headers={
        "header-sobre": ("01", "SOBRE NÓS", "users", "私たち", "私"),
        "header-stack": ("02", "STACK", "code", "技術", "技"),
        "header-atividade": ("03", "ATIVIDADE", "activity", "活動", "動"),
        "header-equipe": ("04", "EQUIPE", "user", "仲間", "仲"),
        "header-gennis": ("05", "GENNISCODE", "cube", "道場", "道"),
        "header-comunidade": ("06", "COMUNIDADE", "chat", "絆", "絆"),
    },
    # quick facts cards: (icon, label, japanese, value, watermark)
    facts=[("monitor", "FOCO", "焦点", "Tecnologia & Educação", "焦"),
           ("code", "ATUAÇÃO", "活動", "Dev · Stream · Edição · Design", "活"),
           ("cap", "FORMAÇÃO", "学歴", "Universidade Braz Cubas", "学"),
           ("globe", "MISSÃO", "使命", "T.I. gratuita para o Brasil", "命")],
    quote=("Lembre-se:", "Você nunca estará sozinho."),
    quote_jp="君は一人じゃない",
    stack=["C", "C++", "C#", "Java", "Python", "JavaScript", "NestJS", "CodeIgniter", "Meteor", "HTML5", "CSS3", "PostgreSQL",
           "Unreal Engine", "Blender", "Photoshop", "Linux", "Debian", "Ubuntu", "Apache", "VS Code"],
    layers=[("BACK-END", "server", ["NestJS", "CodeIgniter", "Meteor", "Java", "C#", "Python"], "バックエンド"),
            ("FRONT-END", "monitor", ["HTML5", "CSS3", "JavaScript"], "フロントエンド"),
            ("BANCO DE DADOS", "database", ["PostgreSQL"], "データベース"),
            ("GAMES & 3D", "cube", ["Unreal Engine", "C++", "C#", "Blender"], "ゲーム・三次元"),
            ("DESIGN & EDIÇÃO", "pen", ["Photoshop"], "デザイン"),
            ("INFRA & AMBIENTE", "terminal", ["Linux", "Debian", "Ubuntu", "Apache", "C", "VS Code"], "基盤")],
    distros=["Ubuntu", "Linux Mint", "Pop!_OS", "Fedora", "Nobara KDE", "Debian", "KDE Plasma", "GNOME", "Wayland", "X11",
             "Windows XP", "Windows 7", "Windows 10", "Windows 11"],
    distro_layers=[("DISTROS DEBIAN / UBUNTU", "terminal", ["Ubuntu", "Linux Mint", "Pop!_OS", "Debian"], "ディストロ"),
                   ("FEDORA & DERIVADAS", "cube", ["Fedora", "Nobara KDE"], "フェドーラ系"),
                   ("AMBIENTES DE DESKTOP", "monitor", ["KDE Plasma", "GNOME", "Cinnamon", "XFCE"], "デスクトップ"),
                   ("SERVIDOR DE VÍDEO", "globe", ["Wayland", "X11"], "表示"),
                   ("WINDOWS", "monitor", ["Windows XP", "Windows 7", "Windows 10", "Windows 11"], "ウィンドウズ"),
                   ("VM & DUAL BOOT", "server", ["VirtualBox", "Dual Boot", "WSL"], "仮想化")],
    recruit=dict(eyebrow="PARA RECRUTADORES E ESTUDANTES", jp="採用担当者・学生の皆さんへ", title="CONHEÇA O QUE CONSTRUÍMOS",
                 text=("Ficou interessado nos nossos projetos e quer conhecer um pouco mais do que fizemos no passado "
                       "e do que estamos construindo agora? Nossos repositórios são públicos e permitidos para testes "
                       "educacionais e técnicos."),
                 chips=[("branch", "REPOSITÓRIOS PÚBLICOS", "公開"), ("cap", "TESTES EDUCACIONAIS", "学習"), ("code", "TESTES TÉCNICOS", "検証")]),
    typing_main=["Opa bão?", "Somos os Guris da T.I", "Tecnologia, educação e criação de conteúdo",
                 "Co-fundadores do GennisCode", "Ensinando T.I. de graça pro Brasil inteiro",
                 "Estudantes na Universidade Braz Cubas", "Você nunca estará sozinho :)", "Siga @guriz.mp4 no Instagram"],
    typing_team=["Guris da T.I | GennisTeam", "Siga nossa equipe pelo Git! :)"],
    cta=("CONHEÇA O PROJETO", "GennisCode"),
    cta_insta=("SIGA NO INSTAGRAM", "@guriz.mp4"),
    # team cards: (file, name, handle, photo in tools/src/photos, role -- leave "" until you decide the roles)
    team=[("joao", "João Victor Guimarães", "@jaobom006", "joao.jpg", ""),
          ("gabriel", "Gabriel Gonçalves", "@midasrei68-dev", "gabriel.jpg", ""),
          ("matheus", "Matheus Pentogennis", "@mwtheuskkj", "matheus.jpg", ""),
          ("gustavo", "Gustavo Gabriel F", "@Massarubash", "gustavo.jpg", ""),
          ("lucas-graca", "Lucas da Graça", "@lucasgracaleandro-arch", "lucas-graca.jpg", ""),
          ("lucas-siqueira", "Lucas Siqueira", "@Luucasy", "lucas-siqueira.jpg", "")],
    fluxer=dict(eyebrow="COMUNIDADE · FLUXER · 仲間に加わろう", l1="NOSSA COMUNIDADE", l2="NO FLUXER",
                line1="Comunidade brasileira 100% gratuita de T.I.",
                line2="Tire dúvidas, aprenda do zero e cresça junto com a gente.",
                button="ENTRAR NA COMUNIDADE", url="fluxer.gg/uHuHUyOJ"),
    footer=dict(a="Aprenda. Construa.", b="Compartilhe.", jp="学ぶ・創る・分かち合う",
                sub="Tecnologia é melhor quando é compartilhada.",
                credit="GURIS DA T.I  ·  GENNISCODE",
                copyright="© GurisDaTI Brazil Entertainment · All privacy and security rights reserved.",
                icons=["code", "gamepad", "coffee", "globe", "heart"]),
    pillars=[("学", "APRENDER", "学ぶ", "Do zero absoluto ao mercado de trabalho, com educação de qualidade e sem mensalidade."),
             ("創", "CONSTRUIR", "創る", "Projetos reais, código aberto e prática de verdade para virar portfólio."),
             ("分", "COMPARTILHAR", "分かち合う", "Conhecimento é melhor dividido. Comunidade, apoio mútuo e ninguém para trás.")],
    journey=[("入", "DO ZERO", "入門", "Sem pré-requisito"), ("基", "FUNDAMENTOS", "基礎", "Lógica e base sólida"),
             ("実", "PRÁTICA", "実践", "Exercícios reais"), ("作", "PROJETOS", "作品", "Portfólio no GitHub"),
             ("証", "CERTIFICADO", "証明", "Certificação ao final")],
    proverbs=[("継続は力なり", "persistência é poder"), ("七転び八起き", "caia sete vezes, levante oito"),
              ("一期一会", "cada encontro é único"), ("初心忘るべからず", "nunca perca a mente de iniciante"),
              ("千里の道も一歩から", "toda jornada começa num passo"), ("為せば成る", "quem faz, consegue")],
)
# =========================================================================

W = 1200
JP = "玄"
RB, R_, RD = P["rb"], P["r"], P["rd"]


def runs(s, x, y, parts, size, anchor="middle", track=0, cls="", style=""):
    """Text made of coloured/font-switched pieces: parts = [(text, font, weight, fill)]."""
    inner = ""
    for t, f, wt, fill in parts:
        s.used.setdefault((f, wt), set()).update(t)
        inner += f"<tspan font-family=\"{fam(f)}\" font-weight='{wt}' fill='{fill}'>{esc(t)}</tspan>"
    a = f" class='{cls}'" if cls else ""
    st = f" style='{style}'" if style else ""
    tr = f" letter-spacing='{track}'" if track else ""
    return f"<text{a}{st} x='{x}' y='{y}' text-anchor='{anchor}' font-size='{size}'{tr}>{inner}</text>"


def runs_w(s, parts, size, track=0):
    tot = 0
    for t, f, wt, _ in parts:
        s.used.setdefault((f, wt), set()).update(t)
        tot += measure(f, wt, t, size, track) + track * 1
    return tot


def edge_mask(s, mid, h, fade=.12, y=0, gid="ef"):
    s.d(f"<linearGradient id='{gid}' x1='0' x2='1'><stop offset='0' stop-color='#000'/><stop offset='{fade}' stop-color='#fff'/>"
        f"<stop offset='{1 - fade}' stop-color='#fff'/><stop offset='1' stop-color='#000'/></linearGradient>")
    s.d(f"<mask id='{mid}' maskUnits='userSpaceOnUse' x='0' y='{y}' width='{W}' height='{h}'><rect x='0' y='{y}' width='{W}' height='{h}' fill='url(#{gid})'/></mask>")


def wrap(font, weight, text, size, maxw, sep=" · ", track=0):
    parts, lines, cur = text.split(sep), [], ""
    for p in parts:
        t = p if not cur else cur + sep + p
        if measure(font, weight, t, size, track) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = p
    lines.append(cur)
    return lines


def comet(x0, x1, y, dur, begin=0, w=180, h=1.6, rev=False, gid="cm", op=1):
    g = f"{gid}r" if rev else gid
    xs, xe = (x1, x0) if rev else (x0, x1)
    return (f"<rect x='0' y='{y}' width='{w}' height='{h}' rx='{h / 2}' fill='url(#{g})' opacity='{op}'>"
            f"<animateTransform attributeName='transform' type='translate' from='{xs} 0' to='{xe} 0' dur='{dur}s' begin='{begin}s' repeatCount='indefinite'/></rect>")


def comet_defs(s):
    s.d("<linearGradient id='cm' x1='0' x2='1'><stop offset='0' stop-color='#ff3b57' stop-opacity='0'/><stop offset='1' stop-color='#ffe3e6'/></linearGradient>")
    s.d("<linearGradient id='cmr' x1='0' x2='1'><stop offset='0' stop-color='#ffe3e6'/><stop offset='1' stop-color='#ff3b57' stop-opacity='0'/></linearGradient>")


def ornament(s, cx, cy, fill=P["bg0"], spin=26):
    """Centre piece of the dividers: pulsing ring + sakura blossom."""
    return (f"<circle cx='{cx}' cy='{cy}' r='8' fill='none' stroke='{RB}'><animate attributeName='r' values='8;26' dur='3.2s' repeatCount='indefinite'/>"
            f"<animate attributeName='opacity' values='.6;0' dur='3.2s' repeatCount='indefinite'/></circle>"
            f"<circle cx='{cx}' cy='{cy}' r='13' fill='{fill}' stroke='{RB}' stroke-opacity='.8' stroke-width='1.1'/>"
            f"{sakura_flower(cx, cy, 8.5, P['pk'], '#ff3b57', spin)}"
            f"<g fill='{R_}'><rect x='{cx - 40}' y='{cy - 2}' width='4' height='4' transform='rotate(45 {cx - 38} {cy})'/>"
            f"<rect x='{cx + 36}' y='{cy - 2}' width='4' height='4' transform='rotate(45 {cx + 38} {cy})'/></g>")


# ------------------------------------------------------------------ dividers
def divider():
    s = Svg(W, 48, "")
    comet_defs(s)
    edge_mask(s, "m", 48)
    s.d("<linearGradient id='gv' x1='0' x2='1'><stop offset='0' stop-color='#5a0e1c' stop-opacity='0'/><stop offset='.15' stop-color='#8a0f24' stop-opacity='.95'/>"
        "<stop offset='.85' stop-color='#8a0f24' stop-opacity='.95'/><stop offset='1' stop-color='#5a0e1c' stop-opacity='0'/></linearGradient>")
    s.d(f"<linearGradient id='hl' x1='0' x2='1'><stop offset='0' stop-color='{RB}' stop-opacity='0'/><stop offset='.5' stop-color='{RB}' stop-opacity='1'/>"
        f"<stop offset='1' stop-color='{RB}' stop-opacity='0'/></linearGradient>")
    ticks = "".join(f"<rect x='{x}' y='{24 - (4 if i % 5 == 0 else 2.5)}' width='1' height='{8 if i % 5 == 0 else 5}' fill='{RB}' opacity='{.6 if i % 5 == 0 else .3}'/>"
                    for i, x in enumerate(range(96, 1110, 22)) if abs(x - 600) > 56)
    s.add(f"<g mask='url(#m)'><rect x='0' y='22' width='{W}' height='4' rx='2' fill='url(#gv)'/>"
          f"<rect x='0' y='23.5' width='{W}' height='1' fill='url(#hl)'/>{ticks}"
          f"{comet(-180, 1380, 23.2, 5.2)}{comet(-180, 1380, 23.4, 8, 1.5, 120, 1.2, True, op=.6)}</g>")
    s.add(f"<g>{petals(4, 3, 120, 1080, 2, 0, .55, dur=(7, 11), fall=44)}</g>")
    s.add(ornament(s, 600, 24))
    return s


def divider_wave():
    """Seigaiha (青海波) wave strip."""
    s = Svg(W, 60, "")
    edge_mask(s, "m", 60)
    s.add(f"<g mask='url(#m)'>{waves(W, 6, 15, 4, '#c01836', '#4a0b18', '#ffb3b9', .38, 18, 'dv')}</g>")
    s.add(f"<circle cx='600' cy='30' r='21' fill='{P['bg0']}' opacity='.9'/>")
    s.add(ornament(s, 600, 30, spin=30))
    return s


def team_line():
    s = Svg(W, 38, "")
    comet_defs(s)
    edge_mask(s, "m", 38)
    s.d("<linearGradient id='ll' x1='0' x2='1'><stop offset='0' stop-color='#dc143c' stop-opacity='0'/><stop offset='.5' stop-color='#dc143c'/><stop offset='1' stop-color='#dc143c' stop-opacity='0'/></linearGradient>")
    s.add(f"<g mask='url(#m)'><rect x='0' y='18' width='{W}' height='2' rx='1' fill='url(#ll)'/>{comet(-180, 1380, 18.2, 4.6)}</g>")
    s.add(ornament(s, 600, 19))
    return s


# ------------------------------------------------------------------ headers
def header(num, title, ic, jp, mark):
    H = 112
    s = Svg(W, H, title.title(), rx=12)
    s.shimmer("sh", 6, "#ffd6d6")
    comet_defs(s)
    s.d(f"<linearGradient id='ul' x1='0' x2='1'><stop offset='0' stop-color='#fff' stop-opacity='0'/><stop offset='.5' stop-color='{RB}'/><stop offset='1' stop-color='#fff' stop-opacity='0'/></linearGradient>")
    s.d(sun_defs("hs"))
    cid = s.clip_round()
    hot = num == "01"
    s.add(s.panel(colors=HOT if hot else None))
    track = 9
    tw = s.w_("display", 700, title, 34, track)
    s.style(COMMON_CSS + f".t{{animation:tt 1.8s cubic-bezier(.16,.84,.24,1) both}}@keyframes tt{{from{{letter-spacing:34px;opacity:0}}to{{letter-spacing:{track}px;opacity:1}}}}"
            ".ic{opacity:0;animation:fi 1s 1s ease forwards}.ring{transform-origin:center;transform-box:fill-box;animation:spin 24s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}"
            ".wm{animation:wm 7s ease-in-out infinite}@keyframes wm{0%,100%{opacity:.07}50%{opacity:.16}}")
    s.add(f"<g clip-path='url(#{cid})'>")
    s.add(f"<g transform='translate(0 0)'>{sun(30, 56, 38, True, .55, 'hs', 120, 5.5)}{sun(1170, 56, 38, True, .55, 'hs', 150, 5.5)}</g>")
    s.add(s.jp(214, 94, mark, 104, RB, cls="wm") + s.jp(986, 94, mark, 104, RB, cls="wm", style="animation-delay:3.5s"))
    s.add(f"<g>{petals(5, int(num) * 5, 100, 1100, 4, 0, .6, dur=(8, 13), fall=108)}</g>")
    if hot:
        s.add(f"<rect x='-300' y='-10' width='160' height='{H + 20}' fill='#fff' fill-opacity='.14' transform='skewX(-20)'><animateTransform attributeName='transform' type='translate' values='0 0;1600 0;1600 0' keyTimes='0;.5;1' dur='6s' repeatCount='indefinite' additive='sum'/></rect>")
        s.add(f"<ellipse cx='600' cy='56' rx='360' ry='60' fill='#ff3b57' fill-opacity='.22'><animate attributeName='fill-opacity' values='.12;.3;.12' dur='4s' repeatCount='indefinite'/></ellipse>")
    s.add("</g>")
    s.add(runs(s, 600, 32, [(JP, "kanji", 700, R_), (f"  ·  {num}  ·  ", "mono", 700, RB), (jp, "kanji", 700, P["g1"])], 12.5, track=4, cls="fade", style="animation-delay:.3s"))
    s.add(s.text(600 + track / 2, 74, title, "display", 700, 34, "url(#sh)", track=track, cls="t"))
    off = tw / 2 + 56
    for sx in (600 - off, 600 + off):
        s.add(f"<g class='ic'><circle cx='{sx}' cy='60' r='20' fill='{RB}' fill-opacity='.08' stroke='{RB}' stroke-opacity='.7'/>"
              f"<circle class='ring' cx='{sx}' cy='60' r='26' fill='none' stroke='{RB}' stroke-dasharray='1 6' stroke-linecap='round'/>"
              f"{icon(ic, sx, 60, 20, P['w'], 1.5)}</g>")
    s.add("<g><rect x='150' y='96' width='900' height='1' fill='url(#ul)'/>")
    s.add(comet(120, 1020, 95.6, 4.5, 0, 140, 1.8, False))
    s.add(f"{sakura_flower(600, 96.5, 6.5, P['pk'], '#ff3b57', 20)}</g>")
    s.add(s.border())
    s.add(s.grain())
    return s


def subheader(title, ic, name):
    tw = measure("display", 700, title, 22, 7)
    pw = tw + 200
    s = Svg(W, 76, name, rx=36)
    s.shimmer("sh", 6, "#ffd6d6")
    s.style(COMMON_CSS + ".bobi{animation:bob 5s ease-in-out infinite}")
    px = (W - pw) / 2
    s.d("<linearGradient id='bd' x1='0' x2='1'><stop offset='0' stop-color='#8a0f24' stop-opacity='.2'/><stop offset='.5' stop-color='#ff3b57' stop-opacity='.9'/><stop offset='1' stop-color='#8a0f24' stop-opacity='.2'/></linearGradient>")
    s.d(f"<linearGradient id='bg' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='{P['bg0']}'/><stop offset='.6' stop-color='{P['bg1']}'/><stop offset='1' stop-color='{P['bg2']}'/></linearGradient>")
    s.add(f"<rect x='{px}' y='8' width='{pw}' height='60' rx='30' fill='url(#bg)'/><rect x='{px + .5}' y='8.5' width='{pw - 1}' height='59' rx='29.5' fill='none' stroke='url(#bd)' stroke-width='1.2'/>"
          f"<rect x='{px + 5}' y='13' width='{pw - 10}' height='50' rx='25' fill='none' stroke='{RB}' stroke-opacity='.15'/>")
    s.add(f"<g class='bobi'>{sakura_flower(px + 40, 38, 10, P['pk'], '#ff3b57', 24)}{sakura_flower(px + pw - 40, 38, 10, P['pk'], '#ff3b57', 24)}</g>")
    s.add(f"<g class='bobi' style='animation-delay:.6s'>{icon(ic, px + 76, 38, 18, P['g1'], 1.5)}{icon(ic, px + pw - 76, 38, 18, P['g1'], 1.5)}</g>")
    s.add(s.text(600 + 3.5, 46, title, "display", 700, 22, "url(#sh)", track=7))
    return s


def quote():
    a, b = CFG["quote"]
    H = 168
    s = Svg(W, H, "Lembrete: Você nunca estará sozinho", rx=14)
    s.shimmer("sh", 7, "#ffd6d6")
    s.style(COMMON_CSS + ".beat{transform-origin:center;transform-box:fill-box;animation:beat 2.4s ease-in-out infinite}@keyframes beat{0%,100%{transform:scale(1)}12%{transform:scale(1.16)}24%{transform:scale(1)}36%{transform:scale(1.1)}48%{transform:scale(1)}}"
            ".wm{animation:wm 7s ease-in-out infinite}@keyframes wm{0%,100%{opacity:.07}50%{opacity:.17}}")
    s.d(sun_defs("qs"))
    cid = s.clip_round()
    s.add(s.panel())
    s.add(f"<g clip-path='url(#{cid})'>{sun(600, 196, 54, True, .5, 'qs', 140, 3.4)}"
          f"{s.jp(170, 120, '絆', 130, RB, cls='wm')}{s.jp(1030, 120, '友', 130, RB, cls='wm', style='animation-delay:3.5s')}"
          f"<g>{petals(8, 21, 60, 1140, 4, 0, .7, dur=(8, 13), fall=170)}</g>{embers(10, 4, 100, 1100, 120, 160)}</g>")
    heart = icon('heart', 600, 40, 30, RB, 1.6, fill="#ff3b57")
    s.add(f"<g class='beat'>{heart}</g>")
    s.add(runs(s, 600, 96, [(a + " ", "display", 400, P["g3"]), (b, "display", 700, P["w"])], 28, cls="fade", style="animation-delay:.4s"))
    s.add(s.jp(600 + 4, 128, CFG["quote_jp"], 15, P["g2"], track=8, cls="fade", style="animation-delay:1s"))
    s.add(f"<rect x='450' y='142' width='300' height='1' fill='{RB}' opacity='.4'/>")
    comet_defs(s)
    s.add(comet(430, 770, 141.6, 4, 0, 100, 1.6))
    s.add(s.border())
    s.add(s.grain())
    return s


def fact_cards():
    cw, gap, ch = 282, 24, 150
    s = Svg(W, ch + 16, "Resumo", rx=14)
    s.style(COMMON_CSS)
    s.d(f"<linearGradient id='bg' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='{P['bg0']}'/><stop offset='.6' stop-color='{P['bg1']}'/><stop offset='1' stop-color='{P['bg2']}'/></linearGradient>")
    s.d(f"<linearGradient id='bd' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='{RB}' stop-opacity='.8'/><stop offset='1' stop-color='{RD}' stop-opacity='.1'/></linearGradient>")
    comet_defs(s)
    for i, (ic, lab, jp, val, mark) in enumerate(CFG["facts"]):
        x = i * (cw + gap)
        d = f"{i * .5}s"
        lines = wrap("sans", 600, val, 15.5, cw - 36)
        cid = s.uid("fc")
        s.d(f"<clipPath id='{cid}'><rect x='{x}' y='8' width='{cw}' height='{ch}' rx='14'/></clipPath>")
        inner = (f"<rect x='{x}' y='8' width='{cw}' height='{ch}' rx='14' fill='url(#bg)'/>"
                 f"<g clip-path='url(#{cid})'><rect x='{x}' y='8' width='{cw}' height='{ch}' fill='url(#shippo2)'/>"
                 + s.jp(x + cw - 34, 8 + ch - 4, mark, 92, RB, extra="fill-opacity='.10'") +
                 f"<path d='M{x} {8 + ch - 22}h{cw}' stroke='{RB}' stroke-opacity='.12'/></g>"
                 f"<rect x='{x + .5}' y='8.5' width='{cw - 1}' height='{ch - 1}' rx='13.5' fill='none' stroke='url(#bd)' stroke-width='1.1'/>"
                 f"<circle cx='{x + cw / 2}' cy='54' r='23' fill='{RB}' fill-opacity='.10' stroke='{RB}' stroke-opacity='.7'/>"
                 f"<circle cx='{x + cw / 2}' cy='54' r='29' fill='none' stroke='{RB}' stroke-opacity='.6' stroke-dasharray='1 6' stroke-linecap='round'>"
                 f"<animateTransform attributeName='transform' type='rotate' from='0 {x + cw / 2} 54' to='360 {x + cw / 2} 54' dur='{22 + i * 3}s' repeatCount='indefinite'/></circle>"
                 f"{icon(ic, x + cw / 2, 54, 22, P['w'], 1.5)}"
                 + runs(s, x + cw / 2 + 2, 104, [(lab, "mono", 700, P["g3"]), ("  ·  ", "mono", 700, P["g5"]), (jp, "kanji", 700, RB)], 11.5, track=3)
                 + "".join(s.text(x + cw / 2, 130 + j * 20, ln, "sans", 600, 15.5, P["w"]) for j, ln in enumerate(lines))
                 + f"<rect x='{x + cw / 2 - 18}' y='8' width='36' height='3' rx='1.5' fill='{RB}'/>")
        s.add(f"<g class='bob' style='animation-delay:{d};animation-duration:{6 + i * .6}s'>{inner}</g>")
    s.d(f"<pattern id='shippo2' width='36' height='36' patternUnits='userSpaceOnUse'><g fill='none' stroke='{RB}' stroke-opacity='.08'>"
        "<circle cx='0' cy='0' r='18'/><circle cx='36' cy='0' r='18'/><circle cx='0' cy='36' r='18'/><circle cx='36' cy='36' r='18'/><circle cx='18' cy='18' r='18'/></g></pattern>")
    return s


# ------------------------------------------------------------------ stack
def marquee(src=None, name="Stack"):
    items = [t.upper() for t in (src or CFG["stack"])]
    track, size, gap = 2, 14, 28
    s = Svg(W, 64, name, rx=12)
    edge_mask(s, "m", 64)
    x, parts = 0, []
    for t in items:
        tw = s.w_("mono", 700, t, size, track)
        parts.append(s.text(x, 38, t, "mono", 700, size, P["w"], anchor="start", track=track))
        x += tw + gap
        parts.append(sakura_flower(x, 33, 6.5, P["pk"], "#ff3b57"))
        x += gap
    loop = x
    s.add(s.frame(brackets=False))
    one = "".join(parts)
    s.add(f"<g mask='url(#m)'><g><animateTransform attributeName='transform' type='translate' from='0 0' to='-{loop:.1f} 0' dur='{loop / 42:.1f}s' repeatCount='indefinite'/>"
          f"<g>{one}</g><g transform='translate({loop:.1f} 0)'>{one}</g><g transform='translate({2 * loop:.1f} 0)'>{one}</g></g></g>")
    return s


def stack_cards(layers=None, name="Stack por camada"):
    layers = layers or CFG["layers"]
    cw, gap, ch = 384, 24, 190
    rows = (len(layers) + 2) // 3
    s = Svg(W, rows * ch + (rows - 1) * gap + 16, name, rx=14)
    s.style(COMMON_CSS)
    s.d(f"<linearGradient id='bg' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='{P['bg0']}'/><stop offset='.6' stop-color='{P['bg1']}'/><stop offset='1' stop-color='{P['bg2']}'/></linearGradient>")
    s.d(f"<linearGradient id='bd' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='{RB}' stop-opacity='.8'/><stop offset='1' stop-color='{RD}' stop-opacity='.1'/></linearGradient>")
    s.d(f"<pattern id='shippo2' width='36' height='36' patternUnits='userSpaceOnUse'><g fill='none' stroke='{RB}' stroke-opacity='.08'>"
        "<circle cx='0' cy='0' r='18'/><circle cx='36' cy='0' r='18'/><circle cx='0' cy='36' r='18'/><circle cx='36' cy='36' r='18'/><circle cx='18' cy='18' r='18'/></g></pattern>")
    for i, (title, ic, techs, jp) in enumerate(layers):
        x, y = (i % 3) * (cw + gap), 8 + (i // 3) * (ch + gap)
        lines = wrap("mono", 400, " · ".join(techs), 13, cw - 56)
        body = "".join(s.text(x + cw / 2, y + 152 + j * 21, ln, "mono", 400, 13, P["g1"]) for j, ln in enumerate(lines))
        cid = s.uid("sc")
        s.d(f"<clipPath id='{cid}'><rect x='{x}' y='{y}' width='{cw}' height='{ch}' rx='14'/></clipPath>")
        inner = (f"<rect x='{x}' y='{y}' width='{cw}' height='{ch}' rx='14' fill='url(#bg)'/>"
                 f"<g clip-path='url(#{cid})'><rect x='{x}' y='{y}' width='{cw}' height='{ch}' fill='url(#shippo2)'/>"
                 f"<path d='M{x} {y + ch - 20}h{cw}' stroke='{RB}' stroke-opacity='.12'/></g>"
                 f"<rect x='{x + .5}' y='{y + .5}' width='{cw - 1}' height='{ch - 1}' rx='13.5' fill='none' stroke='url(#bd)' stroke-width='1.1'/>"
                 f"<circle cx='{x + cw / 2}' cy='{y + 48}' r='23' fill='{RB}' fill-opacity='.10' stroke='{RB}' stroke-opacity='.7'/>"
                 f"<circle cx='{x + cw / 2}' cy='{y + 48}' r='29' fill='none' stroke='{RB}' stroke-dasharray='1 6' stroke-linecap='round' stroke-opacity='.8'>"
                 f"<animateTransform attributeName='transform' type='rotate' from='0 {x + cw / 2} {y + 48}' to='360 {x + cw / 2} {y + 48}' dur='{26 + i * 3}s' repeatCount='indefinite'/></circle>"
                 f"{icon(ic, x + cw / 2, y + 48, 22, P['w'], 1.5)}"
                 + s.text(x + cw / 2 + 2, y + 104, title, "display", 700, 14.5, P["w"], track=4)
                 + s.jp(x + cw / 2 + 2, y + 126, jp, 12.5, RB, track=3) + body
                 + f"<rect x='{x + cw / 2 - 18}' y='{y}' width='36' height='3' rx='1.5' fill='{RB}'/>")
        s.add(f"<g class='bob' style='animation-delay:{i * .5}s;animation-duration:{6.5 + i * .4}s'>{inner}</g>")
    return s


# ------------------------------------------------------------------ typing
def typing(lines, name, size=19, hold=1.5):
    s = Svg(W, 60, name, rx=30)
    adv = s.w_("mono", 400, "M", size)
    s.used.setdefault(("mono", 400), set()).update("".join(lines))
    maxn = max(len(t) for t in lines)
    pw = maxn * adv + 190
    px = (W - pw) / 2
    ty = 30 + size * .34
    t_type, t_erase = .055, .025
    slots, t = [], .6
    for ln in lines:
        n = len(ln)
        slots.append((t, n))
        t += n * t_type + hold + n * t_erase + .35
    T = t
    s.style(".blink{animation:bl 1s steps(1) infinite}@keyframes bl{0%,100%{opacity:1}50%{opacity:0}}"
            ".rec{animation:rc 2s ease-in-out infinite}@keyframes rc{0%,100%{opacity:1}50%{opacity:.25}}")
    s.d(f"<linearGradient id='bg' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='{P['bg0']}'/><stop offset='.6' stop-color='{P['bg1']}'/><stop offset='1' stop-color='{P['bg2']}'/></linearGradient>")
    s.d("<linearGradient id='bd' x1='0' x2='1'><stop offset='0' stop-color='#8a0f24' stop-opacity='.2'/><stop offset='.5' stop-color='#ff3b57' stop-opacity='.9'/><stop offset='1' stop-color='#8a0f24' stop-opacity='.2'/></linearGradient>")
    s.add(f"<rect x='{px}' y='3' width='{pw}' height='54' rx='27' fill='url(#bg)'/><rect x='{px + .5}' y='3.5' width='{pw - 1}' height='53' rx='26.5' fill='none' stroke='url(#bd)' stroke-width='1.2'/>"
          f"<rect x='{px + 4}' y='7' width='{pw - 8}' height='46' rx='23' fill='none' stroke='{RB}' stroke-opacity='.15'/>")
    s.add(icon("terminal", px + 40, 30, 18, RB, 1.6))
    s.add(f"<g transform='translate({px + pw - 40} 30)'>{sakura_flower(0, 0, 8, P['pk'], '#ff3b57', 18)}</g>")
    s.add(f"<circle class='rec' cx='{px + pw - 66}' cy='30' r='3.2' fill='{RB}'/>")
    for i, (ln, (st, n)) in enumerate(zip(lines, slots)):
        x0 = 600 - n * adv / 2
        times, vals = [0.0], [0.0]
        for k in range(1, n + 1):
            times.append(st + k * t_type); vals.append(k * adv)
        he = st + n * t_type + hold
        for k in range(1, n + 1):
            times.append(he + k * t_erase); vals.append((n - k) * adv)
        kt = ";".join(f"{v / T:.5f}" for v in times)
        vv = ";".join(f"{v:.2f}" for v in vals)
        cid = f"c{i}"
        s.d(f"<clipPath id='{cid}'><rect x='{x0:.2f}' y='0' width='0' height='60'><animate attributeName='width' calcMode='discrete' values='{vv}' keyTimes='{kt}' dur='{T:.2f}s' repeatCount='indefinite'/></rect></clipPath>")
        s.add(f"<g clip-path='url(#{cid})'>" + s.text(f"{x0:.2f}", f"{ty:.1f}", ln, "mono", 400, size, P["w"], anchor="start") + "</g>")
        xs = ";".join(f"{x0 + v:.2f}" for v in vals)
        ov = ";".join("1" if 0 < v else "0" for v in vals)
        s.add(f"<g class='blink'><rect y='{ty - size * .85:.1f}' width='2' height='{size * 1.1:.1f}' fill='{RB}' x='{x0:.2f}'>"
              f"<animate attributeName='x' calcMode='discrete' values='{xs}' keyTimes='{kt}' dur='{T:.2f}s' repeatCount='indefinite'/>"
              f"<animate attributeName='opacity' calcMode='discrete' values='{ov}' keyTimes='{kt}' dur='{T:.2f}s' repeatCount='indefinite'/></rect></g>")
    return s


# ------------------------------------------------------------------ hero banner
def banner():
    H = 520
    s = Svg(W, H, f"{CFG['name']} · {' '.join(CFG['role'])}")
    s.shimmer("sh", 6.5, "#ffe0e3")
    comet_defs(s)
    s.d(sun_defs("sun") + lantern_defs())
    s.d("<linearGradient id='sky' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#4a0814' stop-opacity='.55'/><stop offset='.5' stop-color='#b3162f' stop-opacity='.15'/><stop offset='1' stop-color='#ff3b57' stop-opacity='.55'/></linearGradient>")
    s.d("<linearGradient id='mist' x1='0' x2='1'><stop offset='0' stop-color='#ff7a8c' stop-opacity='0'/><stop offset='.5' stop-color='#ff7a8c' stop-opacity='.22'/><stop offset='1' stop-color='#ff7a8c' stop-opacity='0'/></linearGradient>")
    s.d("<linearGradient id='sweep' x1='0' x2='1'><stop offset='0' stop-color='#fff' stop-opacity='0'/><stop offset='.5' stop-color='#fff' stop-opacity='.16'/><stop offset='1' stop-color='#fff' stop-opacity='0'/></linearGradient>")
    s.d(f"<linearGradient id='ln' x1='0' x2='1'><stop offset='0' stop-color='#fff' stop-opacity='0'/><stop offset='.5' stop-color='{RB}' stop-opacity='.95'/><stop offset='1' stop-color='#fff' stop-opacity='0'/></linearGradient>")
    s.d("<radialGradient id='vg'><stop offset='.55' stop-color='#fff'/><stop offset='1' stop-color='#000'/></radialGradient>")
    cid = s.clip_round()
    track, tsz = 14, 148
    ttl = CFG["name"]
    tw0 = measure("display", 700, ttl, tsz, track)
    if tw0 > 860:
        k = 860 / tw0
        tsz, track = tsz * k, track * k
    tw = s.w_("display", 700, ttl, tsz, track)
    s.style(COMMON_CSS + f".title{{animation:tt 2.6s cubic-bezier(.16,.84,.24,1) both}}@keyframes tt{{from{{letter-spacing:70px;opacity:0}}to{{letter-spacing:{track}px;opacity:1}}}}"
            ".draw{transform-origin:center;transform-box:fill-box;transform:scaleX(0);animation:dr 1.8s .9s cubic-bezier(.16,.84,.24,1) forwards}@keyframes dr{to{transform:scaleX(1)}}"
            ".chip{opacity:0;animation:fi .9s ease forwards}.cb{animation:bob 5.5s ease-in-out infinite}"
            ".blink{animation:bl 1s steps(1) infinite}@keyframes bl{0%,100%{opacity:1}50%{opacity:0}}")
    s.add(s.panel(colors=HOT))
    s.add(f"<g clip-path='url(#{cid})'>")
    s.add(f"<rect width='{W}' height='{H}' fill='url(#sky)'/>")
    s.add(sun(600, 168, 122, True, .8, "sun", 100, 2.7))
    for k in range(3):   # anéis de pulso saindo do sol
        s.add(f"<circle cx='600' cy='168' r='122' fill='none' stroke='#ffb3b9' stroke-width='1.4'><animate attributeName='r' values='122;330' dur='6s' begin='{k * 2}s' repeatCount='indefinite'/>"
              f"<animate attributeName='opacity' values='.55;0' dur='6s' begin='{k * 2}s' repeatCount='indefinite'/></circle>")
    s.add(f"<ellipse cx='600' cy='250' rx='520' ry='150' fill='none' stroke='#ffd6d6' stroke-opacity='.45' stroke-dasharray='2 9' stroke-linecap='round'>"
          "<animateTransform attributeName='transform' type='rotate' from='0 600 250' to='360 600 250' dur='90s' repeatCount='indefinite'/></ellipse>")
    s.add("<circle r='3.4' fill='#fff'><animateMotion dur='14s' repeatCount='indefinite' path='M80 250 a520 150 0 1 0 1040 0 a520 150 0 1 0 -1040 0'/></circle>")
    for k, (yy, dd) in enumerate([(150, 22), (300, 30), (400, 26)]):   # névoa vermelha andando
        s.add(f"<rect x='-600' y='{yy}' width='1200' height='46' fill='url(#mist)'><animateTransform attributeName='transform' type='translate' from='0 0' to='1800 0' dur='{dd}s' begin='-{k * 7}s' repeatCount='indefinite'/></rect>")
    # mountains (back -> front)
    s.add(fuji(335, 478, .62, "#b82442", "#ffd6d6", .7) + fuji(880, 478, .56, "#b82442", "#ffd6d6", .7))
    s.add(fuji(150, 480, 1.2, "#8a1730") + fuji(1060, 480, 1.1, "#7a1229"))
    s.add(torii(112, 484, .62, "#3a0612", "#ffd6d6", .95) + torii(1088, 484, .62, "#3a0612", "#ffd6d6", .95))
    s.add(waves(W, 468, 24, 3, "#e02a4a", "#7a1229", "#ffe3e6", .34, 18, "hw"))
    s.add(f"<rect x='0' y='{H - 4}' width='{W}' height='4' fill='#7a1229' opacity='.5'/>")
    s.add(embers(40, 11, 60, 1140, 260, 490))
    # lanterns
    s.add(lantern(70, 10, 54, 0, "玄", s.used) + lantern(1130, 10, 54, 1.4, "玄", s.used)
          + lantern(150, 4, 38, .7, "祭", s.used, 3) + lantern(1050, 4, 38, 2.1, "祭", s.used, 3))
    s.add(petals(24, 8, 100, 1100, -10, 0, 1.0, dur=(8, 14), fall=H + 20))
    s.add(f"<rect x='-300' y='-20' width='260' height='{H + 40}' fill='url(#sweep)' transform='skewX(-20)'><animateTransform attributeName='transform' type='translate' values='0 0;1700 0;1700 0' keyTimes='0;.45;1' dur='7s' repeatCount='indefinite' additive='sum'/></rect>")
    s.add("</g>")
    # eyebrow
    ew = s.w_("sans", 600, CFG["eyebrow"], 12, 5) + 30
    s.add(f"<g class='fade' style='animation-delay:.3s'>{runs(s, 600, 66, [(JP, 'kanji', 700, R_), ('   ·   ' + CFG['eyebrow'], 'sans', 600, P['g2'])], 12, track=5)}"
          f"<rect x='{600 - ew / 2 - 96}' y='62' width='64' height='1' fill='url(#ln)'/><rect x='{600 + ew / 2 + 32}' y='62' width='64' height='1' fill='url(#ln)'/></g>")
    s.add(s.text(600 + track / 2, 214, ttl, "display", 700, tsz, "url(#sh)", track=track, cls="title"))
    lw = max(tw, 560)
    s.add(f"<rect class='draw' x='{600 - lw / 2}' y='236' width='{lw}' height='2' fill='url(#ln)'/>")
    s.add(f"<g opacity='.9'>{comet(560, 1100, 236.2, 5, 1.2, 150, 1.8)}</g>")
    s.add(f"<g class='fade' style='animation-delay:.9s'>{s.jp(600 + 5, 276, CFG['kana'], 21, P['g1'], track=10)}</g>")
    a, amp, b = CFG["role"]
    s.add(runs(s, 600, 322, [(a + " ", "sans", 600, P["w"]), (amp + " ", "sans", 600, P["g3"]), (b, "sans", 600, P["w"])], 29, cls="fade", style="animation-delay:1.1s"))
    s.add(s.text(600, 352, CFG["sub"], "sans", 500, 15.5, P["g1"], cls="fade", style="animation-delay:1.5s"))
    chips = []
    for ic, lab in CFG["chips"]:
        tw_ = s.w_("mono", 700, lab, 11.5, 2)
        chips.append((ic, lab, 14 + 18 + 10 + tw_ + 18))
    gapc = 14
    tot = sum(c[2] for c in chips) + gapc * (len(chips) - 1)
    x = 600 - tot / 2
    for i, (ic, lab, cw) in enumerate(chips):
        s.add(f"<g class='chip' style='animation-delay:{1.7 + i * .15}s'><g class='cb' style='animation-delay:{i * .4}s'>"
              f"<rect x='{x:.1f}' y='374' width='{cw:.1f}' height='38' rx='19' fill='#1d0409' fill-opacity='.55' stroke='{RB}' stroke-opacity='.7'/>"
              f"{icon(ic, x + 14 + 9, 393, 17, RB, 1.6)}"
              + s.text(f"{x + 14 + 18 + 10:.1f}", 397.5, lab, "mono", 700, 11.5, P["w"], anchor="start", track=2) + "</g></g>")
        x += cw + gapc
    tag = CFG["tagline"]
    tgw = s.w_("mono", 400, tag, 13, 0)
    s.add(f"<g class='fade' style='animation-delay:2.3s'>{s.text(600, 446, tag, 'mono', 400, 13, P['g1'])}"
          f"<g class='blink'><rect x='{600 + tgw / 2 + 5:.1f}' y='435' width='7' height='13' fill='{RB}'/></g></g>")
    # side ornaments: vertical JP (right + left), hanko seals, vertical latin
    for j, ch in enumerate(CFG["vertical_jp"]):
        s.add(s.jp(1152, 150 + j * 27, ch, 20, P["g1"]))
    s.add(s.seal(1152, 334, 28))
    for j, ch in enumerate(CFG["vertical_jp_l"]):
        s.add(s.jp(86, 150 + j * 27, ch, 20, P["g1"]))
    s.add(s.seal(86, 300, 24, "紅", 3))
    s.add(f"<g transform='rotate(-90 50 230)'>{s.text(50, 230, CFG['side_text'], 'mono', 700, 11, P['g3'], track=6)}</g>")
    s.add(s.border())
    s.add(s.grain())
    return s


# ------------------------------------------------------------------ cta
def s_w(font, weight, text, size, track):
    return measure(font, weight, text, size, track)


def cta(l, r, ic="globe", CW=W):
    size, track = 15, 3
    lw, rw = s_w("display", 700, l, size, track), s_w("display", 700, r, size, track)
    left_w = 34 + 20 + lw + 30
    bw = left_w + 20 + rw + 18 + 16 + 26
    s = Svg(CW, 100, "")
    s.style(COMMON_CSS)
    x = (CW - bw) / 2
    y, h = 22, 56
    s.d(f"<linearGradient id='bgd' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='{P['bg0']}'/><stop offset='1' stop-color='{P['bg2']}'/></linearGradient>")
    s.d("<linearGradient id='rg' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='#ff3b57'/><stop offset='.6' stop-color='#dc143c'/><stop offset='1' stop-color='#a50f2a'/></linearGradient>")
    s.d("<linearGradient id='gl' x1='0' x2='1'><stop offset='0' stop-color='#fff' stop-opacity='0'/><stop offset='.5' stop-color='#fff' stop-opacity='.4'/><stop offset='1' stop-color='#fff' stop-opacity='0'/></linearGradient>")
    s.add(f"<rect x='{x}' y='{y}' width='{bw}' height='{h}' rx='{h / 2}' fill='none' stroke='{RB}'><animate attributeName='opacity' values='.6;0' dur='2.6s' repeatCount='indefinite'/><animate attributeName='stroke-width' values='1;12' dur='2.6s' repeatCount='indefinite'/></rect>")
    s.add(f"<clipPath id='cp'><rect x='{x}' y='{y}' width='{bw}' height='{h}' rx='{h / 2}'/></clipPath>")
    s.add(f"<g clip-path='url(#cp)'><rect x='{x}' y='{y}' width='{bw}' height='{h}' fill='url(#bgd)'/><rect x='{x + left_w}' y='{y}' width='{bw - left_w}' height='{h}' fill='url(#rg)'/>"
          f"<path d='M{x + left_w} {y}l-10 {h}' stroke='#fff' stroke-opacity='.25'/>"
          f"<g><animateTransform attributeName='transform' type='translate' values='-120 0;{bw + 120} 0;{bw + 120} 0' keyTimes='0;.4;1' dur='5s' repeatCount='indefinite'/>"
          f"<rect x='{x}' y='{y - 4}' width='34' height='{h + 8}' fill='url(#gl)' transform='skewX(-20)'/></g></g>")
    s.add(f"<rect x='{x + .5}' y='{y + .5}' width='{bw - 1}' height='{h - 1}' rx='{h / 2 - .5}' fill='none' stroke='{RB}' stroke-opacity='.8'/>")
    s.add(icon(ic, x + 34, y + h / 2, 20, RB, 1.6))
    s.add(s.text(f"{x + 34 + 20:.1f}", y + h / 2 + 5.3, l, "display", 700, size, P["w"], anchor="start", track=track))
    s.add(s.text(f"{x + left_w + 20:.1f}", y + h / 2 + 5.3, r, "display", 700, size, "#fff", anchor="start", track=track))
    s.add(f"<g>{icon('send', x + bw - 34, y + h / 2, 16, '#fff', 2)}</g>")
    return s


# ------------------------------------------------------------------ fluxer
def bubble(s, x, y, w, h, side, light=False, delay=0, dots=False, lines=(.62, .42)):
    face = "url(#face)" if not light else P["g1"]
    cx = x - 38 if side == "l" else x + w + 38
    av = (f"<circle cx='{cx}' cy='{y + h / 2}' r='17' fill='url(#face)' stroke='#ffb3b9' stroke-opacity='.4'/>"
          f"<circle cx='{cx}' cy='{y + h / 2 - 4}' r='5.5' fill='{P['g1']}'/><path d='M{cx - 9} {y + h / 2 + 11} a9 7.5 0 0 1 18 0z' fill='{P['g1']}'/>")
    body = s.extrude(x, y, w, h, 20, face, 9)
    if dots:
        body += "".join(f"<circle cx='{x + 28 + k * 16}' cy='{y + h / 2}' r='4.2' fill='{P['g1']}'><animate attributeName='opacity' values='.2;1;.2' dur='1.2s' begin='{k * .2}s' repeatCount='indefinite'/></circle>" for k in range(3))
    else:
        c1, c2 = (P["bg1"], P["g4"]) if light else (P["w"], P["g3"])
        body += (f"<rect x='{x + 20}' y='{y + h / 2 - 12}' width='{(w - 40) * lines[0]:.0f}' height='6' rx='3' fill='{c1}'/>"
                 f"<rect x='{x + 20}' y='{y + h / 2 + 3}' width='{(w - 40) * lines[1]:.0f}' height='6' rx='3' fill='{c2}'/>")
    cid = s.uid("k")
    body += (f"<clipPath id='{cid}'><rect x='{x}' y='{y}' width='{w}' height='{h}' rx='20'/></clipPath><g clip-path='url(#{cid})'><g>"
             f"<animateTransform attributeName='transform' type='translate' values='-{w + 40} 0;{w + 40} 0;{w + 40} 0' keyTimes='0;.35;1' dur='5.5s' begin='{delay + .4}s' repeatCount='indefinite'/>"
             f"<rect x='{x - 20}' y='{y - 20}' width='28' height='{h + 40}' fill='url(#gl)' transform='skewX(-20)'/></g></g>")
    s.add(f"<g><animateTransform attributeName='transform' type='translate' values='0 0;0 -8;0 0' keyTimes='0;.5;1' calcMode='spline' keySplines='.45 0 .55 1;.45 0 .55 1' dur='6.5s' begin='{delay}s' repeatCount='indefinite'/>{av}{body}</g>")


def tile3d(s, x, y, size, ic, delay=0, label=""):
    cid = s.uid("k")
    body = s.extrude(x, y, size, size, 20, "url(#face)", 10)
    body += icon(ic, x + size / 2, y + size / 2, size * .46, RB, 2.2)
    body += f"<rect x='{x}' y='{y}' width='{size}' height='{size}' rx='20' fill='none' stroke='{RB}' stroke-opacity='.7'/>"
    body += (f"<clipPath id='{cid}'><rect x='{x}' y='{y}' width='{size}' height='{size}' rx='20'/></clipPath><g clip-path='url(#{cid})'><g>"
             f"<animateTransform attributeName='transform' type='translate' values='-{size + 40} 0;{size + 40} 0;{size + 40} 0' keyTimes='0;.35;1' dur='5.5s' begin='{delay + .4}s' repeatCount='indefinite'/>"
             f"<rect x='{x - 20}' y='{y - 20}' width='24' height='{size + 40}' fill='url(#gl)' transform='skewX(-20)'/></g></g>")
    if label:
        body += s.text(x + size / 2 - 1, y + size + 28, label, "mono", 700, 10, RB, track=3)
    s.add(f"<g><animateTransform attributeName='transform' type='translate' values='0 0;0 -8;0 0' keyTimes='0;.5;1' calcMode='spline' keySplines='.45 0 .55 1;.45 0 .55 1' dur='6.5s' begin='{delay}s' repeatCount='indefinite'/>{body}</g>")


def fluxer():
    F = CFG["fluxer"]
    H = 430
    s = Svg(W, H, "Comunidade GennisCode no Fluxer")
    s.shimmer("sh", 6, "#ffe0e3")
    s.d(sun_defs("fs") + lantern_defs())
    s.d(f"<linearGradient id='face' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='#c8183a'/><stop offset='1' stop-color='#4a0b18'/></linearGradient>")
    s.d("<linearGradient id='gl' x1='0' x2='1'><stop offset='0' stop-color='#fff' stop-opacity='0'/><stop offset='.5' stop-color='#fff' stop-opacity='.32'/><stop offset='1' stop-color='#fff' stop-opacity='0'/></linearGradient>")
    s.d("<linearGradient id='rg' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='#ff3b57'/><stop offset='.6' stop-color='#dc143c'/><stop offset='1' stop-color='#a50f2a'/></linearGradient>")
    cid = s.clip_round()
    s.style(COMMON_CSS + ".t1{animation:tt 2.4s cubic-bezier(.16,.84,.24,1) both}.t2{animation:tt 2.4s .25s cubic-bezier(.16,.84,.24,1) both}"
            "@keyframes tt{from{letter-spacing:30px;opacity:0}to{letter-spacing:3px;opacity:1}}")
    s.add(s.panel())
    s.add(f"<g clip-path='url(#{cid})'>{sun(600, 205, 118, True, .42, 'fs', 110, 2.6)}"
          f"{torii(600, 396, 1.9, '#2a0509', RB, .55)}"
          f"<ellipse cx='600' cy='214' rx='340' ry='160' fill='none' stroke='{R_}' stroke-opacity='.7' stroke-width='1.1' stroke-dasharray='2 9' stroke-linecap='round'>"
          "<animateTransform attributeName='transform' type='rotate' from='0 600 214' to='360 600 214' dur='70s' repeatCount='indefinite'/></ellipse>"
          f"{waves(W, 392, 15, 3, '#b3162f', '#3a0a15', '#ffd6d6', .28, 20, 'fw')}"
          f"{embers(14, 5, 200, 1000, 260, 400)}</g>")
    s.add(lantern(330, 6, 40, 0, "玄", s.used, 3) + lantern(870, 6, 40, 1.3, "玄", s.used, 3))
    bubble(s, 84, 78, 214, 58, "l", False, 0)
    bubble(s, 118, 176, 178, 52, "l", False, .8, dots=True)
    tile3d(s, 100, 262, 84, "chat", 1.6, "FLUXER")
    bubble(s, 902, 104, 214, 58, "r", True, .4, lines=(.66, .5))
    bubble(s, 930, 204, 170, 52, "r", False, 1.2, lines=(.55, .35))
    tile3d(s, 1016, 272, 84, "camera", 2, "INSTAGRAM")
    s.add(f"<g clip-path='url(#{cid})'>{petals(10, 17, 120, 1080, -10, 0, .9, dur=(9, 14), fall=H + 20)}</g>")
    s.add(f"<g class='fade' style='animation-delay:.2s'>{runs(s, 600, 66, [(JP, 'kanji', 700, R_), ('   ·   ' + F['eyebrow'], 'sans', 600, P['g2'])], 12, track=5)}</g>")
    s.add(s.text(600 + 1.5, 142, F["l1"], "display", 700, 46, "url(#sh)", track=3, cls="t1"))
    s.add(s.text(600 + 1.5, 196, F["l2"], "display", 700, 46, P["rb"], track=3, cls="t2"))
    s.add(s.text(600, 244, F["line1"], "sans", 600, 19, P["w"], cls="fade", style="animation-delay:1s"))
    s.add(s.text(600, 271, F["line2"], "sans", 500, 14.5, P["g1"], cls="fade", style="animation-delay:1.3s"))
    bw = s.w_("display", 700, F["button"] + "  →", 14, 3) + 64
    bx = 600 - bw / 2
    s.add(f"<g class='fade' style='animation-delay:1.6s'><rect x='{bx}' y='296' width='{bw}' height='46' rx='23' fill='none' stroke='{RB}'>"
          "<animate attributeName='opacity' values='.7;0' dur='2.4s' repeatCount='indefinite'/><animate attributeName='stroke-width' values='1;10' dur='2.4s' repeatCount='indefinite'/></rect>"
          f"<rect x='{bx}' y='296' width='{bw}' height='46' rx='23' fill='url(#rg)' stroke='#ffb3b9' stroke-opacity='.5'/>"
          + s.text(600 + 1.5, 324, F["button"] + "  →", "display", 700, 14, "#fff", track=3)
          + s.text(600, 368, F["url"], "mono", 400, 13, P["g1"]) + "</g>")
    s.add(s.seal(1150, 376, 24))
    s.add(s.seal(50, 376, 22, "紅", 3))
    s.add(s.border())
    s.add(s.grain())
    return s


# ------------------------------------------------------------------ footer
def footer():
    F = CFG["footer"]
    H = 344
    s = Svg(W, H, "Aprenda. Construa. Compartilhe. " + F["copyright"])
    s.shimmer("sh", 7, "#ffe0e3")
    s.d(sun_defs("ft") + lantern_defs())
    s.d(f"<linearGradient id='ln' x1='0' x2='1'><stop offset='0' stop-color='#fff' stop-opacity='0'/><stop offset='.5' stop-color='{RB}' stop-opacity='.95'/><stop offset='1' stop-color='#fff' stop-opacity='0'/></linearGradient>")
    s.d("<linearGradient id='sky' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#0f0207' stop-opacity='.8'/><stop offset='.6' stop-color='#4a0a18' stop-opacity='.2'/><stop offset='1' stop-color='#c01836' stop-opacity='.65'/></linearGradient>")
    s.d("<linearGradient id='strip' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#2a050c'/><stop offset='1' stop-color='#12030a'/></linearGradient>")
    cid = s.clip_round()
    s.style(COMMON_CSS + ".f{opacity:0;animation:fi 1.6s .2s ease forwards}.dr{transform-origin:center;transform-box:fill-box;transform:scaleX(0);animation:dd 1.4s 1s cubic-bezier(.16,.84,.24,1) forwards}@keyframes dd{to{transform:scaleX(1)}}")
    s.add(s.panel())
    s.add(f"<g clip-path='url(#{cid})'>")
    s.add(f"<rect width='{W}' height='{H}' fill='url(#sky)'/>")
    s.add(sun(600, 262, 78, True, .85, "ft", 110, 3.2))
    s.add(fuji(330, 250, .8, "#7a1830", "#ffc2cc", .55) + fuji(880, 250, .72, "#7a1830", "#ffc2cc", .55))
    s.add(fuji(150, 252, 1.45, "#5c0f22") + fuji(1060, 252, 1.3, "#4e0c1d"))
    s.add(torii(300, 256, .7, "#1d0409", RB, .95) + torii(900, 256, .7, "#1d0409", RB, .95))
    s.add(waves(W, 232, 20, 3, "#b3162f", "#3a0a15", "#ffd6d6", .30, 20, "fw"))
    s.add(f"<rect x='0' y='286' width='{W}' height='{H - 286}' fill='url(#strip)'/>")
    s.add(f"<rect x='0' y='286' width='{W}' height='1' fill='url(#ln)'/>")
    s.add(embers(16, 33, 120, 1080, 160, 280))
    s.add(petals(10, 6, 100, 1100, -10, 0, 1.0, dur=(9, 15), fall=300))
    s.add("</g>")
    s.add(lantern(66, 8, 50, 0, "玄", s.used) + lantern(1134, 8, 50, 1.2, "玄", s.used))
    s.add(f"<g class='f'>{s.jp(600 + 4, 64, F['jp'], 20, P['g1'], track=8)}</g>")
    s.add(runs(s, 600, 122, [(F["a"] + " ", "display", 700, P["w"]), (F["b"], "display", 700, RB)], 50, track=-.5, cls="f"))
    s.add(s.text(600, 154, F["sub"], "sans", 500, 15, P["g1"], cls="f", style="animation-delay:.5s"))
    n, gp = len(F["icons"]), 46
    x0 = 600 - (n - 1) * gp / 2
    for i, ic in enumerate(F["icons"]):
        s.add(f"<g class='bob' style='animation-delay:{i * .5}s'>{icon(ic, x0 + i * gp, 188, 18, RB, 1.6)}</g>")
    s.add("<rect class='dr' x='520' y='168' width='160' height='1.5' fill='url(#ln)'/>")
    s.add(runs(s, 600, 308, [(JP, "kanji", 700, R_), ("   ·   " + F["credit"], "mono", 700, P["g3"])], 11.5, track=4.5))
    s.add(s.text(600, 330, F["copyright"], "sans", 500, 13, P["g1"], track=.3))
    s.add(s.border())
    s.add(s.grain())
    return s


# ------------------------------------------------------------------ team
def member(name, handle, photo, role=""):
    import base64 as _b
    s = Svg(240, 232, name, rx=14)
    s.style(COMMON_CSS + ".ph{animation:bob 6s ease-in-out infinite}.ring{transform-origin:120px 80px;animation:spin 30s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}")
    s.d(f"<linearGradient id='bg' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='{P['bg0']}'/><stop offset='.6' stop-color='{P['bg1']}'/><stop offset='1' stop-color='{P['bg2']}'/></linearGradient>")
    s.d(f"<linearGradient id='bd' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='{RB}' stop-opacity='.85'/><stop offset='1' stop-color='{RD}' stop-opacity='.15'/></linearGradient>")
    s.d("<radialGradient id='pg'><stop offset='0' stop-color='#ff3b57' stop-opacity='.45'/><stop offset='1' stop-color='#ff3b57' stop-opacity='0'/></radialGradient>")
    s.d("<clipPath id='pc'><circle cx='120' cy='80' r='47'/></clipPath>")
    cid = s.clip_round()
    b64 = _b.b64encode(open(os.path.join(HERE, "src", "photos", photo), "rb").read()).decode()
    s.add(s.panel())
    s.add(f"<g clip-path='url(#{cid})'>{waves(240, 214, 8, 2, '#8c1428', '#3a0a15', '#ffd6d6', .25, 14, 'mw')}{petals(3, hash(name) % 97, 20, 220, -6, 0, .55, dur=(7, 11), fall=240)}</g>")
    s.add("<circle cx='120' cy='80' r='80' fill='url(#pg)'/>")
    s.add(f"<g class='ph'><circle class='ring' cx='120' cy='80' r='58' fill='none' stroke='{RB}' stroke-width='1.4' stroke-dasharray='2 7' stroke-linecap='round'/>"
          f"<image href='data:image/jpeg;base64,{b64}' x='71' y='31' width='98' height='98' preserveAspectRatio='xMidYMid slice' clip-path='url(#pc)'/>"
          f"<circle cx='120' cy='80' r='48' fill='none' stroke='{RB}' stroke-width='2.4'/></g>")
    size = 15 if len(name) < 20 else 14
    s.add(s.text(120, 172, name, "display", 700, size, P["w"], track=.5))
    s.add(f"<rect x='90' y='184' width='60' height='1.5' rx='.75' fill='{RB}'/>")
    s.add(s.text(120, 206, handle, "mono", 400, 12, RB))
    if role:
        s.add(s.text(120, 224, role, "sans", 600, 11, P["g3"]))
    s.add(f"<rect x='104' y='0' width='32' height='3' rx='1.5' fill='{RB}'/>")
    s.add(s.seal(216, 22, 16))
    s.add(s.border(inner=False, brackets=False))
    return s


# ------------------------------------------------------------------ platforms (rebuilt: crimson 3D devices, each with its own animation)
def _dev_defs(s):
    s.d("<linearGradient id='dface' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='#d01a3d'/><stop offset='1' stop-color='#5a0b1b'/></linearGradient>")
    s.d("<linearGradient id='dscr' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='#a0112c'/><stop offset='.55' stop-color='#4a0a18'/><stop offset='1' stop-color='#1d0409'/></linearGradient>")
    s.d("<linearGradient id='gl' x1='0' x2='1'><stop offset='0' stop-color='#fff' stop-opacity='0'/><stop offset='.5' stop-color='#fff' stop-opacity='.3'/><stop offset='1' stop-color='#fff' stop-opacity='0'/></linearGradient>")
    s.d("<filter id='blur' x='-50%' y='-50%' width='200%' height='200%'><feGaussianBlur stdDeviation='6'/></filter>")


EXT = dict(ex=.9, ey=-.9)


def _typed(s, x, y, txt, fill, t0, t1, T, size=11):
    adv = measure("mono", 400, "M", size)
    s.used.setdefault(("mono", 400), set()).update(txt)
    wfull = len(txt) * adv + 2
    cid = s.uid("tp")
    kt = f"0;{t0 / T:.4f};{t1 / T:.4f};.94;1"
    s.d(f"<clipPath id='{cid}'><rect x='{x}' y='{y - 12}' width='0' height='16'><animate attributeName='width' values='0;0;{wfull:.1f};{wfull:.1f};0' keyTimes='{kt}' dur='{T}s' repeatCount='indefinite'/></rect></clipPath>")
    return f"<g clip-path='url(#{cid})'>{s.text(x, y, txt, 'mono', 400, size, fill, anchor='start')}</g>"


def _pop(a, T, peak=1.1):
    """keyTimes/values for a scale pop-in that starts at fraction a of the loop."""
    kt = f"0;{a:.3f};{a + .05:.3f};{a + .09:.3f};.88;.95;1"
    return kt, f"0.001;0.001;{peak};1;1;0.001;0.001"


def _dev_linux(s):
    T = 8
    o = s.extrude(-85, -140, 170, 125, 10, "url(#dface)", 14, **EXT)
    o += "<rect x='-85' y='-140' width='170' height='125' rx='10' fill='#1d0409'/>"
    o += f"<path d='M-85 -130 a10 10 0 0 1 10 -10 h150 a10 10 0 0 1 10 10 v12 h-170z' fill='#5c0b1b'/>"
    o += "<circle cx='-70' cy='-129' r='3.2' fill='#ff3b57'/><circle cx='-59' cy='-129' r='3.2' fill='#f0c27b'/><circle cx='-48' cy='-129' r='3.2' fill='#ffd6d6'/>"
    o += s.text(0, -126, "gennis@linux:~", "mono", 400, 8.5, P["g3"])
    o += f"<rect x='-85' y='-140' width='170' height='125' rx='10' fill='none' stroke='#ffb3b9' stroke-opacity='.3'/>"
    o += _typed(s, -74, -100, "$ sudo ./gennis", P["w"], .6, 1.8, T)
    o += _typed(s, -74, -82, "> iniciando curso...", P["g3"], 2.2, 3.6, T)
    o += _typed(s, -74, -64, "> tudo certo ✓", RB, 4.0, 5.0, T)
    o += _typed(s, -74, -46, "$", P["w"], 5.4, 5.6, T)
    o += (f"<g opacity='0'><animate attributeName='opacity' values='0;0;1;1' keyTimes='0;.67;.68;1' dur='{T}s' repeatCount='indefinite'/>"
          f"<rect x='-64' y='-55' width='7' height='12' fill='{RB}'><animate attributeName='opacity' values='1;1;0;0' keyTimes='0;.5;.5;1' dur='1.1s' repeatCount='indefinite'/></rect></g>")
    cid = s.uid("lc")
    o += f"<clipPath id='{cid}'><rect x='-85' y='-140' width='170' height='125' rx='10'/></clipPath><g clip-path='url(#{cid})'>"
    o += (f"<rect x='-85' y='-140' width='170' height='3' fill='{RB}' opacity='.35'><animateTransform attributeName='transform' type='translate' values='0 0;0 125;0 125' keyTimes='0;.7;1' dur='3.2s' repeatCount='indefinite'/></rect>"
          "<g><animateTransform attributeName='transform' type='translate' values='-190 0;190 0;190 0' keyTimes='0;.35;1' dur='5.5s' begin='.5s' repeatCount='indefinite'/>"
          "<rect x='-105' y='-160' width='28' height='165' fill='url(#gl)' transform='skewX(-20)'/></g></g>")
    return o


def _dev_windows(s):
    T = 8
    o = s.extrude(-42, -14, 84, 8, 4, "url(#dface)", 8, **EXT)
    o += "<rect x='-10' y='-36' width='20' height='24' fill='#5c0b1b'/><rect x='-10' y='-36' width='6' height='24' fill='#7a1020'/>"
    o += s.extrude(-92, -152, 184, 120, 8, "url(#dface)", 12, **EXT)
    o += "<rect x='-84' y='-144' width='168' height='104' rx='4' fill='url(#dscr)'/>"
    o += f"<circle cx='0' cy='-70' r='22' fill='{RB}' opacity='.35'><animate attributeName='r' values='22;25;22' dur='5s' repeatCount='indefinite'/></circle>"
    wins = [(-26, -104, 92, 56, "#fff3ef", .0), (34, -88, 76, 44, "#ffd6d6", .14), (-52, -78, 56, 32, "#ffb3b9", .28)]
    for cx, cy, w, h, col, a in wins:
        kt, vals = _pop(.06 + a, T)
        o += (f"<g transform='translate({cx} {cy})'><g><animateTransform attributeName='transform' type='scale' values='{vals}' keyTimes='{kt}' dur='{T}s' repeatCount='indefinite'/>"
              f"<rect x='{-w / 2}' y='{-h / 2}' width='{w}' height='{h}' rx='4' fill='{col}' opacity='.95'/>"
              f"<rect x='{-w / 2}' y='{-h / 2}' width='{w}' height='9' rx='4' fill='#dc143c'/><rect x='{-w / 2}' y='{-h / 2 + 5}' width='{w}' height='4' fill='#dc143c'/>"
              f"<circle cx='{-w / 2 + 6}' cy='{-h / 2 + 4.5}' r='1.6' fill='#fff'/><circle cx='{-w / 2 + 12}' cy='{-h / 2 + 4.5}' r='1.6' fill='#fff' opacity='.7'/>"
              f"<rect x='{-w / 2 + 8}' y='{-h / 2 + 16}' width='{w * .5:.0f}' height='4' rx='2' fill='#8a0f24' opacity='.7'/>"
              f"<rect x='{-w / 2 + 8}' y='{-h / 2 + 24}' width='{w * .7:.0f}' height='3' rx='1.5' fill='#8a0f24' opacity='.4'/></g></g>")
    # progress bar inside first window
    o += (f"<rect x='-62' y='-92' width='72' height='5' rx='2.5' fill='#8a0f24' opacity='.25'/>"
          f"<rect x='-62' y='-92' width='0' height='5' rx='2.5' fill='#dc143c'><animate attributeName='width' values='0;0;72;72;0' keyTimes='0;.14;.6;.94;1' dur='{T}s' repeatCount='indefinite'/></rect>")
    # taskbar with lights running
    o += "<rect x='-84' y='-52' width='168' height='12' rx='0' fill='#12030a' opacity='.9'/>"
    for k in range(5):
        a = k * .16
        o += (f"<rect x='{-40 + k * 18}' y='-49' width='10' height='6' rx='2' fill='#ffd6d6' opacity='.35'>"
              f"<animate attributeName='opacity' values='.3;1;.3;.3' keyTimes='0;{.1 + a * .4:.2f};{.2 + a * .4:.2f};1' dur='{T / 2}s' repeatCount='indefinite'/></rect>")
    cid = s.uid("wc")
    o += (f"<clipPath id='{cid}'><rect x='-92' y='-152' width='184' height='120' rx='8'/></clipPath><g clip-path='url(#{cid})'>"
          "<g><animateTransform attributeName='transform' type='translate' values='-200 0;200 0;200 0' keyTimes='0;.35;1' dur='5.5s' begin='1.2s' repeatCount='indefinite'/>"
          "<rect x='-112' y='-172' width='28' height='160' fill='url(#gl)' transform='skewX(-20)'/></g></g>")
    return o


def _dev_mac(s):
    T = 6
    o = s.extrude(-102, -34, 204, 14, 6, "url(#dface)", 8, **EXT)
    o += "<rect x='-24' y='-34' width='48' height='5' rx='2.5' fill='#4a0b18'/>"
    o += s.extrude(-80, -140, 160, 106, 7, "url(#dface)", 12, **EXT)
    o += "<rect x='-73' y='-133' width='146' height='92' rx='3' fill='url(#dscr)'/>"
    o += f"<circle cx='34' cy='-96' r='18' fill='{RB}' opacity='.4'/>"
    o += "<rect x='-73' y='-133' width='146' height='8' fill='#12030a' opacity='.75'/><circle cx='-65' cy='-129' r='2' fill='#ffd6d6'/><rect x='-57' y='-131' width='24' height='4' rx='2' fill='#b0606c'/>"
    o += ("<rect x='-52' y='-116' width='104' height='46' rx='5' fill='#fff3ef' opacity='.92'/><rect x='-52' y='-116' width='104' height='8' rx='4' fill='#dc143c'/>"
          "<rect x='-44' y='-100' width='56' height='5' rx='2.5' fill='#8a0f24' opacity='.75'/><rect x='-44' y='-90' width='86' height='4' rx='2' fill='#8a0f24' opacity='.4'/><rect x='-44' y='-82' width='46' height='4' rx='2' fill='#8a0f24' opacity='.4'/>")
    # dock with bouncing icons
    o += "<rect x='-40' y='-58' width='80' height='14' rx='7' fill='#12030a' opacity='.8'/>"
    cols = ["#ff3b57", "#ffd6d6", "#f0c27b", "#ffb3b9", "#dc143c"]
    for k, c in enumerate(cols):
        x = -32 + k * 14.5
        a = k * .09
        o += (f"<rect x='{x}' y='-55' width='9' height='9' rx='2.6' fill='{c}'><animateTransform attributeName='transform' type='translate' "
              f"values='0 0;0 0;0 -7;0 0;0 0' keyTimes='0;{.05 + a:.2f};{.10 + a:.2f};{.16 + a:.2f};1' dur='{T}s' repeatCount='indefinite'/></rect>")
    # cursor travelling + click ripple
    o += (f"<circle cx='-26' cy='-51' r='0' fill='none' stroke='#fff' stroke-width='1.2'><animate attributeName='r' values='0;0;9;9' keyTimes='0;.62;.78;1' dur='{T}s' repeatCount='indefinite'/>"
          f"<animate attributeName='opacity' values='0;0;.9;0;0' keyTimes='0;.62;.66;.8;1' dur='{T}s' repeatCount='indefinite'/></circle>")
    o += (f"<g><animateMotion path='M-44 -108 L28 -96 L-26 -51 L-44 -108' dur='{T}s' repeatCount='indefinite'/>"
          "<path d='M0 0L0 12L3.4 9L5.6 14L7.6 13L5.4 8.2L9.6 8.2Z' fill='#fff' stroke='#1d0409' stroke-width='.8'/></g>")
    cid = s.uid("mc")
    o += (f"<clipPath id='{cid}'><rect x='-80' y='-140' width='160' height='106' rx='7'/></clipPath><g clip-path='url(#{cid})'>"
          "<g><animateTransform attributeName='transform' type='translate' values='-180 0;180 0;180 0' keyTimes='0;.35;1' dur='5.5s' begin='1.9s' repeatCount='indefinite'/>"
          "<rect x='-100' y='-160' width='28' height='142' fill='url(#gl)' transform='skewX(-20)'/></g></g>")
    return o


def _dev_android(s):
    T = 6.4
    o = s.extrude(-46, -152, 92, 148, 15, "url(#dface)", 12, **EXT)
    o += "<rect x='-40' y='-146' width='80' height='136' rx='11' fill='url(#dscr)'/>"
    o += f"<circle cx='0' cy='-72' r='20' fill='{RB}' opacity='.4'><animate attributeName='r' values='20;23;20' dur='4.5s' repeatCount='indefinite'/></circle>"
    o += "<circle cx='0' cy='-137' r='3.4' fill='#12030a'/>"
    o += s.text(0, -118, "09:41", "mono", 700, 13, P["w"])
    for k, (y, col) in enumerate([(-100, "#fff3ef"), (-68, "#ffd6d6"), (-36, "#ffb3b9")]):
        a = .06 + k * .13
        kt = f"0;{a:.3f};{a + .06:.3f};.86;.94;1"
        o += (f"<g opacity='0'><animateTransform attributeName='transform' type='translate' values='70 0;70 0;0 0;0 0;0 0;70 0' keyTimes='{kt}' dur='{T}s' repeatCount='indefinite'/>"
              f"<animate attributeName='opacity' values='0;0;1;1;0;0' keyTimes='{kt}' dur='{T}s' repeatCount='indefinite'/>"
              f"<rect x='-34' y='{y}' width='68' height='26' rx='7' fill='{col}' opacity='.93'/><circle cx='-24' cy='{y + 13}' r='5' fill='#dc143c'/>"
              f"<rect x='-14' y='{y + 7}' width='34' height='4' rx='2' fill='#8a0f24' opacity='.8'/><rect x='-14' y='{y + 15}' width='46' height='3.5' rx='1.7' fill='#8a0f24' opacity='.4'/></g>")
    o += (f"<circle cx='10' cy='-24' r='0' fill='none' stroke='#fff' stroke-width='1.4'><animate attributeName='r' values='0;0;14;14' keyTimes='0;.55;.75;1' dur='{T}s' repeatCount='indefinite'/>"
          f"<animate attributeName='opacity' values='0;0;.9;0;0' keyTimes='0;.55;.6;.75;1' dur='{T}s' repeatCount='indefinite'/></circle>")
    o += "<rect x='-15' y='-16' width='30' height='3' rx='1.5' fill='#ffd6d6' opacity='.8'/>"
    cid = s.uid("ac")
    o += (f"<clipPath id='{cid}'><rect x='-46' y='-152' width='92' height='148' rx='15'/></clipPath><g clip-path='url(#{cid})'>"
          "<g><animateTransform attributeName='transform' type='translate' values='-120 0;120 0;120 0' keyTimes='0;.35;1' dur='5.5s' begin='2.6s' repeatCount='indefinite'/>"
          "<rect x='-66' y='-172' width='28' height='188' fill='url(#gl)' transform='skewX(-20)'/></g></g>")
    return o


def platforms():
    H = 440
    s = Svg(W, H, "O GennisCode é multiplataforma: Linux, Windows, macOS e Android")
    s.shimmer("sh", 5.5, "#ffe0e3")
    _dev_defs(s)
    s.d(sun_defs("ps"))
    cid = s.clip_round()
    s.style(COMMON_CSS + ".title{animation:tt 2.4s cubic-bezier(.16,.84,.24,1) both}@keyframes tt{from{letter-spacing:34px;opacity:0}to{letter-spacing:6px;opacity:1}}")
    s.add(s.panel())
    s.add(f"<g clip-path='url(#{cid})'>{sun(600, 250, 100, True, .35, 'ps', 120, 3)}"
          f"<ellipse cx='600' cy='336' rx='560' ry='30' fill='none' stroke='{RB}' stroke-opacity='.3' stroke-dasharray='2 8' stroke-linecap='round'>"
          "<animate attributeName='stroke-dashoffset' values='0;-100' dur='8s' repeatCount='indefinite'/></ellipse>"
          f"{waves(W, 400, 16, 3, '#b3162f', '#3a0a15', '#ffd6d6', .28, 22, 'pw')}"
          f"{embers(16, 9, 100, 1100, 250, 400)}{petals(9, 12, 60, 1140, -10, 0, .85, dur=(9, 14), fall=H + 20)}</g>")
    s.add(f"<g class='fade' style='animation-delay:.2s'>{runs(s, 600, 40, [(JP, 'kanji', 700, R_), ('   ·   ONDE VOCÊ ESTIVER   ·   ', 'sans', 600, P['g2']), ('どこでも学べる', 'kanji', 700, P['g1'])], 12, track=5)}</g>")
    s.add(s.text(600, 92, "O GENNISCODE É MULTIPLATAFORMA", "display", 700, 40, "url(#sh)", track=6, cls="title"))
    s.add(s.text(600, 124, "Aprenda no PC, no notebook ou no celular. Sem barreira, sem custo.", "sans", 500, 15, P["g1"], cls="fade", style="animation-delay:1s"))
    devs = [(210, "LINUX", "リナックス", _dev_linux, "float"), (470, "WINDOWS", "ウィンドウズ", _dev_windows, "tilt"),
            (730, "MACOS", "マックオーエス", _dev_mac, "pulse"), (990, "ANDROID", "アンドロイド", _dev_android, "sway")]
    for i, (x, lab, kana, fn, motion) in enumerate(devs):
        d = i * .7
        inner = fn(s)
        if motion == "float":
            anim = f"<g><animateTransform attributeName='transform' type='translate' values='0 0;0 -10;0 0' keyTimes='0;.5;1' calcMode='spline' keySplines='.45 0 .55 1;.45 0 .55 1' dur='6s' begin='{d}s' repeatCount='indefinite'/>{inner}</g>"
        elif motion == "tilt":
            anim = (f"<g><animateTransform attributeName='transform' type='translate' values='0 0;0 -8;0 0' keyTimes='0;.5;1' calcMode='spline' keySplines='.45 0 .55 1;.45 0 .55 1' dur='5.2s' begin='{d}s' repeatCount='indefinite'/>"
                    f"<g><animateTransform attributeName='transform' type='rotate' values='-1.8 0 0;1.8 0 0;-1.8 0 0' keyTimes='0;.5;1' calcMode='spline' keySplines='.45 0 .55 1;.45 0 .55 1' dur='7s' repeatCount='indefinite'/>{inner}</g></g>")
        elif motion == "pulse":
            anim = (f"<g transform='translate(0 -76)'><g><animateTransform attributeName='transform' type='scale' values='1;1.045;1' keyTimes='0;.5;1' calcMode='spline' keySplines='.45 0 .55 1;.45 0 .55 1' dur='4.6s' begin='{d}s' repeatCount='indefinite'/>"
                    f"<g transform='translate(0 76)'>{inner}</g></g></g>")
        else:
            anim = (f"<g><animateTransform attributeName='transform' type='translate' values='-5 0;5 -9;-5 0' keyTimes='0;.5;1' calcMode='spline' keySplines='.45 0 .55 1;.45 0 .55 1' dur='6.4s' begin='{d}s' repeatCount='indefinite'/>{inner}</g>")
        s.add(f"<g transform='translate({x} 322)'>"
              f"<ellipse cx='0' cy='12' rx='78' ry='9' fill='#12030a' opacity='.85' filter='url(#blur)'><animate attributeName='rx' values='78;64;78' keyTimes='0;.5;1' dur='6s' begin='{d}s' repeatCount='indefinite'/></ellipse>"
              f"<ellipse cx='0' cy='12' rx='70' ry='6' fill='none' stroke='{RB}' stroke-opacity='.3'/>{anim}"
              + s.text(0, 44, lab, "display", 700, 13, P["w"], track=5) + s.jp(0, 63, kana, 11, RB, track=3) + "</g>")
    s.add(f"<rect x='578' y='386' width='44' height='2' fill='{RB}'><animate attributeName='width' values='0;44;44' keyTimes='0;.3;1' dur='4s' repeatCount='indefinite'/></rect>")
    s.add(s.border())
    s.add(s.grain())
    return s


# ------------------------------------------------------------------ extra banners
def pillars():
    cw, gap, ch = 384, 24, 214
    s = Svg(W, ch + 16, "Nossos pilares: aprender, construir, compartilhar", rx=14)
    s.shimmer("sh", 6, "#ffe0e3")
    s.style(COMMON_CSS)
    s.d(f"<linearGradient id='bg' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='{P['bg0']}'/><stop offset='.6' stop-color='{P['bg1']}'/><stop offset='1' stop-color='{P['bg2']}'/></linearGradient>")
    s.d(f"<linearGradient id='bd' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='{RB}' stop-opacity='.85'/><stop offset='1' stop-color='{RD}' stop-opacity='.1'/></linearGradient>")
    s.d(sun_defs("pl"))
    s.d(f"<pattern id='shippo2' width='36' height='36' patternUnits='userSpaceOnUse'><g fill='none' stroke='{RB}' stroke-opacity='.08'>"
        "<circle cx='0' cy='0' r='18'/><circle cx='36' cy='0' r='18'/><circle cx='0' cy='36' r='18'/><circle cx='36' cy='36' r='18'/><circle cx='18' cy='18' r='18'/></g></pattern>")
    for i, (ch_, title, jp, desc) in enumerate(CFG["pillars"]):
        x, y = i * (cw + gap), 8
        cid = s.uid("pc")
        s.d(f"<clipPath id='{cid}'><rect x='{x}' y='{y}' width='{cw}' height='{ch}' rx='14'/></clipPath>")
        lines = wrap("sans", 500, desc, 14, cw - 70, sep=" ")
        body = "".join(s.text(x + cw / 2, y + 162 + j * 20, ln, "sans", 500, 14, P["g1"]) for j, ln in enumerate(lines))
        inner = (f"<rect x='{x}' y='{y}' width='{cw}' height='{ch}' rx='14' fill='url(#bg)'/>"
                 f"<g clip-path='url(#{cid})'><rect x='{x}' y='{y}' width='{cw}' height='{ch}' fill='url(#shippo2)'/>"
                 f"{sun(x + cw / 2, y + 58, 30, True, .55, 'pl', 90 + i * 20, 3.6)}"
                 f""
                 f"</g>"
                 f"<rect x='{x + .5}' y='{y + .5}' width='{cw - 1}' height='{ch - 1}' rx='13.5' fill='none' stroke='url(#bd)' stroke-width='1.1'/>"
                 f"<circle cx='{x + cw / 2}' cy='{y + 58}' r='33' fill='#1d0409' fill-opacity='.7' stroke='{RB}' stroke-opacity='.8' stroke-width='1.2'/>"
                 f"<circle cx='{x + cw / 2}' cy='{y + 58}' r='41' fill='none' stroke='{RB}' stroke-dasharray='1 6' stroke-linecap='round' stroke-opacity='.8'>"
                 f"<animateTransform attributeName='transform' type='rotate' from='0 {x + cw / 2} {y + 58}' to='360 {x + cw / 2} {y + 58}' dur='{24 + i * 4}s' repeatCount='indefinite'/></circle>"
                 + s.jp(x + cw / 2, y + 71, ch_, 38, P["w"])
                 + s.text(x + cw / 2 + 3, y + 126, title, "display", 700, 18, P["w"], track=6)
                 + s.jp(x + cw / 2 + 2, y + 146, jp, 13, RB, track=4) + body
                 + f"<rect x='{x + cw / 2 - 18}' y='{y}' width='36' height='3' rx='1.5' fill='{RB}'/>")
        s.add(f"<g class='bob' style='animation-delay:{i * .6}s;animation-duration:{6.4 + i * .4}s'>{inner}</g>")
    return s


def journey():
    H = 262
    s = Svg(W, H, "Jornada do aluno: do zero ao certificado", rx=14)
    s.shimmer("sh", 6, "#ffe0e3")
    s.d(sun_defs("jn"))
    cid = s.clip_round()
    T = 10.0
    s.style(COMMON_CSS)
    s.add(s.panel())
    xs = [130 + i * 235 for i in range(5)]
    ly = 120
    s.add(f"<g clip-path='url(#{cid})'>{torii(1090, 262, 1.15, '#2a0509', RB, .5)}{torii(110, 262, 1.15, '#2a0509', RB, .5)}{petals(8, 31, 60, 1140, -10, 0, .8, dur=(9, 14), fall=H + 20)}</g>")
    s.add(runs(s, 600, 44, [(JP, "kanji", 700, R_), ("   ·   JORNADA DO ALUNO   ·   ", "sans", 600, P["g2"]), ("道", "kanji", 700, P["g1"])], 12, track=5))
    s.add(s.text(600 + 2, 78, "Do zero ao certificado", "display", 700, 24, "url(#sh)", track=2))
    s.add(f"<rect x='{xs[0]}' y='{ly - 1}' width='{xs[-1] - xs[0]}' height='2' fill='{RB}' opacity='.25'/>")
    s.add(f"<rect x='{xs[0]}' y='{ly - 1.5}' width='0' height='3' rx='1.5' fill='{RB}'><animate attributeName='width' values='0;{xs[-1] - xs[0]};{xs[-1] - xs[0]}' keyTimes='0;.8;1' dur='{T}s' repeatCount='indefinite'/></rect>")
    s.add(f"<g opacity='0'><animateTransform attributeName='transform' type='translate' values='{xs[0]} {ly};{xs[-1]} {ly};{xs[-1]} {ly}' keyTimes='0;.8;1' dur='{T}s' repeatCount='indefinite'/>"
          f"<animate attributeName='opacity' values='1;1;0;0' keyTimes='0;.8;.86;1' dur='{T}s' repeatCount='indefinite'/>{sakura_flower(0, 0, 11, P['pk'], '#ff3b57', 6)}</g>")
    for i, (kj, title, jp, desc) in enumerate(CFG["journey"]):
        x = xs[i]
        a = i / 4 * .8
        s.add(f"<circle cx='{x}' cy='{ly}' r='34' fill='none' stroke='{RB}' stroke-width='1.4' opacity='.25'><animate attributeName='opacity' values='.2;.2;1;1;.2' keyTimes='0;{a:.3f};{a + .02:.3f};.93;1' dur='{T}s' repeatCount='indefinite'/>"
              f"<animate attributeName='r' values='34;34;42;34;34' keyTimes='0;{a:.3f};{a + .05:.3f};{a + .12:.3f};1' dur='{T}s' repeatCount='indefinite'/></circle>")
        s.add(f"<circle cx='{x}' cy='{ly}' r='30' fill='{P['bg0']}' stroke='{RB}' stroke-width='1.6'/>"
              f"<circle cx='{x}' cy='{ly}' r='30' fill='{RB}' fill-opacity='0'><animate attributeName='fill-opacity' values='0;0;.35;.18;0' keyTimes='0;{a:.3f};{a + .02:.3f};.93;1' dur='{T}s' repeatCount='indefinite'/></circle>"
              + s.jp(x, ly + 11, kj, 31, P["w"]))
        s.add(s.text(x + 2, ly + 62, title, "display", 700, 14, P["w"], track=3.5))
        s.add(s.jp(x + 2, ly + 82, jp, 12.5, RB, track=3))
        s.add(s.text(x, ly + 104, desc, "sans", 500, 12.5, P["g3"]))
    s.add(s.border())
    s.add(s.grain())
    return s


def open_repos():
    H = 150
    s = Svg(W, H, "Repositórios abertos para consulta e avaliação", rx=14)
    s.shimmer("sh", 6, "#ffe0e3")
    s.d(sun_defs("op"))
    cid = s.clip_round()
    s.style(COMMON_CSS + ".blink{animation:bl 1s steps(1) infinite}@keyframes bl{0%,100%{opacity:1}50%{opacity:0}}")
    s.add(s.panel())
    s.add(f"<g clip-path='url(#{cid})'>{sun(120, 75, 44, True, .6, 'op', 80, 3.2)}{embers(12, 71, 40, 1160, 60, 150)}{petals(5, 2, 300, 1100, -10, 0, .7, dur=(8, 12), fall=170)}</g>")
    s.add(f"<circle cx='120' cy='75' r='44' fill='{P['bg0']}' fill-opacity='.35'/>" + s.jp(120, 92, "開", 52, P["w"]))
    s.add(f"<circle cx='120' cy='75' r='56' fill='none' stroke='{RB}' stroke-dasharray='1 6' stroke-linecap='round'><animateTransform attributeName='transform' type='rotate' from='0 120 75' to='360 120 75' dur='28s' repeatCount='indefinite'/></circle>")
    s.add(runs(s, 560, 52, [(JP, "kanji", 700, R_), ("   ·   100% PÚBLICO   ·   ", "sans", 600, P["g2"]), ("公開", "kanji", 700, P["g1"])], 11.5, track=4))
    s.add(s.text(560 + 2, 92, "REPOSITÓRIOS ABERTOS", "display", 700, 34, "url(#sh)", track=5))
    s.add(s.text(560, 120, "Para consulta, estudo e avaliação. Educador, recrutador, estudante ou curioso: explore à vontade.", "sans", 500, 14, P["g1"]))
    px, py, pw_, ph = 934, 38, 232, 74
    s.add(f"<rect x='{px}' y='{py}' width='{pw_}' height='{ph}' rx='10' fill='#12030a' fill-opacity='.85' stroke='{RB}' stroke-opacity='.7'/>"
          f"<circle cx='{px + 14}' cy='{py + 12}' r='3' fill='#ff3b57'/><circle cx='{px + 25}' cy='{py + 12}' r='3' fill='#f0c27b'/><circle cx='{px + 36}' cy='{py + 12}' r='3' fill='#ffd6d6'/>")
    T = 6
    s.add(_typed(s, px + 14, py + 40, "$ git clone --open", P["w"], .5, 2.2, T, 12.5))
    s.add(_typed(s, px + 14, py + 62, "✓ acesso livre", RB, 2.8, 3.8, T, 12.5))
    s.add(s.border())
    s.add(s.grain())
    return s


def proverbs():
    items = CFG["proverbs"]
    H = 92
    s = Svg(W, H, "Provérbios japoneses", rx=12)
    edge_mask(s, "m", H)
    x, parts = 0, []
    gap = 56
    for jp, pt in items:
        wj = s.w_("kanji", 700, jp, 22, 4)
        wp = s.w_("mono", 400, pt, 11, 0)
        wd = max(wj, wp)
        parts.append(s.jp(x + wd / 2, 40, jp, 22, P["w"], track=4))
        parts.append(s.text(x + wd / 2, 66, pt, "mono", 400, 11, P["g3"]))
        x += wd + gap / 2
        parts.append(sakura_flower(x, 34, 7.5, P["pk"], "#ff3b57"))
        x += gap / 2
    loop = x
    s.add(s.frame(brackets=False))
    one = "".join(parts)
    s.add(f"<g mask='url(#m)'><g><animateTransform attributeName='transform' type='translate' from='0 0' to='-{loop:.1f} 0' dur='{loop / 38:.1f}s' repeatCount='indefinite'/>"
          f"<g>{one}</g><g transform='translate({loop:.1f} 0)'>{one}</g><g transform='translate({2 * loop:.1f} 0)'>{one}</g></g></g>")
    return s



# ------------------------------------------------------------------ recrutadores / estudantes
def recruit():
    R = CFG["recruit"]
    H = 318
    s = Svg(W, H, R["eyebrow"] + ": " + R["text"], rx=14)
    s.shimmer("sh", 6, "#ffe0e3")
    s.d(sun_defs("rc") + lantern_defs())
    s.d("<linearGradient id='rg' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='#ff3b57'/><stop offset='.6' stop-color='#dc143c'/><stop offset='1' stop-color='#a50f2a'/></linearGradient>")
    s.d("<linearGradient id='sweep' x1='0' x2='1'><stop offset='0' stop-color='#fff' stop-opacity='0'/><stop offset='.5' stop-color='#fff' stop-opacity='.14'/><stop offset='1' stop-color='#fff' stop-opacity='0'/></linearGradient>")
    cid = s.clip_round()
    s.style(COMMON_CSS + ".chip{opacity:0;animation:fi .9s ease forwards}.blink{animation:bl 1s steps(1) infinite}@keyframes bl{0%,100%{opacity:1}50%{opacity:0}}")
    s.add(s.panel(colors=HOT))
    s.add(f"<g clip-path='url(#{cid})'>{sun(110, 160, 66, True, .8, 'rc', 100, 3.2)}"
          f"{fuji(1080, 324, 1.2, '#8a1730')}{torii(1000, 324, .8, '#3a0612', '#ffd6d6', .9)}"
          f"{waves(W, 296, 18, 3, '#e02a4a', '#7a1229', '#ffe3e6', .3, 20, 'rw')}{embers(22, 41, 60, 1140, 190, 318)}"
          f"{petals(12, 19, 100, 1100, -10, 0, .9, dur=(8, 13), fall=H + 20)}"
          f"<rect x='-300' y='-20' width='240' height='{H + 40}' fill='url(#sweep)' transform='skewX(-20)'><animateTransform attributeName='transform' type='translate' values='0 0;1700 0;1700 0' keyTimes='0;.45;1' dur='7s' repeatCount='indefinite' additive='sum'/></rect></g>")
    # emblem
    s.add(f"<circle cx='110' cy='160' r='54' fill='#3a0612' fill-opacity='.55' stroke='#ffd6d6' stroke-opacity='.8' stroke-width='1.4'/>"
          f"<circle cx='110' cy='160' r='64' fill='none' stroke='#ffd6d6' stroke-dasharray='1 6' stroke-linecap='round'><animateTransform attributeName='transform' type='rotate' from='0 110 160' to='360 110 160' dur='26s' repeatCount='indefinite'/></circle>"
          + s.jp(110, 178, "公", 56, P["w"]) + icon("branch", 110, 213, 18, P["w"], 1.7))
    cx = 665
    s.add(f"<g class='fade' style='animation-delay:.2s'>{runs(s, cx, 54, [(JP, 'kanji', 700, '#fff'), ('   ·   ' + R['eyebrow'] + '   ·   ', 'sans', 600, P['g1']), (R['jp'], 'kanji', 700, P['w'])], 12, track=4)}</g>")
    s.add(s.text(cx + 2, 100, R["title"], "display", 700, 40, "url(#sh)", track=4))
    lines = wrap("sans", 500, R["text"], 16.5, 760, sep=" ")
    for j, ln in enumerate(lines):
        s.add(s.text(cx, 142 + j * 26, ln, "sans", 500, 16.5, P["w"], cls="fade", style=f"animation-delay:{.6 + j * .25}s"))
    chips, gapc = [], 14
    for ic, lab, jp in R["chips"]:
        tw_ = s.w_("mono", 700, lab, 11.5, 2) + s.w_("kanji", 700, jp, 12, 2)
        chips.append((ic, lab, jp, 14 + 18 + 10 + tw_ + 34))
    tot = sum(c[3] for c in chips) + gapc * (len(chips) - 1)
    x = cx - tot / 2
    y0 = 142 + len(lines) * 26 + 14
    for i, (ic, lab, jp, cw) in enumerate(chips):
        s.add(f"<g class='chip' style='animation-delay:{1.3 + i * .15}s'><g class='bob' style='animation-delay:{i * .4}s'>"
              f"<rect x='{x:.1f}' y='{y0}' width='{cw:.1f}' height='38' rx='19' fill='#3a0612' fill-opacity='.6' stroke='#ffd6d6' stroke-opacity='.7'/>"
              f"{icon(ic, x + 14 + 9, y0 + 19, 17, '#fff', 1.6)}"
              + s.text(f"{x + 14 + 18 + 10:.1f}", y0 + 23.5, lab, "mono", 700, 11.5, P["w"], anchor="start", track=2)
              + s.jp(x + cw - 20, y0 + 23.5, jp, 12, P["g1"], anchor="end") + "</g></g>")
        x += cw + gapc
    s.add(s.seal(1150, 40, 24) + s.seal(50, 40, 22, "紅", 3))
    s.add(lantern(1130, 60, 40, .6, "玄", s.used, 3)) if False else None
    s.add(s.border())
    s.add(s.grain())
    return s


# ------------------------------------------------------------------ more dividers (variety)
def divider_torii():
    s = Svg(W, 70, "")
    comet_defs(s)
    edge_mask(s, "m", 70)
    s.d(f"<linearGradient id='hl' x1='0' x2='1'><stop offset='0' stop-color='{RB}' stop-opacity='0'/><stop offset='.5' stop-color='{RB}'/><stop offset='1' stop-color='{RB}' stop-opacity='0'/></linearGradient>")
    s.d("<radialGradient id='tg'><stop offset='0' stop-color='#ff3b57' stop-opacity='.55'/><stop offset='1' stop-color='#ff3b57' stop-opacity='0'/></radialGradient>")
    s.add(f"<g mask='url(#m)'><rect x='0' y='56' width='{W}' height='1.5' fill='url(#hl)'/>{comet(-180, 1380, 56, 5.5)}{comet(-180, 1380, 56.2, 8, 2, 120, 1.2, True, op=.6)}</g>")
    s.add(f"<ellipse cx='600' cy='40' rx='70' ry='34' fill='url(#tg)'><animate attributeName='opacity' values='.4;1;.4' dur='3.4s' repeatCount='indefinite'/></ellipse>")
    s.add(torii(600, 58, .52, "#7a1229", "#ffb3b9", 1))
    for sx in (-1, 1):
        for k in range(3):
            s.add(f"<rect x='{600 + sx * (96 + k * 26) - 3}' y='{50 - k * 2}' width='6' height='6' fill='{RB}' opacity='{.9 - k * .25}' transform='rotate(45 {600 + sx * (96 + k * 26)} {53 - k * 2})'><animate attributeName='opacity' values='.2;1;.2' dur='2.4s' begin='{k * .3}s' repeatCount='indefinite'/></rect>")
    s.add(petals(4, 6, 200, 1000, 2, 0, .6, dur=(7, 10), fall=60))
    return s


def divider_katana():
    s = Svg(W, 60, "")
    edge_mask(s, "m", 60)
    s.d(f"<linearGradient id='bl' x1='0' x2='1'><stop offset='0' stop-color='#ffe3e6' stop-opacity='0'/><stop offset='.12' stop-color='#ffd6d6'/><stop offset='1' stop-color='#fff'/></linearGradient>")
    s.d("<linearGradient id='ln2' x1='0' x2='1'><stop offset='0' stop-color='#ff3b57' stop-opacity='0'/><stop offset='.5' stop-color='#ff3b57'/><stop offset='1' stop-color='#ff3b57' stop-opacity='0'/></linearGradient>")
    s.add(f"<g mask='url(#m)'><rect x='0' y='29.2' width='{W}' height='1.6' fill='url(#ln2)'/></g>")
    # two katanas crossing a hanko-like centre
    for rot in (-18, 18):
        s.add(f"<g transform='rotate({rot} 600 30)'><path d='M470 30 L722 27.5 Q735 30 722 32 Z' fill='url(#bl)'/><path d='M470 30 L722 30.2' stroke='#ff8fa3' stroke-width='.6'/>"
              f"<rect x='724' y='24' width='5' height='12' rx='2' fill='{P['au']}'/><rect x='730' y='26.5' width='50' height='7' rx='3' fill='#7a1229'/>"
              + "".join(f"<path d='M{736 + k * 9} 26.5l5 7' stroke='#ffd6d6' stroke-opacity='.6'/>" for k in range(5)) + "</g>")
    s.add(f"<g mask='url(#m)'><rect x='-200' y='20' width='90' height='20' fill='#fff' fill-opacity='.0'/>"
          f"<rect x='0' y='28' width='120' height='4' rx='2' fill='#fff' fill-opacity='.8' filter='url(#gb)'><animateTransform attributeName='transform' type='translate' values='-150 0;1300 0' dur='4.2s' repeatCount='indefinite'/></rect></g>")
    s.d("<filter id='gb'><feGaussianBlur stdDeviation='2'/></filter>")
    s.add(s.seal(600, 30, 24))
    return s


def divider_lanterns():
    s = Svg(W, 92, "")
    edge_mask(s, "m", 92)
    s.d(lantern_defs())
    s.add(f"<g mask='url(#m)'><path d='M0 6Q600 18 1200 6' fill='none' stroke='{P['g5']}' stroke-width='1.2'/>")
    n = 13
    for i in range(n):
        x = 60 + i * (W - 120) / (n - 1)
        y = 6 + 12 * math.sin(math.pi * x / W) - 0
        h = 30 if i % 2 else 36
        s.add(lantern(round(x), round(y + 1), h, i * .45, ["玄", "祭", "紅"][i % 3], s.used, 4))
    s.add("</g>")
    return s


def divider_sunrise():
    s = Svg(W, 70, "")
    edge_mask(s, "m", 70)
    s.d(sun_defs("ds"))
    s.add(f"<clipPath id='dc'><rect x='0' y='0' width='{W}' height='54'/></clipPath>")
    s.add(f"<g mask='url(#m)'><g clip-path='url(#dc)'>{sun(600, 56, 34, True, .9, 'ds', 60, 6)}</g>"
          f"<rect x='0' y='54' width='{W}' height='1.5' fill='{RB}' opacity='.8'/>{waves(W, 55, 7, 3, '#e02a4a', '#5a0b1b', '#ffe3e6', .3, 10, 'dw')}</g>")
    s.add(petals(5, 8, 150, 1050, -4, 0, .6, dur=(7, 11), fall=62))
    return s


# ------------------------------------------------------------------ build all
def main():
    os.makedirs(OUT, exist_ok=True)
    jobs = {"banner": banner(), "divider": divider(), "divider-wave": divider_wave(), "stack-marquee": marquee(),
            "stack-cards": stack_cards(), "fact-cards": fact_cards(), "quote": quote(), "cta": cta(*CFG["cta"]),
            "cta-instagram": cta(*CFG["cta_insta"], "camera"), "cta-repo-quiz": cta("REPOSITÓRIO", "Quiz-Projeto", "branch", 600), "cta-repo-gennis": cta("REPOSITÓRIO", "GennisCode", "branch", 600), "team-line": team_line(),
            "fluxer-banner": fluxer(), "footer": footer(), "platforms-banner": platforms(),
            "banner-pilares": pillars(), "banner-jornada": journey(), "banner-recrutadores": recruit(), "stack-distros": stack_cards(CFG["distro_layers"], "Sistemas e distros"), "distros-marquee": marquee(CFG["distros"], "Distros e sistemas"), "sub-sistemas": subheader("SISTEMAS & DISTROS", "terminal", "Sistemas e distros"), "divider-torii": divider_torii(), "divider-katana": divider_katana(), "divider-lanterns": divider_lanterns(), "divider-sunrise": divider_sunrise(), "banner-proverbios": proverbs(),
            "typing-main": typing(CFG["typing_main"], "Apresentação"), "typing-team": typing(CFG["typing_team"], "GennisTeam"),
            "sub-projeto": subheader("SOBRE O PROJETO", "cube", "Sobre o projeto"),
            "sub-familia": subheader("VENHA FAZER PARTE DA NOSSA FAMÍLIA", "heart", "Venha fazer parte da nossa família")}
    for fid, nm, hd, ph, rl in CFG["team"]:
        jobs[f"member-{fid}"] = member(nm, hd, ph, rl)
    for name, (num, title, ic, jp, mark) in CFG["headers"].items():
        jobs[name] = header(num, title, ic, jp, mark)
    for name, svg in jobs.items():
        open(os.path.join(OUT, f"{name}.svg"), "w", encoding="utf-8").write(svg.render())
    print(f"{len(jobs)} assets -> {OUT}")


if __name__ == "__main__":
    main()
