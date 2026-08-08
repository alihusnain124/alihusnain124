#!/usr/bin/env python3
"""
Generates the animated SVG panels used by README.md.

Everything here is plain SVG + CSS keyframes, which GitHub renders (and animates)
when the file is referenced with <img src="assets/....svg">. Tweak the palette or
copy below and re-run:  python3 assets/generate.py
"""

import os
import sys
import math
import xml.etree.ElementTree as ET

OUT = os.path.dirname(os.path.abspath(__file__))

STATIC = "--static" in sys.argv

# ─────────────────────────────── design tokens ───────────────────────────────
# Matches alihusnaintech.vercel.app's palette: near-black surfaces, mint accent.

BG        = "#080808"
CARD      = "#0F0F0F"
CARD_ALT  = "#161616"
LINE      = "#1F1F1F"
INK       = "#F0F0F0"
INK_DIM   = "#888888"
INK_FAINT = "#5A5A5A"

A1 = "#6EE7B7"          # mint (the portfolio's --accent)
A2 = "#34D399"          # emerald
A3 = "#2DD4BF"          # teal
A4 = "#22D3EE"          # cyan

FONT = "'Segoe UI',Roboto,-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif"
MONO = "'SFMono-Regular',ui-monospace,Consolas,'Liberation Mono',Menlo,monospace"

STATIC_CSS = "" if not STATIC else """
  .rise,.slide,.in,.bar,.caret,.blob,.blob2,.halo,.ping,.bob,.draw,.typeline,.ring {
    animation:none !important; opacity:1 !important; transform:none !important;
    stroke-dashoffset:0 !important; clip-path:none !important;
  }"""


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def write(name, body):
    body = body.strip() + "\n"
    try:
        ET.fromstring(body)
    except ET.ParseError as e:
        raise SystemExit(f"✗ {name} is not valid XML: {e}")
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"  ✓ {name}  ({os.path.getsize(path) / 1024:.1f} KB)")


