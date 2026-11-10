"""CHROMA//SCAN - Clasificador de color a partir de un código HEX (versión Streamlit).

Estética Y2K / software P2P underground.
Ejecutar en local:  streamlit run app.py
"""
import time

import streamlit as st

st.set_page_config(page_title="CHROMA//SCAN · Clasificador de color", page_icon="🎨", layout="wide")

PASOS = ["Validar HEX", "Convertir a RGB", "Luminosidad", "Temperatura", "Salida"]


# ----------------------------------------------------------------------
# Lógica del algoritmo (la misma del programa de consola)
# ----------------------------------------------------------------------
def leer_hex(texto):
    """Devuelve el HEX de 6 caracteres en mayúsculas, o None si es inválido."""
    codigo = texto.strip().lstrip("#").upper()
    if len(codigo) == 6 and all(c in "0123456789ABCDEF" for c in codigo):
        return codigo
    return None


def clasificar(codigo):
    """Convierte HEX a RGB y clasifica claridad, temperatura y texto sugerido."""
    r, g, b = int(codigo[0:2], 16), int(codigo[2:4], 16), int(codigo[4:6], 16)
    luminosidad = 0.299 * r + 0.587 * g + 0.114 * b
    diferencia = r - b
    claro = luminosidad >= 128
    if abs(diferencia) <= 30:
        temperatura = "neutro"
    elif diferencia > 0:
        temperatura = "cálido"
    else:
        temperatura = "frío"
    return {"codigo": codigo, "r": r, "g": g, "b": b, "lum": luminosidad, "dif": diferencia,
            "claridad": "claro" if claro else "oscuro",
            "texto": "oscuro" if claro else "claro", "temp": temperatura}


