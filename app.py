"""
========================================================================
  La IA como Sistema Operativo del Asesor de Negocios
  Tablero de Visualización de Datos — Proyecto Final
  Reyes Betancourt García · Especialidad en IA y Ciencia de Datos
========================================================================
No asesoro desde la teoría: construyo sistemas. La IA es la capa que me
lleva de la estrategia a la entrega técnica end-to-end. Orey AI es el
copiloto que orquesta seis ventures y se replica dentro de cada uno.

Ejecutar:  streamlit run app.py
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

from components.graph import orey_graph

st.set_page_config(
    page_title="IA · Sistema Operativo del Asesor",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Paleta "Deep Signal" ---
INK    = "#0B1220"
PANEL  = "#111C2E"
LINE   = "#1F2E44"
TEXT   = "#E6EDF7"
MUTED  = "#7C8CA6"
CYAN   = "#38E1D6"
BLUE   = "#4C7DFF"
AMBER  = "#F5B455"
VIOLET = "#9B7DFF"
GREEN  = "#5FD3A0"

PLOT_SEQ = [CYAN, BLUE, AMBER, VIOLET, GREEN, "#FF7D9C"]
PLOT_FONT = dict(family="Inter, system-ui, sans-serif", color=MUTED, size=13)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

.stApp {{
  background:
    radial-gradient(1100px 560px at 85% -8%, rgba(56,225,214,0.10), transparent 60%),
    radial-gradient(820px 440px at -8% 8%, rgba(76,125,255,0.08), transparent 55%),
    {INK};
}}
#MainMenu, footer {{ visibility: hidden; }}
header[data-testid="stHeader"] {{ background: transparent; }}
.block-container {{ padding-top: 2rem; max-width: 1200px; }}

h1,h2,h3 {{ font-family:'Space Grotesk',sans-serif !important; color:{TEXT}; letter-spacing:-0.5px; }}
p,div,span,li {{ font-family:'Inter',sans-serif; }}

@keyframes rise {{ from {{opacity:0; transform:translateY(14px);}} to {{opacity:1; transform:translateY(0);}} }}
.rise {{ animation: rise .7s cubic-bezier(.2,.7,.3,1) both; }}
.d1{{animation-delay:.05s}} .d2{{animation-delay:.15s}} .d3{{animation-delay:.28s}}
.d4{{animation-delay:.42s}} .d5{{animation-delay:.56s}}

.eyebrow {{ font-family:'JetBrains Mono',monospace; font-size:0.72rem; letter-spacing:3px;
  text-transform:uppercase; color:{CYAN}; margin-bottom:0.4rem; }}
.hero-title {{ font-size:3.0rem; line-height:1.04; font-weight:700; margin:0.1rem 0 0.6rem; }}
.hero-title .hl {{ background:linear-gradient(100deg,{CYAN},{BLUE});
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; }}
.hero-sub {{ font-size:1.06rem; color:{MUTED}; max-width:730px; line-height:1.58; }}
.hero-sub b {{ color:{TEXT}; }}

.rule {{ height:1px; background:linear-gradient(90deg,{CYAN},transparent); border:0; margin:2.1rem 0 1.5rem; }}
.rule-soft {{ height:1px; background:{LINE}; border:0; margin:2rem 0 1.4rem; }}

.sec-h {{ font-size:1.55rem; font-weight:700; margin:0.2rem 0 0.2rem; }}
.sec-p {{ color:{MUTED}; font-size:0.93rem; max-width:780px; line-height:1.55; }}

.kpi {{ background:linear-gradient(160deg,rgba(255,255,255,0.04),rgba(255,255,255,0.01));
  border:1px solid {LINE}; border-radius:16px; padding:1.05rem 1.2rem; height:100%;
  transition:transform .2s, border-color .2s; }}
.kpi:hover {{ transform:translateY(-4px); border-color:{CYAN}; }}
.kpi-label {{ font-size:0.72rem; letter-spacing:1.5px; text-transform:uppercase; color:{MUTED}; font-weight:600; }}
.kpi-value {{ font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:2.1rem; color:{CYAN}; line-height:1.1; margin:.25rem 0 .1rem; }}
.kpi-foot {{ font-size:0.76rem; color:#5E6E86; }}

.card {{ background:{PANEL}; border:1px solid {LINE}; border-radius:14px; padding:1.05rem 1.15rem; height:100%;
  transition:transform .2s, border-color .2s, box-shadow .2s; }}
.card:hover {{ transform:translateY(-5px); border-color:{CYAN}; box-shadow:0 14px 34px rgba(0,0,0,.35); }}
.card .vert {{ font-family:'JetBrains Mono',monospace; font-size:0.66rem; letter-spacing:2px; text-transform:uppercase; color:{CYAN}; }}
.card .name {{ font-family:'Space Grotesk',sans-serif; font-size:1.14rem; font-weight:600; margin:.25rem 0 .35rem; }}
.card .desc {{ font-size:0.85rem; color:{MUTED}; line-height:1.5; min-height:62px; }}
.card .ia {{ font-size:0.78rem; color:{VIOLET}; margin-top:.5rem; line-height:1.4; }}
.chip {{ display:inline-block; font-family:'JetBrains Mono',monospace; font-size:0.64rem; color:{TEXT};
  background:{INK}; border:1px solid {LINE}; border-radius:20px; padding:2px 9px; margin:2px 3px 0 0; }}
.phase {{ font-family:'JetBrains Mono',monospace; font-size:0.64rem; padding:2px 8px; border-radius:20px; margin-top:.55rem; display:inline-block; }}
.p-prod {{ color:{GREEN}; border:1px solid {GREEN}; }}
.p-dev  {{ color:{BLUE};  border:1px solid {BLUE}; }}
.p-plan {{ color:{AMBER}; border:1px solid {AMBER}; }}

.insight {{ border-left:3px solid {CYAN}; background:rgba(56,225,214,0.06);
  border-radius:0 12px 12px 0; padding:.9rem 1.1rem; margin:.4rem 0 1rem; color:{TEXT}; font-size:.94rem; line-height:1.55; }}
.insight b {{ color:{CYAN}; }}

.orey-band {{ background:linear-gradient(135deg,rgba(56,225,214,0.08),rgba(76,125,255,0.05));
  border:1px solid {LINE}; border-left:3px solid {CYAN}; border-radius:12px; padding:1.15rem 1.35rem; }}

.gate {{ display:inline-block; font-family:'Inter',sans-serif; font-size:.78rem; color:{TEXT};
  background:{PANEL}; border:1px solid {LINE}; border-radius:10px; padding:6px 11px; margin:4px 5px 0 0;
  transition:border-color .2s, transform .15s; }}
.gate:hover {{ border-color:{GREEN}; transform:translateY(-2px); }}
.gate b {{ color:{GREEN}; font-family:'JetBrains Mono',monospace; }}

.flow-row {{ display:flex; align-items:center; gap:6px; flex-wrap:wrap; margin:.6rem 0; }}
.stage {{ font-family:'JetBrains Mono',monospace; font-size:.74rem; padding:7px 12px; border-radius:10px;
  border:1px solid {LINE}; color:{TEXT}; background:{PANEL}; }}
.stage.s0{{border-color:{VIOLET};color:{VIOLET}}} .stage.s1{{border-color:{AMBER};color:{AMBER}}}
.stage.s2{{border-color:{BLUE};color:{BLUE}}} .stage.s3{{border-color:{GREEN};color:{GREEN}}}
.stage.s4{{border-color:{CYAN};color:{CYAN}}}
.arrow {{ color:{MUTED}; font-size:.9rem; }}

section[data-testid="stSidebar"] {{ background:#0C1524; border-right:1px solid {LINE}; }}
.side-brand {{ font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:1.2rem; color:{TEXT}; }}
.side-sub {{ color:{MUTED}; font-size:.78rem; }}

.foot {{ color:#5E6E86; font-size:.8rem; text-align:center; margin-top:2rem; padding-top:1rem;
  border-top:1px solid {LINE}; font-family:'JetBrains Mono',monospace; }}
</style>
""", unsafe_allow_html=True)