def svg(w, h, body, extra_defs="", rounded=0):
    if rounded:
        extra_defs = (f'<clipPath id="shell"><rect width="{w}" height="{h}" rx="{rounded}"/>'
                      f'</clipPath>') + extra_defs
        body = (f'<g clip-path="url(#shell)">{body}</g>'
                f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="{rounded}" '
                f'fill="none" stroke="{LINE}" stroke-width="1.5"/>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" fill="none" role="img">
<defs>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{A1}"/><stop offset=".45" stop-color="{A2}"/>
    <stop offset=".8" stop-color="{A3}"/><stop offset="1" stop-color="{A4}"/>
  </linearGradient>
  <linearGradient id="accentV" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{A1}"/><stop offset="1" stop-color="{A4}"/>
  </linearGradient>
  <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{A1}"/><stop offset="1" stop-color="{A1}" stop-opacity="0"/>
  </linearGradient>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="1.4" cy="1.4" r="1.4" fill="#FFFFFF" fill-opacity=".05"/>
  </pattern>
  <filter id="blur" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="58"/>
  </filter>
  <filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
    <feDropShadow dx="0" dy="5" stdDeviation="9" flood-color="#000" flood-opacity=".42"/>
  </filter>
{extra_defs}
</defs>
<style>
  text {{ font-family:{FONT}; }}
  .mono {{ font-family:{MONO}; }}
  @keyframes rise    {{ from {{ opacity:0; transform:translateY(16px); }} to {{ opacity:1; transform:translateY(0); }} }}
  @keyframes slideL  {{ from {{ opacity:0; transform:translateX(-22px); }} to {{ opacity:1; transform:translateX(0); }} }}
  @keyframes slideR  {{ from {{ opacity:0; transform:translateX(22px); }} to {{ opacity:1; transform:translateX(0); }} }}
  @keyframes fade    {{ from {{ opacity:0; }} to {{ opacity:1; }} }}
  @keyframes grow    {{ from {{ transform:scaleX(0); }} to {{ transform:scaleX(1); }} }}
  @keyframes blink   {{ 0%,45% {{ opacity:1; }} 55%,100% {{ opacity:0; }} }}
  @keyframes drift   {{ 0%,100% {{ transform:translate(0,0) scale(1); }} 50% {{ transform:translate(46px,-30px) scale(1.16); }} }}
  @keyframes drift2  {{ 0%,100% {{ transform:translate(0,0) scale(1.1); }} 50% {{ transform:translate(-52px,26px) scale(.9); }} }}
  @keyframes halo    {{ 0%,100% {{ opacity:.34; }} 50% {{ opacity:.8; }} }}
  @keyframes ping    {{ 0% {{ transform:scale(.7); opacity:.85; }} 100% {{ transform:scale(2.6); opacity:0; }} }}
  @keyframes bob     {{ 0%,100% {{ transform:translateY(0); }} 50% {{ transform:translateY(7px); }} }}
  @keyframes typeline{{ from {{ clip-path:inset(0 100% 0 0); }} to {{ clip-path:inset(0 0 0 0); }} }}
  @keyframes ringgrow{{ from {{ stroke-dashoffset:var(--circ); }} to {{ stroke-dashoffset:var(--off); }} }}
  .rise  {{ animation:rise .85s cubic-bezier(.22,1,.36,1) both; }}
  .slide {{ animation:slideL .85s cubic-bezier(.22,1,.36,1) both; }}
  .slideR{{ animation:slideR .85s cubic-bezier(.22,1,.36,1) both; }}
  .in    {{ animation:fade 1s ease both; }}
  .bar   {{ transform-box:fill-box; transform-origin:left center;
            animation:grow 1.15s cubic-bezier(.22,1,.36,1) both; }}
  .caret {{ animation:blink 1.1s steps(1) infinite; }}
  .blob  {{ transform-box:fill-box; transform-origin:center;
            animation:drift 17s ease-in-out infinite; }}
  .blob2 {{ transform-box:fill-box; transform-origin:center;
            animation:drift2 21s ease-in-out infinite; }}
  .halo  {{ animation:halo 4.5s ease-in-out infinite; }}
  .ping  {{ transform-box:fill-box; transform-origin:center;
            animation:ping 2.6s ease-out infinite; }}
  .bob   {{ animation:bob 2.1s ease-in-out infinite; }}
  .typeline {{ animation:typeline .7s steps(28) both; }}
  .ring  {{ animation:ringgrow 1.3s cubic-bezier(.22,1,.36,1) both; }}
  @media (prefers-reduced-motion:reduce) {{
    .rise,.slide,.slideR,.in,.bar,.caret,.blob,.blob2,.halo,.ping,.bob,.typeline,.ring {{
      animation:none !important; opacity:1 !important; transform:none !important;
      stroke-dashoffset:0 !important; clip-path:none !important;
    }}
  }}
{STATIC_CSS}
</style>
{body}
</svg>"""


def panel(x, y, w, h, r=16, fill=CARD, stroke=LINE, sw=1):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>')


def backdrop(w, h, blobs=True):
    out = [f'<rect width="{w}" height="{h}" fill="{BG}"/>',
           f'<rect width="{w}" height="{h}" fill="url(#dots)"/>']
    if blobs:
        out += [
            f'<g filter="url(#blur)" opacity=".26">',
            f'<circle class="blob" cx="{int(w*0.1)}" cy="{int(h*0.15)}" r="{int(h*0.4)}" fill="{A1}"/>',
            f'<circle class="blob2" cx="{int(w*0.86)}" cy="{int(h*0.82)}" r="{int(h*0.36)}" fill="{A4}"/>',
            f'</g>',
        ]
    return "".join(out)


def chip(x, y, label, w=None, pad=15, fs=12, fill="#FFFFFF", op=".07",
         stroke=None, color=INK_DIM, h=27, weight="600"):
    w = w if w else int(len(label) * fs * 0.60) + pad * 2
    s = f'stroke="{stroke}" stroke-width="1"' if stroke else ""
    return (f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h//2}" fill="{fill}" '
            f'fill-opacity="{op}" {s}/>'
            f'<text x="{x + w/2}" y="{y + h/2 + fs*0.36}" font-size="{fs}" font-weight="{weight}" '
            f'fill="{color}" text-anchor="middle">{esc(label)}</text></g>'), w


def ring(cx, cy, r, pct, color, delay=0, sw=9):
    circ = 2 * math.pi * r
    off = circ * (1 - pct / 100)
    b = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#FFFFFF" '
         f'stroke-opacity=".07" stroke-width="{sw}"/>']
    b.append(f'<circle class="ring" style="--circ:{circ:.1f};--off:{off:.1f};animation-delay:{delay:.2f}s" '
              f'cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{sw}" '
              f'stroke-linecap="round" stroke-dasharray="{circ:.1f}" stroke-dashoffset="{circ:.1f}" '
              f'transform="rotate(-90 {cx} {cy})"/>')
    return "".join(b)


# ──────────────────── 1. hero — name-forward + stat dashboard ───────────────

def hero():
    W, H = 1200, 356
    b = [backdrop(W, H)]
    b.append(f'<rect width="{W}" height="3" fill="url(#accent)"/>')

    # ── left: identity block ──
    b.append('<g class="rise" style="animation-delay:.05s">')
    b.append(f'<rect x="72" y="70" width="9" height="9" rx="4.5" fill="{A1}" class="halo"/>')
    b.append(f'<text x="94" y="79" font-size="13" font-weight="700" letter-spacing="2.6" '
             f'fill="{INK_DIM}">FULL-STACK SOFTWARE ENGINEER</text>')
    b.append('</g>')

    b.append('<g class="rise" style="animation-delay:.18s">')
    b.append(f'<text x="70" y="180" font-size="84" font-weight="800" letter-spacing="-2.6" '
             f'fill="{INK}">Ali <tspan fill="url(#accent)">Husnain</tspan></text>')
    b.append('</g>')

    b.append('<g class="rise" style="animation-delay:.32s">')
    b.append(f'<text x="72" y="226" class="mono" font-size="18" fill="{INK_DIM}">'
             f'<tspan fill="{A1}">&gt;</tspan> building full-stack web apps &amp; AI/RAG-powered products'
             f'<tspan class="caret" fill="{A4}">_</tspan></text>')
    b.append('</g>')

    b.append('<g class="rise" style="animation-delay:.44s">')
    for i, ln in enumerate([
        "3+ years shipping production code — from PHP/Laravel foundations",
        "to Node.js, NestJS &amp; LLM-driven applications.",
    ]):
        b.append(f'<text x="72" y="{264+i*24}" font-size="15.5" fill="{INK_FAINT}">{ln}</text>')
    b.append('</g>')

    # (CTA buttons live as separate clickable images below the hero — see
    #  cta-journey.svg / cta-contact.svg — since a single <a> already wraps
    #  this whole banner in the README, buttons drawn *inside* it can't carry
    #  their own separate links.)

    # ── right: tilted 2×2 stat dashboard, distinct from a plain strip ──
    stats = [("3+", "YEARS", A1), ("15+", "SHIPPED", A2), ("10+", "INTEGRATIONS", A3), ("3", "COMPANIES", A4)]
    gx, gy, gw, gh, gap = 858, 90, 150, 108, 18
    rot = -5
    b.append(f'<g filter="url(#blur)" opacity=".35">'
             f'<circle class="blob" cx="{gx+gw+gap/2}" cy="{gy+gh+gap/2}" r="190" fill="{A1}"/></g>')
    b.append(f'<g transform="rotate({rot} {gx+gw+gap/2} {gy+gh+gap/2})">')
    for i, (big, small, col) in enumerate(stats):
        cx_ = gx + (i % 2) * (gw + gap)
        cy_ = gy + (i // 2) * (gh + gap)
        d = 0.5 + i * 0.1
        b.append(f'<g class="rise" style="animation-delay:{d:.2f}s" filter="url(#soft)">')
        b.append(panel(cx_, cy_, gw, gh, r=16))
        b.append(f'<circle cx="{cx_+28}" cy="{cy_+30}" r="4" fill="{col}" class="halo"/>')
        b.append(f'<text x="{cx_+22}" y="{cy_+72}" font-size="30" font-weight="800" fill="{col}">{big}</text>')
        b.append(f'<text x="{cx_+22}" y="{cy_+92}" font-size="10" font-weight="700" letter-spacing="1.4" '
                 f'fill="{INK_FAINT}">{small}</text>')
        b.append('</g>')
    b.append('</g>')

    return svg(W, H, "".join(b), rounded=20)


# ────────────────────────── 2. section headings ─────────────────────────────

HEADER_H = 104


def header_frag(kicker, title, color):
    b = ['<g class="slide">']
    b.append(f'<rect x="70" y="30" width="3" height="52" rx="1.5" fill="url(#accentV)"/>')
    b.append(f'<text x="90" y="49" font-size="11.5" font-weight="700" letter-spacing="2.4" '
             f'fill="{INK_FAINT}">{esc(kicker)}</text>')
    b.append(f'<text x="89" y="80" font-size="34" font-weight="800" letter-spacing="-.8" '
             f'fill="{INK}">{esc(title)}</text>')
    b.append('</g>')
    w = int(len(title) * 19) + 40
    b.append(f'<rect x="{89 + w}" y="67" width="{max(60, 1040 - w)}" height="1" fill="url(#fade)" '
             f'class="bar" style="animation-delay:.5s"/>')
    b.append(f'<circle cx="1116" cy="56" r="4" fill="{color}" class="halo"/>')
    b.append(f'<circle cx="1116" cy="56" r="4" fill="{color}" class="ping"/>')
    return "".join(b)


def with_header(w, h, body, kicker, title, color, blobs=True):
    H = h + HEADER_H
    out = [backdrop(w, H, blobs=blobs),
           header_frag(kicker, title, color),
           f'<g transform="translate(0,{HEADER_H})">{body}</g>']
    return svg(w, H, "".join(out), rounded=20)


def section(name, kicker, title, color):
    W = 1200
    b = [backdrop(W, HEADER_H, blobs=False), header_frag(kicker, title, color)]
    write(f"sec-{name}.svg", svg(W, HEADER_H, "".join(b), rounded=20))


# ─────────────────────── 3. about — bento grid ───────────────────────────────

def about():
    W, H = 1200, 546
    b = [f'<g filter="url(#blur)" opacity=".26">'
         f'<circle class="blob2" cx="1080" cy="120" r="190" fill="{A3}"/></g>']

    # ── left: code window ──
    b.append('<g class="rise" style="animation-delay:.1s" filter="url(#soft)">')
    b.append(panel(70, 34, 610, 350, r=14, fill=CARD_ALT))
    b.append(f'<path d="M70 48a14 14 0 0 1 14-14h582a14 14 0 0 1 14 14v30H70z" fill="#1A1A1A"/>')
    b.append(f'<line x1="70" y1="78" x2="680" y2="78" stroke="{LINE}"/>')
    for i, c in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
        b.append(f'<circle cx="{92 + i*19}" cy="56" r="5.5" fill="{c}"/>')
    b.append(f'<text x="375" y="61" class="mono" font-size="12" fill="{INK_FAINT}" '
             f'text-anchor="middle">ali.ts</text>')
    b.append('</g>')

    K, S, V, P, C = "#7EE787", "#A5D6FF", "#79C0FF", "#D2A8FF", "#8B949E"
    code = [
        [("const", K), (" ali", V), (": ", C), ("Engineer", P), (" = {", C)],
        [("  role", V), (":       ", C), ('"Full-Stack Software Engineer"', S), (",", C)],
        [("  based", V), (":      ", C), ('"Lahore, Pakistan · remote-friendly"', S), (",", C)],
        [("  experience", V), (": ", C), ('"3+ years, 3 companies"', S), (",", C)],
        [("", C)],
        [("  builds", V), (": {", C)],
        [("    frontend", V), (": [", C), ('"React"', S), (", ", C), ('"Next.js"', S), (", ", C), ('"TypeScript"', S), ("],", C)],
        [("    backend", V), (":  [", C), ('"NestJS"', S), (", ", C), ('"Express"', S), (", ", C), ('"Laravel"', S), ("],", C)],
        [("    api", V), (":      [", C), ('"FastAPI"', S), (", ", C), ('"Python"', S), ("],", C)],
        [("    ai", V), (":       [", C), ('"OpenAI"', S), (", ", C), ('"RAG"', S), (", ", C), ('"Vector Search"', S), ("],", C)],
        [("    database", V), (": [", C), ('"PostgreSQL"', S), (", ", C), ('"MongoDB"', S), ("],", C)],
        [("  },", C)],
        [("", C)],
        [("  shipsOnTime", V), (": ", C), ("true", K), (",", C)],
        [("};", C)],
    ]
    y = 106
    for n, line in enumerate(code):
        b.append(f'<g class="in" style="animation-delay:{0.3 + n*0.055:.2f}s">')
        b.append(f'<text x="96" y="{y}" class="mono" font-size="11" fill="#484F58" '
                 f'text-anchor="end">{n+1}</text>')
        parts = "".join(f'<tspan fill="{col}" xml:space="preserve">{esc(t)}</tspan>'
                        for t, col in line)
        b.append(f'<text x="112" y="{y}" class="mono" font-size="13">{parts}</text>')
        b.append('</g>')
        y += 18

    # ── right: highlight cards ──
    cards = [
        ("🏗️", "I build end-to-end", "Frontend, backend and the AI layer — one\nengineer, no handoff gaps.", A1),
        ("🤖", "I ship AI-powered features", "RAG pipelines, embeddings and LLM APIs\nwired into real production apps.", A3),
        ("🔌", "I connect real systems", "10+ third-party integrations across\npayments, data and AI tooling.", A4),
    ]
    cy = 34
    for i, (icon, title, desc, col) in enumerate(cards):
        b.append(f'<g class="rise" style="animation-delay:{0.34 + i*0.12:.2f}s">')
        b.append(panel(706, cy, 424, 106, r=14))
        b.append(f'<rect x="706" y="{cy}" width="3.5" height="106" rx="2" fill="{col}"/>')
        b.append(f'<rect x="726" y="{cy+22}" width="36" height="36" rx="10" fill="{col}" fill-opacity=".14"/>')
        b.append(f'<text x="744" y="{cy+46}" font-size="18" text-anchor="middle">{icon}</text>')
        b.append(f'<text x="776" y="{cy+36}" font-size="16" font-weight="700" fill="{INK}">{esc(title)}</text>')
        for j, ln in enumerate(desc.split("\n")):
            b.append(f'<text x="776" y="{cy+58+j*17}" font-size="12.5" fill="{INK_FAINT}">{esc(ln)}</text>')
        b.append('</g>')
        cy += 122

    # ── bottom: focus tags ──
    b.append('<g class="rise" style="animation-delay:.8s">')
    b.append(f'<text x="72" y="424" font-size="11.5" font-weight="700" letter-spacing="2.2" '
             f'fill="{INK_FAINT}">WHAT I FOCUS ON</text>')
    x = 70
    for label, col in (("🌐 Full-Stack Web", A1), ("🤖 AI & RAG", A2),
                       ("🔌 API Integrations", A3), ("🗄️ Database Design", A4),
                       ("☁️ Deployment", A1)):
        g, w = chip(x, 444, label, fs=13, h=33, pad=17, fill=col, op=".1",
                    stroke=col + "55", color=INK)
        b.append(g)
        x += w + 10
    b.append('</g>')

    b.append('<g class="rise" style="animation-delay:.9s">')
    b.append(f'<rect x="70" y="500" width="1060" height="1" fill="{LINE}"/>')
    b.append(f'<text x="70" y="528" font-size="13.5" font-style="italic" fill="{INK_DIM}">'
             f'"Clean architecture, clear communication, fast shipping."</text>')
    b.append('</g>')
    return with_header(W, H, "".join(b), "01 — WHO I AM", "About me", A1, blobs=False)


# ──────────────────────────── 4. skills — ring grid ──────────────────────────

def skills():
    rows = [
        ("React / Next.js",            95, A1, "TypeScript · Tailwind · Redux"),
        ("Node.js / NestJS", 92, A2, "REST, WebSockets, auth"),
        ("PHP / Laravel",               85, A3, "Where it started"),
        ("Python / FastAPI",            77, A2, "REST APIs, scripting, automation"),
        ("AI / RAG / LLM tooling",      80, A4, "OpenAI, embeddings, vectors"),
        ("SQL / NoSQL",                 82, A1, "Postgres · Mongo · Supabase"),
        ("Git / CI / Deploy",           78, A3, "Actions, Docker, Vercel"),
    ]
    W = 1200
    COLS = 3
    TW = (1060 - 20 * (COLS - 1)) / COLS
    TH = 168
    ROWS = math.ceil(len(rows) / COLS)
    H = ROWS * TH + (ROWS - 1) * 20 + 20

    b = [backdrop(W, H + 20, blobs=False)]
    b.append(f'<g filter="url(#blur)" opacity=".2">'
             f'<circle class="blob" cx="120" cy="{H}" r="200" fill="{A1}"/></g>')

    for i, (label, pct, col, note) in enumerate(rows):
        r, c = divmod(i, COLS)
        x = 70 + c * (TW + 20)
        y = 20 + r * (TH + 20)
        d = 0.15 + i * 0.09
        b.append(f'<g class="rise" style="animation-delay:{d:.2f}s" filter="url(#soft)">')
        b.append(panel(x, y, TW, TH, r=16))
        b.append('</g>')
        cx, cy_ = x + 66, y + TH / 2
        b.append(ring(cx, cy_, 40, pct, col, delay=d + 0.15))
        b.append(f'<text x="{cx}" y="{cy_+6}" font-size="17" font-weight="800" fill="{INK}" '
                 f'text-anchor="middle" class="in" style="animation-delay:{d+0.5:.2f}s">{pct}%</text>')
        tx = x + 128
        b.append(f'<text x="{tx}" y="{y+62}" font-size="14.5" font-weight="700" fill="{INK}">{esc(label)}</text>')
        b.append(f'<text x="{tx}" y="{y+84}" font-size="11.5" fill="{INK_FAINT}">{note}</text>')
    return svg(W, H, "".join(b), rounded=20)


# ────────────────────── 5. journey — vertical zig-zag ────────────────────────

def projects():
    items = [
        ("🩺", "Skannr", "UK medical scan booking platform — patient/doctor flows, MVC architecture, payments.", A1,
         ["React", "Node.js", "Next.js", "PostgreSQL", "Stripe"], "skannr.com"),
        ("🏛️", "ICMPD — R3P Platform", "Government system tracking returnee case management, counseling and vocational training.", A3,
         ["Next.js", "NestJS", "PostgreSQL", "REST APIs"], "icmpd-fe.govt.septemsystems.com"),
        ("🐾", "VOP — Veterinary Online Platform", "Connects pet owners with vets — consultations, billing, multi-role access.", A4,
         ["Next.js", "NestJS", "PostgreSQL", "REST APIs"], "vop-fe.govt.septemsystems.com"),
        ("🥊", "FightBook", "Fighter/promoter platform with identity verification and notifications.", A2,
         ["NestJS", "Veriff", "Firebase", "Knock"], None),
        ("🏢", "Kiewit Real Estate", "Real estate backend with real-time socket updates and cloud file storage.", A1,
         ["NestJS", "WebSockets", "AWS S3"], None),
    ]
    W = 1200
    CW, GAP = 516, 28
    CH = 200
    rows = (len(items) + 1) // 2
    H = rows * (CH + GAP) - GAP + 20
    b = [f'<g filter="url(#blur)" opacity=".2">'
         f'<circle class="blob" cx="1060" cy="90" r="210" fill="{A3}"/>'
         f'<circle class="blob2" cx="120" cy="{H-90}" r="200" fill="{A1}"/></g>']

    for i, (icon, title, desc, col, tags, link) in enumerate(items):
        cx = 70 + (i % 2) * (CW + GAP)
        cy = 20 + (i // 2) * (CH + GAP)
        d = 0.1 + i * 0.09
        b.append(f'<g class="rise" style="animation-delay:{d:.2f}s" filter="url(#soft)">')
        b.append(panel(cx, cy, CW, CH, r=16))
        # gradient top edge, uniform across every card like a hovered browser tab
        b.append(f'<path d="M{cx} {cy+16}a16 16 0 0 1 16-16h{CW-32}a16 16 0 0 1 16 16v2H{cx}z" '
                 f'fill="url(#accent)"/>')
        b.append(f'<rect x="{cx+24}" y="{cy+24}" width="42" height="42" rx="12" fill="{col}" fill-opacity=".14"/>')
        b.append(f'<text x="{cx+45}" y="{cy+51}" font-size="20" text-anchor="middle">{icon}</text>')
        b.append(f'<text x="{cx+82}" y="{cy+40}" font-size="16.5" font-weight="750" fill="{INK}">{esc(title)}</text>')
        if link:
            b.append(f'<text x="{cx+82}" y="{cy+58}" font-size="11" font-weight="600" fill="{col}">{esc(link)}</text>')
        words = desc.split(" ")
        wrapped, cur = [], ""
        for wd in words:
            if len(cur + " " + wd) > 58:
                wrapped.append(cur); cur = wd
            else:
                cur = (cur + " " + wd).strip()
        wrapped.append(cur)
        yoff = cy + (82 if link else 74)
        for j, ln in enumerate(wrapped):
            b.append(f'<text x="{cx+24}" y="{yoff+j*18}" font-size="12.5" fill="{INK_DIM}">{esc(ln)}</text>')
        tx = cx + 24
        ty = cy + CH - 30
        for t in tags:
            g, w = chip(tx, ty, t, fs=11, h=24, pad=11, fill="#FFFFFF", op=".06",
                        stroke=LINE, color=INK_DIM)
            b.append(g)
            tx += w + 8
        b.append(f'<text x="{cx+CW-24}" y="{cy+CH-18}" font-size="12" font-weight="700" '
                 f'fill="{col}" text-anchor="end">production ●</text>')
        b.append('</g>')
    return with_header(W, H, "".join(b), "03 — WHAT I'VE BUILT", "Selected projects", A2, blobs=False)


def timeline():
    stops = [
        ("Mar 2023 — Nov 2024", "Nex Developers ltd", "Full Stack Engineer · Part-time · Remote (UK)", A1,
         ["Worked remotely with a London-based team on",
          "Express.js + PostgreSQL products, part-time",
          "alongside other commitments."]),
        ("Dec 2024 — Nov 2025", "ILSA Interactive", "Software Engineer · Full-time · Lahore", A3,
         ["Backend-focused engineering with Express.js",
          "and PostgreSQL, on-site with the Lahore team."]),
        ("Nov 2025 — Present", "Septem Systems", "Full Stack Engineer · Full-time · Lahore", A4,
         ["Current role. Full-stack delivery with",
          "JavaScript, React.js and the modern",
          "Node.js toolkit."]),
    ]
    W = 1200
    ROW_H = 168
    H = len(stops) * ROW_H + 60
    b = [f'<g filter="url(#blur)" opacity=".16">'
         f'<circle class="blob" cx="600" cy="{H//2}" r="240" fill="{A2}"/></g>']

    b.append(f'<text x="70" y="14" font-size="16.5" font-weight="700" fill="{INK}">'
             f'3+ years · 3 companies · 15+ projects shipped</text>')

    cx = 600
    b.append(f'<line x1="{cx}" y1="40" x2="{cx}" y2="{H-30}" stroke="{LINE}" stroke-width="2"/>')
    b.append(f'<line x1="{cx}" y1="40" x2="{cx}" y2="{H-30}" stroke="url(#accentV)" stroke-width="2" '
             f'class="bar" style="animation-delay:.2s;transform-origin:top center;"/>')

    CARD_W = 430
    for i, (period, org, role, col, lines) in enumerate(stops):
        cy_ = 40 + i * ROW_H + ROW_H / 2 - 10
        left = (i % 2 == 0)
        d = 0.3 + i * 0.16
        anim = "slide" if left else "slideR"
        b.append(f'<circle cx="{cx}" cy="{cy_}" r="9" fill="{col}" opacity=".3" class="ping" '
                 f'style="animation-delay:{d+0.7:.2f}s"/>')
        b.append(f'<circle cx="{cx}" cy="{cy_}" r="8" fill="{BG}" stroke="{col}" stroke-width="3"/>')
        b.append(f'<circle cx="{cx}" cy="{cy_}" r="3" fill="{col}"/>')

        card_x = (cx - 50 - CARD_W) if left else (cx + 50)
        conn_x1 = card_x + (CARD_W if left else 0)
        b.append(f'<line x1="{conn_x1}" y1="{cy_}" x2="{cx}" y2="{cy_}" stroke="{col}" '
                 f'stroke-width="1.5" stroke-dasharray="3 4" opacity=".6"/>')

        card_h = 128
        card_y = cy_ - card_h / 2
        b.append(f'<g class="{anim}" style="animation-delay:{d:.2f}s" filter="url(#soft)">')
        b.append(panel(card_x, card_y, CARD_W, card_h, r=14))
        edge_x = card_x + (CARD_W - 3 if left else 0)
        b.append(f'<rect x="{edge_x}" y="{card_y}" width="3" height="{card_h}" fill="{col}"/>')
        pad = 28
        b.append(f'<text x="{card_x+pad}" y="{card_y+30}" font-size="11.5" font-weight="700" '
                 f'letter-spacing=".5" fill="{INK_FAINT}">{esc(period)}</text>')
        b.append(f'<text x="{card_x+pad}" y="{card_y+56}" font-size="18" font-weight="750" '
                 f'fill="{INK}">{esc(org)}</text>')
        b.append(f'<text x="{card_x+pad}" y="{card_y+76}" font-size="12" font-weight="600" '
                 f'fill="{col}">{esc(role)}</text>')
        for j, ln in enumerate(lines):
            b.append(f'<text x="{card_x+pad}" y="{card_y+98+j*16}" font-size="11.5" '
                     f'fill="{INK_DIM}">{esc(ln)}</text>')
        b.append('</g>')

    b.append(f'<g class="in" style="animation-delay:1.1s">')
    b.append(f'<text x="600" y="{H-8}" font-size="12.5" font-weight="600" fill="{A3}" '
             f'text-anchor="middle">● open to new opportunities</text>')
    b.append('</g>')
    return with_header(W, H, "".join(b), "04 — WHERE I'VE BEEN", "Career journey", A4, blobs=False)


# ──────────────────────────── 6. contact panel ──────────────────────────────

def contact():
    W, H = 1200, 244
    b = []
    b.append(f'<text x="600" y="76" font-size="30" font-weight="800" letter-spacing="-.6" '
             f'fill="{INK}" text-anchor="middle" class="rise">Let&#39;s build something '
             f'<tspan fill="url(#accent)">great</tspan>.</text>')
    b.append(f'<text x="600" y="110" font-size="14.5" fill="{INK_DIM}" text-anchor="middle" '
             f'class="rise" style="animation-delay:.12s">Got an idea that needs building, or a team '
             f'that needs a full-stack engineer? My inbox is open.</text>')
    b.append('<g class="rise" style="animation-delay:.24s">')
    b.append(f'<rect x="410" y="142" width="380" height="1" fill="url(#fade)"/>')
    b.append(f'<text x="600" y="176" class="mono" font-size="14" fill="{A3}" text-anchor="middle">'
             f'alihusnaindhaulka124@gmail.com</text>')
    b.append(f'<text x="600" y="206" font-size="12" fill="{INK_FAINT}" text-anchor="middle">'
             f'Usually replies within a day · Lahore, Pakistan · Available for collaboration</text>')
    b.append('</g>')
    b.append(f'<path d="M592 226l8 9 8-9" stroke="{INK_FAINT}" stroke-width="2" '
             f'stroke-linecap="round" fill="none" class="bob"/>')
    return with_header(W, H, "".join(b), "06 — SAY HELLO", "Get in touch", A3)


# ──────────────────────────────── 7. footer ─────────────────────────────────

def footer():
    W, H = 1200, 132
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<rect width="{W}" height="{H}" fill="url(#dots)" opacity=".6"/>',
         f'<g filter="url(#blur)" opacity=".4">'
         f'<circle class="blob" cx="300" cy="150" r="150" fill="{A1}"/>'
         f'<circle class="blob2" cx="900" cy="150" r="150" fill="{A4}"/></g>',
         f'<rect y="0" width="{W}" height="2" fill="url(#accent)"/>']
    b.append(f'<text x="600" y="52" font-size="17" font-weight="700" fill="{INK}" '
             f'text-anchor="middle" class="rise">Thanks for scrolling all the way down 👋</text>')
    b.append(f'<text x="600" y="78" class="mono in" font-size="12.5" fill="{INK_FAINT}" '
             f'text-anchor="middle">'
             f'built by Ali Husnain · hand-rolled SVG, no page builder</text>')
    b.append(f'<text x="600" y="106" font-size="12" fill="{INK_FAINT}" text-anchor="middle">'
             f'⭐ Star a repo if it helped you</text>')
    return svg(W, H, "".join(b), rounded=20)


# ─────────────────────────── 8. bits and pieces ─────────────────────────────

def button(name, label, w, primary=False):
    H = 46
    b = []
    if primary:
        b.append(f'<rect x="1" y="4" width="{w-2}" height="{H-8}" rx="10" fill="url(#accent)"/>')
        fill = "#080808"
    else:
        b.append(f'<rect x="1" y="4" width="{w-2}" height="{H-8}" rx="10" fill="{CARD}" '
                 f'stroke="{LINE}" stroke-width="1.4"/>')
        fill = INK
    b.append(f'<text x="{w/2}" y="{H/2 + 5}" font-size="14" font-weight="700" fill="{fill}" '
             f'text-anchor="middle">{esc(label)}</text>')
    write(name, svg(w, H, "".join(b)))


def navitem(name, label, w, active=False):
    """Underline-tab style nav item (distinct from a pill button)."""
    H = 40
    b = [f'<text x="{w/2}" y="20" font-size="13.5" font-weight="650" '
         f'fill="{INK if active else INK_DIM}" text-anchor="middle">{esc(label)}</text>']
    if active:
        b.append(f'<rect x="6" y="30" width="{w-12}" height="2.5" rx="1.25" fill="url(#accent)"/>')
    else:
        b.append(f'<rect x="6" y="30" width="{w-12}" height="1" fill="{LINE}"/>')
    write(name, svg(w, H, "".join(b)))


# ──────────────────────────────── build ─────────────────────────────────────

if __name__ == "__main__":
    print("building assets/")
    write("hero.svg", hero())
    write("about.svg", about())
    write("skills.svg", skills())
    write("projects.svg", projects())
    write("timeline.svg", timeline())
    write("contact.svg", contact())
    write("footer.svg", footer())

    section("stack", "02 — WHAT I USE",  "Tech arsenal",    A2)
    section("stats", "05 — THE NUMBERS", "GitHub activity", A1)

    for slug, label, w in (("about", "About", 84), ("stack", "Stack", 80),
                           ("projects", "Projects", 104), ("journey", "Journey", 96),
                           ("stats", "Stats", 80), ("contact", "Contact", 96)):
        navitem(f"nav-{slug}.svg", label, w)

    button("btn-linkedin.svg", "LinkedIn  ↗", 168, primary=True)
    button("btn-email.svg",    "Email me  ✉", 156)
    button("btn-github.svg",   "Follow  ★",   142)
    button("btn-portfolio.svg", "Portfolio  ↗", 168)
    button("cta-journey.svg",  "View my journey ↓", 220, primary=True)
    button("cta-contact.svg",  "Get in touch", 168)
    print("done.")