# ----------------------------------------------------------------------
# Estilos
# ----------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Anton&family=IBM+Plex+Mono:wght@400;700&display=swap');
:root{--paper:#d9d9d2;--card:#e9e9e3;--ink:#0a0a0a;--r:#f2212b;--c:#00b7d6;--ok:#6fcf00;
--mono:'IBM Plex Mono','Courier New',monospace;--disp:'Anton','Arial Narrow',Impact,sans-serif}
#MainMenu,header[data-testid="stHeader"],footer{visibility:hidden;height:0}
.stApp{background-color:var(--paper);color:var(--ink);font-family:var(--mono);
background-image:url("data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)' opacity='.16'/%3E%3C/svg%3E"),
linear-gradient(rgba(0,0,0,.08) 1px,transparent 1px),linear-gradient(90deg,rgba(0,0,0,.08) 1px,transparent 1px);
background-size:160px 160px,24px 24px,24px 24px}
.block-container{max-width:1080px;padding:1.2rem 1rem 2rem}
html,body,[class*="css"],p,label,span,div{font-family:var(--mono)}
.tb{display:flex;justify-content:space-between;background:var(--ink);color:var(--card);padding:4px 10px;font-weight:700;font-size:13px;margin-top:6px}
.menu{display:flex;gap:18px;padding:4px 10px;border:1px solid var(--ink);border-top:0;background:var(--card);font-size:12px}
.menu .r{margin-left:auto;opacity:.7}
.hd{display:flex;flex-wrap:wrap;gap:8px 28px;align-items:flex-end;justify-content:space-between;
background:var(--card);border:1px solid var(--ink);border-top:0;padding:16px 16px 12px}
.glitch{position:relative;margin:0;padding:0;font:400 clamp(34px,7.5vw,84px)/.92 var(--disp);text-transform:uppercase}
.glitch::before,.glitch::after{content:attr(data-text);position:absolute;inset:0;pointer-events:none;mix-blend-mode:multiply}
.glitch::before{color:var(--r);transform:translate(-3px,0);animation:g1 3.2s infinite steps(1)}
.glitch::after{color:var(--c);transform:translate(3px,0);animation:g2 3.2s infinite steps(1)}
@keyframes g1{0%,86%,100%{clip-path:inset(0)}88%{clip-path:inset(8% 0 62% 0);transform:translate(-9px,0)}93%{clip-path:inset(58% 0 10% 0);transform:translate(-4px,0)}}
@keyframes g2{0%,84%,100%{clip-path:inset(0)}87%{clip-path:inset(40% 0 35% 0);transform:translate(9px,0)}95%{clip-path:inset(5% 0 75% 0);transform:translate(5px,0)}}
.hd p{margin:0;max-width:300px;font-size:12px}
[class*="st-key-mod"]{background:var(--card);border:1px solid var(--ink);padding:12px 14px 16px;margin-top:-1px}
h2.m{margin:0 0 10px;font:400 20px/1 var(--disp);text-transform:uppercase;letter-spacing:.04em;
display:flex;justify-content:space-between;border-bottom:1px solid var(--ink);padding-bottom:4px}
h2.m span{font:400 11px var(--mono);letter-spacing:0;align-self:flex-end}
.stTextInput input{font:700 20px var(--mono);letter-spacing:.06em;text-transform:uppercase;border:1px solid var(--ink);border-radius:0;background:var(--paper);color:var(--ink)}
.stTextInput div[data-baseweb]{border-radius:0;border:0;background:transparent}
.stButton>button{width:100%;height:42px;border-radius:0;border:1px solid var(--ink);background:var(--ink);color:var(--card);font:700 13px var(--mono)}
.stButton>button:hover{background:var(--card);color:var(--ink);border-color:var(--ink)}
[data-testid="stColorPicker"] label{display:none}
[data-testid="stColorPicker"] div[data-baseweb]{border-radius:0}
.bar{position:relative;height:18px;border:1px solid var(--ink);background:var(--paper);overflow:hidden}
.bar i{position:absolute;left:0;top:0;bottom:0;background:var(--col,var(--ink))}
.bar::after{content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0 8px,var(--card) 8px 10px)}
.bar b{position:absolute;top:0;bottom:0;width:2px;background:var(--ink);z-index:2}
.bar u{position:absolute;top:0;bottom:0;left:44.1%;width:11.8%;background:rgba(128,128,128,.35);z-index:1}
.lb{display:flex;justify-content:space-between;font-size:11px;margin:3px 0 9px}
ol.st{list-style:none;margin:10px 0 0;padding:0;font-size:12px}
ol.st li{display:flex;justify-content:space-between;border-bottom:1px dotted var(--ink);padding:2px 4px}
ol.st li.run{background:var(--ink);color:var(--card)}
ol.st li.err{color:var(--r);font-weight:700}
.err{min-height:18px;margin:6px 0;color:var(--r);font-weight:700;font-size:13px}
.sw{height:150px;border:1px solid var(--ink);display:flex;flex-direction:column;justify-content:space-between;padding:10px 12px}
.sw strong{font:400 44px/1 var(--disp);letter-spacing:.03em}
.rd{display:grid;grid-template-columns:repeat(3,1fr);margin-top:10px;border:1px solid var(--ink)}
.rd div{padding:6px 8px;border-right:1px solid var(--ink)}
.rd div:last-child{border:0}
.rd small{display:block;font-size:10px;opacity:.7}
.rd b{font:400 22px/1.1 var(--disp);text-transform:uppercase}
.tw{overflow-x:auto}
table.h{width:100%;border-collapse:collapse;font-size:12px;min-width:520px}
table.h th,table.h td{border:1px solid var(--ink);padding:3px 8px;text-align:left}
table.h th{background:var(--ink);color:var(--card)}
.chip{display:inline-block;width:12px;height:12px;border:1px solid var(--ink);vertical-align:-1px;margin-right:6px}
.sb{display:flex;flex-wrap:wrap;gap:4px 18px;padding:4px 10px;font-size:11px;border:1px solid var(--ink);border-top:0;background:var(--card)}
@media (prefers-reduced-motion:reduce){.glitch::before,.glitch::after{animation:none}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ----------------------------------------------------------------------
# Componentes HTML
# ----------------------------------------------------------------------
def barra(frac, color="#0a0a0a"):
    return f'<div class="bar"><i style="width:{max(0, min(1, frac)) * 100:.1f}%;--col:{color}"></i></div>'


def pasos_html(estados):
    marca = {"": "[ ]", "run": "[&gt;&gt;]", "ok": "[OK]", "err": "[!!]"}
    filas = "".join(f'<li class="{e}"><span>{n}</span><span>{marca[e]}</span></li>' for n, e in zip(PASOS, estados))
    return f'<ol class="st">{filas}</ol>'


def titulo(texto, nota=""):
    return f'<h2 class="m">{texto}<span>{nota}</span></h2>'


# ----------------------------------------------------------------------
# Estado y callbacks
# ----------------------------------------------------------------------
ss = st.session_state
ss.setdefault("hex_txt", "#FF8C00")
ss.setdefault("hex_pick", "#ff8c00")
ss.setdefault("hist_sel", "—")
ss.setdefault("run", True)
ss.setdefault("hist", [])
ss.setdefault("res", None)
ss.setdefault("estados", [""] * len(PASOS))
ss.setdefault("error", "")


def pedir():
    ss.run = True


def desde_selector():
    ss.hex_txt = ss.hex_pick.upper()
    ss.run = True


def desde_historial():
    if ss.hist_sel != "—":
        ss.hex_txt = ss.hist_sel
        ss.run = True
    ss.hist_sel = "—"


# Normaliza el código ANTES de crear los widgets (Streamlit no permite cambiarlos después)
codigo = leer_hex(ss.hex_txt) if ss.run else None
if codigo:
    ss.hex_txt = "#" + codigo
    ss.hex_pick = "#" + codigo.lower()

# ----------------------------------------------------------------------
# Interfaz
# ----------------------------------------------------------------------
st.markdown(
    '<div class="tb"><span>■ CHROMA//SCAN.EXE</span><span>_ &nbsp;□ &nbsp;×</span></div>'
    '<div class="menu"><span>ARCHIVO</span><span>EDITAR</span><span>VER</span><span>AYUDA</span>'
    '<span class="r">HEX → RGB → CRITERIO</span></div>'
    '<header class="hd"><h1 class="glitch" data-text="Clasificador de color">Clasificador de color</h1>'
    '<p>Escriba un código HEX. Se decide si el color es claro u oscuro, cálido, frío o neutro, '
    'y qué tono de texto contrasta mejor.</p></header>',
    unsafe_allow_html=True,
)

izq, der = st.columns(2, gap="small")

with izq:
    with st.container(key="mod_entrada"):
        st.markdown(titulo("Entrada", "cola local"), unsafe_allow_html=True)
        c1, c2, c3 = st.columns([5, 1.2, 2.4])
        c1.text_input("Código HEX", key="hex_txt", max_chars=9, on_change=pedir, label_visibility="collapsed")
        c2.color_picker("Elegir color", key="hex_pick", on_change=desde_selector, label_visibility="collapsed")
        c3.button("ANALIZAR", on_click=pedir)
        ph_error = st.empty()
        ph_prog = st.empty()
        ph_pasos = st.empty()

        if ss.run:
            ss.run = False
            if codigo is None:
                ss.error = "Código inválido. Use 6 caracteres entre 0-9 y A-F, por ejemplo #FF8C00."
                ss.estados = ["err", "", "", "", ""]
                ph_prog.markdown(barra(0, "#6fcf00"), unsafe_allow_html=True)
            else:
                ss.error = ""
                estados = [""] * len(PASOS)
                for i in range(len(PASOS)):
                    estados[i] = "run"
                    ph_pasos.markdown(pasos_html(estados), unsafe_allow_html=True)
                    ph_prog.markdown(barra((i + 1) / len(PASOS), "#6fcf00"), unsafe_allow_html=True)
                    time.sleep(0.15)
                    estados[i] = "ok"
                ss.estados = estados
                ss.res = clasificar(codigo)
                ss.hist.insert(0, ss.res)
                del ss.hist[8:]
        else:
            ph_prog.markdown(barra(1 if ss.estados[0] == "ok" else 0, "#6fcf00"), unsafe_allow_html=True)

        ph_error.markdown(f'<div class="err">{ss.error}</div>', unsafe_allow_html=True)
        ph_pasos.markdown(pasos_html(ss.estados), unsafe_allow_html=True)

    res = ss.res
    with st.container(key="mod_canales"):
        st.markdown(titulo("Canales RGB", "0-255"), unsafe_allow_html=True)
        for canal, color in (("r", "#e5202a"), ("g", "#2fa84f"), ("b", "#2a5bd7")):
            valor = res[canal] if res else 0
            st.markdown(barra(valor / 255, color) + f'<div class="lb"><span>{canal.upper()}</span><span>{valor}</span></div>',
                        unsafe_allow_html=True)

with der:
    res = ss.res
    with st.container(key="mod_resultado"):
        fondo = "#" + res["codigo"] if res else "#d9d9d2"
        tinta = "#0a0a0a" if (not res or res["texto"] == "oscuro") else "#f5f5f0"
        st.markdown(titulo("Resultado", fondo), unsafe_allow_html=True)
        st.markdown(
            f'<div class="sw" style="background:{fondo};color:{tinta}"><span>Texto de muestra</span>'
            f'<strong>{fondo}</strong></div>'
            f'<div class="rd"><div><small>Claridad</small><b>{res["claridad"] if res else "--"}</b></div>'
            f'<div><small>Temperatura</small><b>{res["temp"] if res else "--"}</b></div>'
            f'<div><small>Texto sugerido</small><b>{res["texto"] if res else "--"}</b></div></div>',
            unsafe_allow_html=True,
        )

    with st.container(key="mod_indicadores"):
        st.markdown(titulo("Luminosidad / Temperatura", "umbral 128 · ±30"), unsafe_allow_html=True)
        lum = res["lum"] if res else 0
        dif = res["dif"] if res else 0
        st.markdown(
            f'<div class="bar"><i style="width:{lum / 255 * 100:.1f}%"></i><b style="left:50.2%"></b></div>'
            f'<div class="lb"><span>OSCURO</span><span><b>{lum:.1f}</b></span><span>CLARO</span></div>'
            f'<div class="bar"><u></u><b style="left:50%"></b>'
            f'<b style="left:calc({50 + dif / 255 * 50:.1f}% - 3px);width:6px;background:#f2212b"></b></div>'
            f'<div class="lb"><span>FRÍO</span><span><b>{dif:+d}</b></span><span>CÁLIDO</span></div>',
            unsafe_allow_html=True,
        )

with st.container(key="mod_historial"):
    st.markdown(titulo("Historial de análisis", f"{len(ss.hist)} archivo" + ("" if len(ss.hist) == 1 else "s")),
                unsafe_allow_html=True)
    filas = "".join(
        f'<tr><td><span class="chip" style="background:#{h["codigo"]}"></span>#{h["codigo"]}</td>'
        f'<td>{h["r"]}</td><td>{h["g"]}</td><td>{h["b"]}</td><td>{h["claridad"]}</td>'
        f'<td>{h["temp"]}</td><td>{h["texto"]}</td></tr>' for h in ss.hist)
    st.markdown(
        '<div class="tw"><table class="h"><thead><tr><th>HEX</th><th>R</th><th>G</th><th>B</th>'
        f'<th>Claridad</th><th>Temperatura</th><th>Texto</th></tr></thead><tbody>{filas}</tbody></table></div>',
        unsafe_allow_html=True,
    )
    st.selectbox("Volver a analizar un color del historial", ["—"] + ["#" + h["codigo"] for h in ss.hist],
                 key="hist_sel", on_change=desde_historial)

st.markdown(
    '<div class="sb"><span>ESTADO: LISTO</span><span>LUM = 0.299R + 0.587G + 0.114B</span>'
    '<span>|R − B| ≤ 30 → NEUTRO</span></div>',
    unsafe_allow_html=True,
)