# --- DATOS REALES ---
PROJECTS = [
    {"id":"uege","name":"UEGE / Gastro","vertical":"Salud","phase":"Desarrollo",
     "stack":["Supabase","Lovable","React","TypeScript"],
     "desc":"Sistema operativo para clínica de gastroenterología: schema, landing pública y app operativa.",
     "ia":"IA: generación de schema y corrección de prompts (20+ errores → v3 verificado).",
     "hours":10, "accel":0.55},
    {"id":"dentwork","name":"Dentwork","vertical":"Salud","phase":"Plan",
     "stack":["Supabase","Lovable","React"],
     "desc":"Plataforma para gestión de espacio dental. Bloqueada por una decisión de arquitectura.",
     "ia":"IA: diseño de arquitectura y ADRs asistidos.",
     "hours":6, "accel":0.50},
    {"id":"barber","name":"BarberBROTHER","vertical":"Retail/Servicios","phase":"Plan",
     "stack":["Supabase","Lovable","React"],
     "desc":"Sistema de operación para barbería. En auditoría de diseño previa a implementación.",
     "ia":"IA: auditoría de diseño operativo y definición de entidades.",
     "hours":6, "accel":0.45},
    {"id":"zvezda","name":"Viajes Zvezda","vertical":"Turismo","phase":"Producción",
     "stack":["Next.js 15","React","TypeScript","Tailwind"],
     "desc":"Rediseño full-stack (russia.com.mx): 6 unidades de negocio, ruteo hash, CTAs a WhatsApp.",
     "ia":"IA: scaffold de 74 archivos y sistema visual asistido.",
     "hours":12, "accel":0.60},
    {"id":"patrimonio","name":"PatrimonioOS","vertical":"Wealth-tech","phase":"Plan",
     "stack":["React Native","Expo","Supabase"],
     "desc":"SaaS de gestión patrimonial multi-familia con escaneo documental y motor de reglas por estado.",
     "ia":"IA: extracción documental y motor de obligaciones recurrentes.",
     "hours":8, "accel":0.50},
    {"id":"orey","name":"Orey AI Assistant","vertical":"Capa transversal","phase":"Desarrollo",
     "stack":["GitHub","Knowledge Graph","Python","n8n"],
     "desc":"Copiloto personal: grafo de conocimiento con gobernanza, ADRs y pipeline de promoción.",
     "ia":"IA: orquesta todos los ventures. Se replica dentro de cada uno.",
     "hours":14, "accel":0.40},
]
projects = pd.DataFrame(PROJECTS)
PHASE_CLASS = {"Producción":"p-prod","Desarrollo":"p-dev","Plan":"p-plan"}
PIPELINE = ["Research","Arquitectura","Spec / Schema","Generación asistida","Corrección / Validación","Deploy"]
IA_WEIGHT = [55, 70, 80, 95, 65, 60]


