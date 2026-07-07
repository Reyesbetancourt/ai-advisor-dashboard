"""
La IA como Sistema Operativo del Asesor de Negocios
Tablero-portafolio: método de trabajo con IA aplicado a ventures reales.
Reyes Betancourt García — Especialidad en IA y Ciencia de Datos.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="IA · Sistema Operativo del Asesor",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------------------------
# PALETA Y ESTILO
#   Fondo azul-acero profundo (no negro), acento cian-eléctrico = "OS".
#   Display: Space Grotesk · Datos: Inter · Mono: JetBrains Mono
# ----------------------------------------------------------------------
INK      = "#0B1220"   # fondo profundo
PANEL    = "#111C2E"   # paneles
LINE     = "#1F2E44"   # divisores
TEXT     = "#E6EDF7"   # texto principal
MUTED    = "#7C8CA6"   # texto secundario
CYAN     = "#38E1D6"   # acento OS
BLUE     = "#4C7DFF"   # acento secundario
AMBER    = "#F5B455"   # alerta / fase plan

PLOT_SEQ = [CYAN, BLUE, AMBER, "#9B7DFF", "#5FD3A0", "#FF7D9C"]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

.stApp {{ background: {INK}; color: {TEXT}; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 2.2rem; max-width: 1180px; }}

h1,h2,h3 {{ font-family: 'Space Grotesk', sans-serif !important; color: {TEXT}; letter-spacing:-0.5px; }}
p, div, span, li {{ font-family: 'Inter', sans-serif; }}

.eyebrow {{
  font-family:'JetBrains Mono',monospace; font-size:0.72rem; letter-spacing:3px;
  text-transform:uppercase; color:{CYAN}; margin-bottom:0.4rem;
}}
.hero-title {{ font-size:2.9rem; line-height:1.05; font-weight:700; margin:0.1rem 0 0.6rem; }}
.hero-title .hl {{ color:{CYAN}; }}
.hero-sub {{ font-size:1.05rem; color:{MUTED}; max-width:720px; line-height:1.55; }}

.rule {{ height:1px; background:{LINE}; border:0; margin:2.2rem 0 1.6rem; }}

.card {{
  background:{PANEL}; border:1px solid {LINE}; border-radius:14px;
  padding:1.1rem 1.2rem; height:100%;
}}
.card .vert {{ font-family:'JetBrains Mono',monospace; font-size:0.68rem;
  letter-spacing:2px; text-transform:uppercase; color:{CYAN}; }}
.card .name {{ font-family:'Space Grotesk',sans-serif; font-size:1.15rem;
  font-weight:600; margin:0.25rem 0 0.35rem; }}
.card .desc {{ font-size:0.86rem; color:{MUTED}; line-height:1.5; min-height:66px; }}
.card .stack {{ margin-top:0.7rem; }}
.chip {{
  display:inline-block; font-family:'JetBrains Mono',monospace; font-size:0.66rem;
  color:{TEXT}; background:{INK}; border:1px solid {LINE}; border-radius:20px;
  padding:2px 9px; margin:2px 3px 0 0;
}}
.phase {{ font-family:'JetBrains Mono',monospace; font-size:0.66rem;
  padding:2px 8px; border-radius:20px; margin-top:0.6rem; display:inline-block; }}
.p-prod {{ color:{CYAN}; border:1px solid {CYAN}; }}
.p-dev  {{ color:{BLUE}; border:1px solid {BLUE}; }}
.p-plan {{ color:{AMBER}; border:1px solid {AMBER}; }}

.orey-band {{
  background:linear-gradient(135deg, rgba(56,225,214,0.08), rgba(76,125,255,0.06));
  border:1px solid {LINE}; border-left:3px solid {CYAN};
  border-radius:12px; padding:1.2rem 1.4rem;
}}
.section-h {{ font-size:1.5rem; font-weight:700; margin:0.2rem 0 0.2rem; }}
.section-p {{ color:{MUTED}; font-size:0.92rem; max-width:760px; }}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# DATOS (tu operación real — no simulados, no de mercado)
# ----------------------------------------------------------------------
projects = pd.DataFrame([
    {"name":"UEGE / Gastro",   "vertical":"Salud",     "phase":"Desarrollo",
     "stack":["Supabase","Lovable","React","TypeScript"],
     "desc":"Sistema operativo para clínica de gastroenterología: schema, landing pública y app operativa.",
     "ia_role":"Generación de schema y corrección de prompts (20+ errores → v3)."},
    {"name":"Dentwork",        "vertical":"Salud",     "phase":"Plan",
     "stack":["Supabase","Lovable","React"],
     "desc":"Plataforma operativa para gestión de espacio dental. Bloqueada por decisión de arquitectura.",
     "ia_role":"Diseño de arquitectura y ADRs asistidos."},
    {"name":"BarberBROTHER",   "vertical":"Retail/Servicios","phase":"Plan",
     "stack":["Supabase","Lovable","React"],
     "desc":"Sistema de operación para barbería. En auditoría de diseño previa a implementación.",
     "ia_role":"Auditoría de diseño operativo y definición de entidades."},
    {"name":"Viajes Zvezda",   "vertical":"Turismo",   "phase":"Producción",
     "stack":["Next.js 15","React","TypeScript","Tailwind"],
     "desc":"Rediseño full-stack del sitio (russia.com.mx): 6 unidades de negocio, ruteo hash, CTAs a WhatsApp.",
     "ia_role":"Scaffold de 74 archivos y sistema visual asistido."},
    {"name":"PatrimonioOS",    "vertical":"Wealth-tech","phase":"Plan",
     "stack":["React Native","Expo","Supabase"],
     "desc":"SaaS de gestión patrimonial multi-familia con escaneo documental y motor de reglas por estado.",
     "ia_role":"Extracción documental y motor de obligaciones recurrentes con IA."},
    {"name":"Orey AI Assistant","vertical":"Capa transversal","phase":"Desarrollo",
     "stack":["GitHub","Knowledge Graph","Python","n8n"],
     "desc":"Copiloto personal: grafo de conocimiento con gobernanza, ADRs y pipeline de promoción de aprendizajes.",
     "ia_role":"Orquesta todos los proyectos. Se replica dentro de cada venture."},
])

PHASE_CLASS = {"Producción":"p-prod","Desarrollo":"p-dev","Plan":"p-plan"}

# ----------------------------------------------------------------------
# HERO
# ----------------------------------------------------------------------
st.markdown('<div class="eyebrow">Especialidad en IA · Visualización de Datos</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-title">La IA como <span class="hl">sistema operativo</span><br>del asesor de negocios</div>',
    unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">No asesoro desde la teoría: construyo sistemas completos. '
    'La IA es la capa que me permite pasar de la estrategia a la entrega técnica '
    'de punta a punta —arquitectura, código y operación— sin un equipo grande. '
    'Este tablero muestra <b>cómo lo hago</b> y <b>dónde lo aplico</b>.</div>',
    unsafe_allow_html=True)

# métricas simples y verdaderas
st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
m1,m2,m3,m4 = st.columns(4)
for col,(v,l) in zip([m1,m2,m3,m4],[
    (str(len(projects)),"ventures activos"),
    (projects["vertical"].nunique(),"verticales de negocio"),
    ("6","etapas del pipeline con IA"),
    ("1","copiloto transversal (Orey)"),
]):
    col.markdown(
        f'<div style="font-family:Space Grotesk;font-size:2.1rem;font-weight:700;color:{CYAN}">{v}</div>'
        f'<div style="color:{MUTED};font-size:0.8rem;text-transform:uppercase;letter-spacing:1px">{l}</div>',
        unsafe_allow_html=True)

# ----------------------------------------------------------------------
# SECCIÓN: EL MÉTODO (PIPELINE)
# ----------------------------------------------------------------------
st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
st.markdown('<div class="eyebrow">01 · El método</div>', unsafe_allow_html=True)
st.markdown('<div class="section-h">Mi pipeline con IA</div>', unsafe_allow_html=True)
st.markdown('<div class="section-p">Cada proyecto recorre las mismas seis etapas. '
            'La IA no reemplaza el criterio: acelera cada tramo y me deja validar más rápido.</div>',
            unsafe_allow_html=True)
st.write("")

pipeline = ["Research","Arquitectura","Spec / Schema","Generación asistida","Corrección / Validación","Deploy"]
ia_weight = [55, 70, 80, 95, 65, 60]   # % de intervención de IA por etapa (juicio propio)

fig_pipe = go.Figure()
fig_pipe.add_trace(go.Scatter(
    x=pipeline, y=ia_weight, mode="lines+markers",
    line=dict(color=CYAN, width=3, shape="spline"),
    marker=dict(size=13, color=INK, line=dict(color=CYAN, width=3)),
    fill="tozeroy", fillcolor="rgba(56,225,214,0.10)",
    hovertemplate="<b>%{x}</b><br>Intervención IA: %{y}%<extra></extra>",
))
fig_pipe.update_layout(
    height=320, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color=MUTED), margin=dict(l=10,r=10,t=20,b=10),
    yaxis=dict(title="Intervención de IA (%)", range=[0,100], gridcolor=LINE, zeroline=False),
    xaxis=dict(gridcolor="rgba(0,0,0,0)"),
)
st.plotly_chart(fig_pipe, use_container_width=True)

# ----------------------------------------------------------------------
# SECCIÓN: PORTAFOLIO
# ----------------------------------------------------------------------
st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
st.markdown('<div class="eyebrow">02 · Dónde lo aplico</div>', unsafe_allow_html=True)
st.markdown('<div class="section-h">Portafolio de ventures</div>', unsafe_allow_html=True)
st.markdown('<div class="section-p">Seis proyectos, una misma arquitectura de IA por debajo. '
            'Algunos en producción, otros en plan: el método es el mismo.</div>',
            unsafe_allow_html=True)
st.write("")

cols = st.columns(3)
for i, row in projects.iterrows():
    with cols[i % 3]:
        chips = "".join(f'<span class="chip">{s}</span>' for s in row["stack"])
        pcls = PHASE_CLASS[row["phase"]]
        st.markdown(f"""
        <div class="card">
          <div class="vert">{row['vertical']}</div>
          <div class="name">{row['name']}</div>
          <div class="desc">{row['desc']}</div>
          <div class="stack">{chips}</div>
          <div class="phase {pcls}">● {row['phase']}</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")