def style_fig(fig, height=380, legend=False):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=PLOT_FONT, height=height, margin=dict(l=10, r=10, t=30, b=10),
        showlegend=legend,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor=PANEL, font_size=12, bordercolor=LINE),
    )
    fig.update_xaxes(gridcolor=LINE, zeroline=False)
    fig.update_yaxes(gridcolor=LINE, zeroline=False)
    return fig


# --- SIDEBAR: modelo de impacto ajustable ---
with st.sidebar:
    st.markdown('<div class="side-brand">◆ AI Advisor OS</div>', unsafe_allow_html=True)
    st.markdown('<div class="side-sub">Reyes Betancourt · IA aplicada a negocios</div>', unsafe_allow_html=True)
    st.divider()
    st.caption("MODELO DE IMPACTO (tus supuestos)")
    rate = st.slider("Tu tarifa de asesoría (MXN/hora)", 200, 1500, 450, 50)
    global_accel = st.slider("Cuánto acelera la IA tu trabajo (×)", 1.0, 4.0, 2.2, 0.1,
                             help="Factor de aceleración base; cada proyecto lo ajusta según su etapa.")
    weeks = st.slider("Semanas del horizonte", 4, 52, 24, 4)
    st.divider()
    st.caption("FILTRO")
    sectors = sorted(projects["vertical"].unique())
    sel = st.multiselect("Vertical", sectors, default=sectors)
    st.divider()
    st.caption("Datos: operación real · supuestos declarados, no simulados de mercado.")

dfp = projects[projects["vertical"].isin(sel)].copy() if sel else projects.copy()
if dfp.empty:
    dfp = projects.copy()

dfp["accel_x"] = 1 + (global_accel - 1) * (dfp["accel"] / dfp["accel"].max())
dfp["horas_liberadas_sem"] = (dfp["hours"] * (1 - 1/dfp["accel_x"])).round(1)
horas_sem = dfp["horas_liberadas_sem"].sum()
horas_horizonte = horas_sem * weeks
valor_horizonte = horas_horizonte * rate

# --- HERO ---
st.markdown('<div class="rise d1"><div class="eyebrow">Especialidad en IA · Visualización de Datos</div></div>', unsafe_allow_html=True)
st.markdown('<div class="rise d2"><div class="hero-title">La IA como <span class="hl">sistema operativo</span><br>del asesor de negocios</div></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="rise d3"><div class="hero-sub">No asesoro desde la teoría: <b>construyo sistemas completos</b>. '
    'La IA es la capa que me lleva de la estrategia a la entrega técnica de punta a punta —arquitectura, código y operación— '
    'sin un equipo grande. En el centro está <b>Orey AI</b>: un copiloto que orquesta seis ventures y se replica dentro de cada uno.</div></div>',
    unsafe_allow_html=True)
st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
kpis = [
    (k1, f"{len(dfp)}", "ventures activos", "6 verticales de negocio"),
    (k2, f"{horas_sem:,.0f} h", "liberadas / semana", "según tus supuestos"),
    (k3, f"${valor_horizonte/1e6:,.2f} M", f"valor en {weeks} sem", "capacidad estratégica recuperada"),
    (k4, "1", "copiloto transversal", "Orey, replicable en cada venture"),
]
for col, v, l, f in kpis:
    col.markdown(
        f'<div class="rise d4"><div class="kpi"><div class="kpi-label">{l}</div>'
        f'<div class="kpi-value">{v}</div><div class="kpi-foot">{f}</div></div></div>',
        unsafe_allow_html=True)

st.markdown(
    f'<div class="rise d5"><div class="insight" style="margin-top:1rem">Con tus supuestos actuales '
    f'(<b>{global_accel:.1f}×</b> de aceleración, <b>${rate:,} MXN/h</b>), la IA te libera <b>{horas_sem:,.0f} h/semana</b>. '
    f'En {weeks} semanas son <b>{horas_horizonte:,.0f} horas</b> que dejas de gastar en trabajo operativo y reinviertes en estrategia — '
    f'el retorno real de la IA no es el software, es el <b>tiempo del experto</b>. Ajusta los deslizadores en el panel para ver cómo cambia.</div></div>',
    unsafe_allow_html=True)

# --- 01 EL MÉTODO ---
st.markdown('<div class="rule-soft"></div>', unsafe_allow_html=True)
st.markdown('<div class="eyebrow">01 · El método</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-h">Mi pipeline con IA</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-p">Cada proyecto recorre las mismas seis etapas. La IA no reemplaza el criterio: '
            'acelera cada tramo y me deja validar más rápido. El pico está en la generación asistida.</div>', unsafe_allow_html=True)
st.write("")

fig_pipe = go.Figure()
fig_pipe.add_trace(go.Scatter(
    x=PIPELINE, y=IA_WEIGHT, mode="lines+markers+text",
    text=[f"{w}%" for w in IA_WEIGHT], textposition="top center",
    textfont=dict(color=CYAN, size=11),
    line=dict(color=CYAN, width=3, shape="spline"),
    marker=dict(size=13, color=INK, line=dict(color=CYAN, width=3)),
    fill="tozeroy", fillcolor="rgba(56,225,214,0.10)",
    hovertemplate="<b>%{x}</b><br>Intervención IA: %{y}%<extra></extra>"))