# ----------------------------------------------------------------------
# SECCIÓN: VISUALIZACIONES
# ----------------------------------------------------------------------
st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
st.markdown('<div class="eyebrow">03 · La operación en datos</div>', unsafe_allow_html=True)
st.markdown('<div class="section-h">Mi portafolio, en gráficas</div>', unsafe_allow_html=True)
st.write("")

c1, c2 = st.columns(2)

# Proyectos por vertical
with c1:
    st.markdown(f'<div style="color:{TEXT};font-weight:600;margin-bottom:.3rem">Ventures por vertical</div>',
                unsafe_allow_html=True)
    vc = projects["vertical"].value_counts().reset_index()
    vc.columns = ["vertical","n"]
    fig1 = px.bar(vc, x="n", y="vertical", orientation="h",
                  color="vertical", color_discrete_sequence=PLOT_SEQ)
    fig1.update_layout(
        height=280, showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter",color=MUTED),
        margin=dict(l=10,r=10,t=10,b=10),
        xaxis=dict(gridcolor=LINE, dtick=1, title=""), yaxis=dict(title=""))
    st.plotly_chart(fig1, use_container_width=True)

# Fase de madurez
with c2:
    st.markdown(f'<div style="color:{TEXT};font-weight:600;margin-bottom:.3rem">Fase de madurez</div>',
                unsafe_allow_html=True)
    ph = projects["phase"].value_counts().reset_index()
    ph.columns = ["phase","n"]
    cmap = {"Producción":CYAN,"Desarrollo":BLUE,"Plan":AMBER}
    fig2 = px.pie(ph, values="n", names="phase", hole=0.62,
                  color="phase", color_discrete_map=cmap)
    fig2.update_traces(textposition="outside", textinfo="label+value")
    fig2.update_layout(
        height=280, showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter",color=MUTED), margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig2, use_container_width=True)

# Stack recurrente
st.markdown(f'<div style="color:{TEXT};font-weight:600;margin:.6rem 0 .3rem">Stack tecnológico recurrente</div>',
            unsafe_allow_html=True)
stack_flat = [s for lst in projects["stack"] for s in lst]
sc = pd.Series(stack_flat).value_counts().reset_index()
sc.columns = ["tech","n"]
fig3 = px.bar(sc, x="tech", y="n", color="n", color_continuous_scale=["#1F2E44",CYAN])
fig3.update_layout(
    height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter",color=MUTED), margin=dict(l=10,r=10,t=10,b=10),
    coloraxis_showscale=False, xaxis=dict(title=""), yaxis=dict(title="proyectos", gridcolor=LINE, dtick=1))
st.plotly_chart(fig3, use_container_width=True)

# ----------------------------------------------------------------------
# SECCIÓN: OREY COMO CAPA TRANSVERSAL
# ----------------------------------------------------------------------
st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
st.markdown('<div class="eyebrow">04 · La tesis</div>', unsafe_allow_html=True)
st.markdown('<div class="section-h">Orey AI Assistant: un copiloto, replicado en cada venture</div>',
            unsafe_allow_html=True)
st.write("")

st.markdown(f"""
<div class="orey-band">
<p style="color:{TEXT};font-size:0.98rem;line-height:1.6;margin:0 0 0.6rem">
<b style="color:{CYAN}">Orey</b> es mi mano derecha: un grafo de conocimiento con capa de gobernanza,
ADRs y un pipeline que promueve aprendizajes crudos a patrones reutilizables entre dominios.
Desde ahí orquesto los seis proyectos.
</p>
<p style="color:{MUTED};font-size:0.9rem;line-height:1.6;margin:0">
El siguiente paso es <b style="color:{TEXT}">incorporar un asistente como Orey dentro de cada venture</b>
—UEGE, Dentwork, BarberBROTHER, Viajes Zvezda, PatrimonioOS— para multiplicar su valor:
cada negocio deja de ser un producto y pasa a ser un sistema que aprende y se opera con IA.
</p>
</div>
""", unsafe_allow_html=True)

# Diagrama hub-and-spoke Orey → ventures
labels = ["Orey AI"] + projects[projects["name"]!="Orey AI Assistant"]["name"].tolist()
src, tgt, val = [], [], []
for i in range(1, len(labels)):
    src.append(0); tgt.append(i); val.append(1)

fig_hub = go.Figure(go.Sankey(
    arrangement="snap",
    node=dict(
        pad=22, thickness=16, line=dict(color=LINE, width=1),
        label=labels,
        color=[CYAN]+[BLUE]*(len(labels)-1)),
    link=dict(source=src, target=tgt, value=val,
              color="rgba(56,225,214,0.18)")
))
fig_hub.update_layout(
    height=340, paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color=TEXT, size=12),
    margin=dict(l=10,r=10,t=20,b=10))
st.markdown(f'<div style="color:{TEXT};font-weight:600;margin:.8rem 0 .2rem">Orey como capa que alimenta cada venture</div>',
            unsafe_allow_html=True)
st.plotly_chart(fig_hub, use_container_width=True)

# ----------------------------------------------------------------------
# FOOTER
# ----------------------------------------------------------------------
st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
st.markdown(
    f'<div style="color:{MUTED};font-size:0.8rem;font-family:JetBrains Mono,monospace">'
    'Reyes Betancourt García · Consultoría de estrategia y transformación con IA · '
    'Especialidad en IA y Ciencia de Datos</div>',
    unsafe_allow_html=True)