fig_pipe.update_yaxes(range=[0, 108], title="Intervención de IA (%)")
st.plotly_chart(style_fig(fig_pipe, 330), use_container_width=True)

# --- 02 PORTAFOLIO ---
st.markdown('<div class="rule-soft"></div>', unsafe_allow_html=True)
st.markdown('<div class="eyebrow">02 · Dónde lo aplico</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-h">Portafolio de ventures</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-p">Seis proyectos, una misma arquitectura de IA por debajo. '
            'Algunos en producción, otros en plan: el método es el mismo. Pasa el cursor sobre cada tarjeta.</div>', unsafe_allow_html=True)
st.write("")

cols = st.columns(3)
for i, row in dfp.reset_index(drop=True).iterrows():
    with cols[i % 3]:
        chips = "".join(f'<span class="chip">{s}</span>' for s in row["stack"])
        st.markdown(
            f'<div class="card"><div class="vert">{row["vertical"]}</div>'
            f'<div class="name">{row["name"]}</div>'
            f'<div class="desc">{row["desc"]}</div>'
            f'<div>{chips}</div>'
            f'<div class="ia">{row["ia"]}</div>'
            f'<div class="phase {PHASE_CLASS[row["phase"]]}">● {row["phase"]}</div></div>',
            unsafe_allow_html=True)
        st.write("")

# --- 03 OPERACIÓN EN DATOS ---
st.markdown('<div class="rule-soft"></div>', unsafe_allow_html=True)
st.markdown('<div class="eyebrow">03 · La operación en datos</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-h">Mi portafolio, en gráficas</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-p">Datos reales del portafolio. La cuarta gráfica usa tu modelo de impacto: '
            'se recalcula al mover los deslizadores del panel.</div>', unsafe_allow_html=True)
st.write("")

c1, c2 = st.columns(2)
with c1:
    st.markdown(f'<div style="color:{TEXT};font-weight:600;margin-bottom:.3rem">Ventures por vertical</div>', unsafe_allow_html=True)
    vc = dfp["vertical"].value_counts().reset_index(); vc.columns = ["vertical","n"]
    f1 = px.bar(vc, x="n", y="vertical", orientation="h", color="vertical", color_discrete_sequence=PLOT_SEQ)
    f1.update_layout(xaxis=dict(dtick=1, title=""), yaxis=dict(title=""))
    st.plotly_chart(style_fig(f1, 280), use_container_width=True)
with c2:
    st.markdown(f'<div style="color:{TEXT};font-weight:600;margin-bottom:.3rem">Fase de madurez</div>', unsafe_allow_html=True)
    ph = dfp["phase"].value_counts().reset_index(); ph.columns = ["phase","n"]
    cmap = {"Producción":GREEN,"Desarrollo":BLUE,"Plan":AMBER}
    f2 = px.pie(ph, values="n", names="phase", hole=0.62, color="phase", color_discrete_map=cmap)
    f2.update_traces(textposition="inside", textinfo="label+value", insidetextorientation="horizontal")
    st.plotly_chart(style_fig(f2, 280), use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    st.markdown(f'<div style="color:{TEXT};font-weight:600;margin:.4rem 0 .3rem">Stack tecnológico recurrente</div>', unsafe_allow_html=True)
    stack_flat = [s for lst in dfp["stack"] for s in lst]
    sc = pd.Series(stack_flat).value_counts().reset_index(); sc.columns = ["tech","n"]
    f3 = px.bar(sc, x="tech", y="n", color="n", color_continuous_scale=[LINE, CYAN])
    f3.update_layout(coloraxis_showscale=False, xaxis=dict(title=""), yaxis=dict(title="proyectos", dtick=1))
    st.plotly_chart(style_fig(f3, 300), use_container_width=True)
with c4:
    st.markdown(f'<div style="color:{TEXT};font-weight:600;margin:.4rem 0 .3rem">Horas liberadas por venture / semana <span style="color:{MUTED};font-weight:400">(tu modelo)</span></div>', unsafe_allow_html=True)
    hb = dfp.sort_values("horas_liberadas_sem")
    f4 = go.Figure(go.Bar(
        x=hb["horas_liberadas_sem"], y=hb["name"], orientation="h",
        marker=dict(color=hb["horas_liberadas_sem"], colorscale=[[0,BLUE],[1,CYAN]], showscale=False),
        text=[f"{v:.1f} h" for v in hb["horas_liberadas_sem"]], textposition="outside",
        textfont=dict(color=TEXT)))
    f4.update_layout(xaxis=dict(title="", range=[0, hb["horas_liberadas_sem"].max()*1.25]), yaxis=dict(title=""))
    st.plotly_chart(style_fig(f4, 300), use_container_width=True)

# --- 04 EL SISTEMA OREY ---
st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
st.markdown('<div class="eyebrow">04 · La tesis · sección estrella</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-h">Orey AI: un copiloto con disciplina de conocimiento</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-p">Orey no es un chatbot: es un grafo de conocimiento gobernado. '
            'Los aprendizajes no se vierten, se <b>promueven</b> por un pipeline auditable. '
            'Eso convierte cada venture en un sistema que aprende.</div>', unsafe_allow_html=True)
st.write("")

st.markdown(f"""
<div class="orey-band">
<p style="color:{TEXT};font-size:.97rem;line-height:1.6;margin:0 0 .5rem">
<b style="color:{CYAN}">Orey</b> es mi mano derecha: un grafo de conocimiento con capa de gobernanza,
ADRs y un pipeline que promueve aprendizajes crudos a patrones y capabilities reutilizables entre dominios.
Desde ahí orquesto los seis proyectos — y el plan es <b style="color:{TEXT}">incorporar un asistente como Orey dentro de cada venture</b>,
para que cada negocio deje de ser un producto y pase a ser un sistema que aprende y se opera con IA.
</p>
</div>
""", unsafe_allow_html=True)
st.write("")

st.markdown(f'<div style="color:{TEXT};font-weight:600;margin:.3rem 0 .2rem">El pipeline de promoción del conocimiento</div>', unsafe_allow_html=True)
st.markdown(f'<div style="color:{MUTED};font-size:.86rem;margin-bottom:.4rem">Un aprendizaje solo entra al núcleo canónico si pasa el gate. Nada se vierte.</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="flow-row">
  <span class="stage s0">learning · raw</span><span class="arrow">→</span>
  <span class="stage s1">candidate</span><span class="arrow">→</span>
  <span class="stage s2">gate</span><span class="arrow">→</span>
  <span class="stage s3">pattern</span><span class="arrow">→</span>
  <span class="stage s4">capability</span>
</div>
""", unsafe_allow_html=True)

st.write("")
gcol1, gcol2 = st.columns([1, 1])
with gcol1:
    st.markdown(f'<div style="color:{TEXT};font-weight:600;margin-bottom:.3rem">El gate: 8 criterios binarios</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color:{MUTED};font-size:.84rem;margin-bottom:.5rem">Deben cumplirse <b style="color:{TEXT}">todos</b>. Si uno falla, no hay promoción.</div>', unsafe_allow_html=True)
    criterios = ["Fuente clara","Utilidad más allá del caso","Recurrencia ≥ 2 contextos","Interfaz definible",
                 "No duplica","Respeta el DNA","Tiene owner","Justificación explícita"]
    chips = "".join(f'<span class="gate"><b>{i+1:02d}</b> · {c}</span>' for i, c in enumerate(criterios))
    st.markdown(f'<div>{chips}</div>', unsafe_allow_html=True)
with gcol2:
    st.markdown(f'<div style="color:{TEXT};font-weight:600;margin-bottom:.3rem">Un caso real, trazado</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="insight" style="margin-top:.2rem">El patrón <b>"CTA → WhatsApp sin precio público"</b> '
        f'nace como <span style="color:{VIOLET}">learning</span> en <b>Zvezda</b>. Cuando <b>BarberBROTHER</b> necesita lo mismo, '
        f'hay ≥2 contextos: se propone, pasa el <span style="color:{BLUE}">gate</span> (fuente clara, recurrente, no duplica, '
        f'respeta DNA, tiene owner, justificado) y se promueve a <span style="color:{GREEN}">pattern</span>. '
        f'Si luego se le define interfaz, se generaliza a <span style="color:{CYAN}">capability</span> que otros ventures consumen.</div>',
        unsafe_allow_html=True)

st.write("")
st.markdown(f'<div style="color:{TEXT};font-weight:600;margin:.5rem 0 .2rem">El grafo vivo: Orey y sus ventures</div>', unsafe_allow_html=True)
st.markdown(f'<div style="color:{MUTED};font-size:.86rem;margin-bottom:.3rem">'
            f'Arrastra los nodos. <span style="color:{BLUE}">CONSUMES</span> = el venture usa una capability de Orey; '
            f'<span style="color:{VIOLET}">SOURCED_FROM</span> = el venture devuelve un aprendizaje al núcleo. El ciclo es bidireccional.</div>',
            unsafe_allow_html=True)

nodes = [
    {"id":"orey","label":"Orey AI","type":"core","desc":"Núcleo: grafo de conocimiento gobernado que orquesta todo."},
    {"id":"cap-onboard","label":"onboarding multi-tenant","type":"capability","desc":"Capability: montar el alta de un vertical nuevo."},
    {"id":"cap-schema","label":"schema Supabase","type":"capability","desc":"Capability: diseño y validación de esquema de datos."},
    {"id":"cap-cta","label":"cta-whatsapp","type":"pattern","desc":"Pattern: CTA que enruta a WhatsApp sin precio público."},
    {"id":"uege","label":"UEGE","type":"project","desc":"Clínica de gastroenterología."},
    {"id":"dentwork","label":"Dentwork","type":"project","desc":"Gestión de espacio dental."},
    {"id":"barber","label":"BarberBROTHER","type":"project","desc":"Sistema para barbería."},
    {"id":"zvezda","label":"Viajes Zvezda","type":"project","desc":"Agencia de viajes, corredor Rusia."},
    {"id":"patrimonio","label":"PatrimonioOS","type":"project","desc":"Gestión patrimonial multi-familia."},
    {"id":"l-cta","label":"learning: CTA","type":"learning","desc":"Aprendizaje capturado en Zvezda."},
    {"id":"l-agenda","label":"learning: agenda","type":"learning","desc":"Aprendizaje capturado en UEGE."},
]
links = [
    {"source":"uege","target":"cap-schema","rel":"CONSUMES"},
    {"source":"dentwork","target":"cap-schema","rel":"CONSUMES"},
    {"source":"barber","target":"cap-onboard","rel":"CONSUMES"},
    {"source":"barber","target":"cap-cta","rel":"CONSUMES"},
    {"source":"zvezda","target":"cap-cta","rel":"CONSUMES"},
    {"source":"patrimonio","target":"cap-schema","rel":"CONSUMES"},
    {"source":"cap-onboard","target":"orey","rel":"CONSUMES"},
    {"source":"cap-schema","target":"orey","rel":"CONSUMES"},
    {"source":"cap-cta","target":"orey","rel":"CONSUMES"},
    {"source":"l-cta","target":"zvezda","rel":"SOURCED_FROM"},
    {"source":"l-agenda","target":"uege","rel":"SOURCED_FROM"},
    {"source":"cap-cta","target":"l-cta","rel":"SOURCED_FROM"},
]
orey_graph(nodes, links, height=560)

# --- FOOTER ---
st.markdown('<div class="rule-soft"></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="foot">Reyes Betancourt García · Consultoría de estrategia y transformación con IA · '
    'Especialidad en IA y Ciencia de Datos · Construido con Streamlit + Plotly + D3</div>',
    unsafe_allow_html=True)
