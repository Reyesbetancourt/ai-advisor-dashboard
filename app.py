"""
========================================================================
  IA como Sistema Operativo del Asesor de Negocios
  Dashboard de Visualización de Datos — Proyecto Final
  Autor: Reyes Betancourt García
  Especialidad: IA aplicada a Negocios
========================================================================

Cuenta una historia con datos: cómo la Inteligencia Artificial está
transformando el trabajo de un asesor en estrategia y transformación de
negocios, medido a través de 6 sistemas reales construidos con IA.

Ejecutar:  streamlit run app.py
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# ----------------------------------------------------------------------
# Configuración de página
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="IA · Sistema Operativo del Asesor",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# Paleta de marca — "Holographic Slate"
# ----------------------------------------------------------------------
INK        = "#0A0B10"   # fondo profundo
SLATE      = "#12131C"   # tarjetas
VIOLET     = "#7C6CFF"   # acento primario (IA)
CYAN       = "#38E1C6"   # acento secundario (crecimiento)
GOLD       = "#E8C37E"   # champagne (destacados)
CORAL      = "#FF7A6B"   # alertas / esfuerzo
TEXT       = "#E8E9F3"
MUTED      = "#8A8DA3"

SECTOR_COLORS = {
    "Salud": VIOLET,
    "Fintech": CYAN,
    "Real Estate": GOLD,
    "Servicios": CORAL,
}

PLOT_FONT = dict(family="Inter, system-ui, sans-serif", color=TEXT, size=13)


# ----------------------------------------------------------------------
# CSS — identidad editorial-tech
# ----------------------------------------------------------------------
def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,900&family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"], .stApp { font-family: 'Inter', sans-serif; }
        .stApp { background:
            radial-gradient(1200px 600px at 80% -10%, rgba(124,108,255,0.12), transparent 60%),
            radial-gradient(900px 500px at -10% 10%, rgba(56,225,198,0.08), transparent 55%),
            #0A0B10; }

        /* ---- Hero ---- */
        .hero-eyebrow {
            font-size: 0.78rem; letter-spacing: 0.32em; text-transform: uppercase;
            color: #38E1C6; font-weight: 600; margin-bottom: 0.6rem;
        }
        .hero-title {
            font-family: 'Fraunces', serif; font-weight: 900; line-height: 1.02;
            font-size: 3.4rem; color: #E8E9F3; margin: 0 0 0.8rem 0;
            letter-spacing: -0.02em;
        }
        .hero-title .accent {
            background: linear-gradient(100deg, #7C6CFF, #38E1C6);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .hero-sub {
            font-size: 1.06rem; color: #B7B9CC; max-width: 720px; line-height: 1.55;
        }
        .hero-rule {
            height: 1px; margin: 1.6rem 0 0.4rem 0;
            background: linear-gradient(90deg, #7C6CFF, transparent);
        }

        /* ---- Section headers ---- */
        .sec-eyebrow {
            font-size: 0.72rem; letter-spacing: 0.28em; text-transform: uppercase;
            color: #8A8DA3; font-weight: 600; margin: 2.2rem 0 0.2rem 0;
        }
        .sec-title {
            font-family: 'Fraunces', serif; font-weight: 600; font-size: 1.7rem;
            color: #E8E9F3; margin: 0 0 0.3rem 0; letter-spacing: -0.01em;
        }
        .sec-note { color: #8A8DA3; font-size: 0.94rem; margin-bottom: 0.8rem; }

        /* ---- KPI cards ---- */
        .kpi {
            background: linear-gradient(160deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
            border: 1px solid rgba(255,255,255,0.07); border-radius: 16px;
            padding: 1.15rem 1.25rem; height: 100%;
        }
        .kpi-label { font-size: 0.74rem; letter-spacing: 0.14em; text-transform: uppercase;
            color: #8A8DA3; font-weight: 600; }
        .kpi-value { font-family: 'Fraunces', serif; font-weight: 900; font-size: 2.15rem;
            color: #E8E9F3; line-height: 1.1; margin: 0.25rem 0 0.1rem 0; }
        .kpi-delta { font-size: 0.86rem; font-weight: 600; }
        .kpi-delta.up { color: #38E1C6; }
        .kpi-delta.down { color: #FF7A6B; }
        .kpi-foot { font-size: 0.78rem; color: #6E7188; margin-top: 0.15rem; }

        /* ---- Insight callout ---- */
        .insight {
            border-left: 3px solid #7C6CFF; background: rgba(124,108,255,0.06);
            border-radius: 0 12px 12px 0; padding: 0.9rem 1.1rem; margin: 0.4rem 0 1.2rem 0;
            color: #D3D5E6; font-size: 0.95rem; line-height: 1.55;
        }
        .insight b { color: #E8C37E; }

        /* Sidebar */
        section[data-testid="stSidebar"] { background: #0D0E15; border-right: 1px solid rgba(255,255,255,0.06); }
        .side-brand { font-family:'Fraunces',serif; font-weight:900; font-size:1.25rem; color:#E8E9F3; }
        .side-sub { color:#8A8DA3; font-size:0.8rem; margin-bottom:0.5rem; }

        /* Footer */
        .foot { color:#6E7188; font-size:0.82rem; text-align:center; margin-top:2rem;
            padding-top:1rem; border-top:1px solid rgba(255,255,255,0.06); }

        #MainMenu, footer, header { visibility: hidden; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------
# Carga y limpieza de datos (cacheada)
# ----------------------------------------------------------------------
# --- Catálogo maestro de las 6 verticales de negocio con IA ---
_VERTICALES = [
    {"id": "UEGE",       "nombre": "Clínica de Gastroenterología", "sector": "Salud",       "ticket_mxn": 2800},
    {"id": "PATRIMONIO", "nombre": "Gestión de Activos Familiares", "sector": "Fintech",     "ticket_mxn": 5200},
    {"id": "BGREAT",     "nombre": "Coworking Dental",              "sector": "Salud",       "ticket_mxn": 3400},
    {"id": "BARBER",     "nombre": "Sistema para Barberías",        "sector": "Servicios",   "ticket_mxn": 380},
    {"id": "RENTAS",     "nombre": "Administración de Rentas",      "sector": "Real Estate", "ticket_mxn": 14500},
    {"id": "CRIPTO",     "nombre": "Trading de Criptomonedas",      "sector": "Fintech",     "ticket_mxn": 1900},
]


@st.cache_data
def load_data():
    """Genera los datasets sintéticos en memoria (semilla fija, reproducible).
    No depende de archivos externos: la app corre con solo app.py + requirements."""
    import numpy as np

    rng = np.random.default_rng(2026)
    meses = pd.date_range("2025-01-01", "2026-06-01", freq="MS")

    # ---- Serie mensual por vertical ----
    filas = []
    for v in _VERTICALES:
        mes_adopcion = rng.integers(3, 9)
        base_horas = rng.uniform(90, 160)
        base_clientes = rng.uniform(40, 220)
        for i, mes in enumerate(meses):
            adoptado = i >= mes_adopcion
            ramp = 1 / (1 + np.exp(-(i - mes_adopcion - 2))) if adoptado else 0.0
            horas = base_horas * (1 - 0.55 * ramp) * rng.uniform(0.95, 1.05)
            clientes = base_clientes * (1 + 0.9 * ramp) * (1 + 0.015 * i) * rng.uniform(0.96, 1.04)
            ingresos = clientes * v["ticket_mxn"] * rng.uniform(0.95, 1.05)
            nps = float(np.clip(58 + 28 * ramp + rng.normal(0, 3), 40, 95))
            pct_auto = float(np.clip(72 * ramp + rng.normal(0, 4), 0, 88))
            horas_ahorradas = max(base_horas - horas, 0)
            filas.append({
                "vertical_id": v["id"], "vertical": v["nombre"], "sector": v["sector"],
                "mes": mes, "adopcion_ia": bool(adoptado),
                "horas_manuales": round(horas, 1), "horas_ahorradas": round(horas_ahorradas, 1),
                "clientes_activos": int(clientes), "ingresos_mxn": round(ingresos, 0),
                "pct_automatizado": round(pct_auto, 1), "nps": round(nps, 1),
                "ticket_mxn": v["ticket_mxn"],
            })
    series = pd.DataFrame(filas)

    # ---- Casos de uso de IA (impacto vs esfuerzo) ----
    _casos = [
        ("UEGE", "Agendado inteligente de estudios", "Operaciones", 8, 3, 42),
        ("UEGE", "Ingesta de documentos clínicos (OCR+LLM)", "Documentación", 9, 6, 55),
        ("UEGE", "Resúmenes de historia clínica", "Clínico", 7, 4, 30),
        ("PATRIMONIO", "Motor de reglas fiscales por estado", "Cumplimiento", 9, 8, 60),
        ("PATRIMONIO", "Clasificación automática de activos", "Datos", 8, 5, 48),
        ("PATRIMONIO", "Alertas de vencimientos y renovaciones", "Riesgo", 7, 3, 25),
        ("BGREAT", "Optimización de ocupación de sillones", "Operaciones", 8, 4, 38),
        ("BGREAT", "Facturación CFDI automatizada", "Finanzas", 9, 5, 52),
        ("BGREAT", "Recordatorios y no-shows", "Retención", 6, 2, 22),
        ("BARBER", "Reservas por WhatsApp con IA", "Ventas", 8, 3, 28),
        ("BARBER", "Predicción de demanda por barbero", "Analítica", 6, 5, 18),
        ("RENTAS", "Screening de inquilinos", "Riesgo", 8, 6, 44),
        ("RENTAS", "Cobranza y conciliación automática", "Finanzas", 9, 5, 58),
        ("RENTAS", "Redacción asistida de contratos", "Legal", 7, 4, 33),
        ("CRIPTO", "Señales cuantitativas asistidas por IA", "Analítica", 9, 9, 40),
        ("CRIPTO", "Gestión de riesgo y stop dinámico", "Riesgo", 8, 7, 35),
        ("CRIPTO", "Cumplimiento LFPIORPI (actividad vulnerable)", "Cumplimiento", 8, 8, 30),
    ]
    casos = pd.DataFrame(_casos, columns=[
        "vertical_id", "caso_uso", "categoria", "impacto", "esfuerzo", "horas_mes_ahorradas"])
    _mapa = {v["id"]: v["nombre"] for v in _VERTICALES}
    casos["vertical"] = casos["vertical_id"].map(_mapa)
    casos["roi_score"] = (casos["impacto"] * casos["horas_mes_ahorradas"] / casos["esfuerzo"]).round(1)

    # ---- Stack de IA del asesor ----
    _stack = [
        ("Claude (LLM)", "Razonamiento / Estrategia", 95, "Diario"),
        ("Python + pandas", "Análisis de datos", 88, "Diario"),
        ("Supabase", "Backend / Base de datos", 82, "Diario"),
        ("n8n", "Automatización de flujos", 70, "Semanal"),
        ("Plotly / Streamlit", "Visualización", 78, "Semanal"),
        ("React + TypeScript", "Frontend de sistemas", 85, "Diario"),
        ("LightGBM / ML", "Modelos predictivos", 55, "Mensual"),
        ("OCR + Vision", "Ingesta de documentos", 48, "Semanal"),
    ]
    stack = pd.DataFrame(_stack, columns=["herramienta", "funcion", "dominio_pct", "frecuencia"])

    series["mes_label"] = series["mes"].dt.strftime("%b %Y")
    return series, casos, stack


def style_fig(fig, height=380, legend=True):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=PLOT_FONT,
        height=height,
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0,
                    bgcolor="rgba(0,0,0,0)") if legend else dict(),
        hoverlabel=dict(bgcolor=SLATE, font_size=12,
                        bordercolor="rgba(255,255,255,0.15)"),
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.05)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)", zeroline=False)
    return fig


def kpi_card(col, label, value, delta=None, up=True, foot=""):
    delta_html = ""
    if delta is not None:
        cls = "up" if up else "down"
        arrow = "▲" if up else "▼"
        delta_html = f'<div class="kpi-delta {cls}">{arrow} {delta}</div>'
    col.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {delta_html}
            <div class="kpi-foot">{foot}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section(eyebrow, title, note=""):
    st.markdown(f'<div class="sec-eyebrow">{eyebrow}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sec-title">{title}</div>', unsafe_allow_html=True)
    if note:
        st.markdown(f'<div class="sec-note">{note}</div>', unsafe_allow_html=True)


# ======================================================================
# APP
# ======================================================================
def main():
    inject_css()
    series, casos, stack = load_data()

    # ------------------------------------------------------------------
    # Sidebar — filtros interactivos
    # ------------------------------------------------------------------
    with st.sidebar:
        st.markdown('<div class="side-brand">◆ AI Advisor OS</div>', unsafe_allow_html=True)
        st.markdown('<div class="side-sub">Reyes Betancourt · IA aplicada a Negocios</div>',
                    unsafe_allow_html=True)
        st.divider()

        st.caption("FILTROS")
        sectores = sorted(series["sector"].unique())
        sel_sectores = st.multiselect("Sector", sectores, default=sectores)

        verticales_disp = sorted(
            series[series["sector"].isin(sel_sectores)]["vertical"].unique()
        )
        sel_verticales = st.multiselect(
            "Vertical de negocio", verticales_disp, default=verticales_disp
        )

        meses = series["mes"].sort_values().unique()
        rango = st.select_slider(
            "Rango de meses",
            options=[pd.Timestamp(m).strftime("%b %Y") for m in meses],
            value=(pd.Timestamp(meses[0]).strftime("%b %Y"),
                   pd.Timestamp(meses[-1]).strftime("%b %Y")),
        )
        st.divider()
        st.caption("Datos sintéticos calibrados · 18 meses · 6 verticales")

    # Aplicar filtros
    m_ini = pd.to_datetime(rango[0], format="%b %Y")
    m_fin = pd.to_datetime(rango[1], format="%b %Y")
    df = series[
        series["sector"].isin(sel_sectores)
        & series["vertical"].isin(sel_verticales)
        & series["mes"].between(m_ini, m_fin)
    ].copy()

    if df.empty:
        st.warning("No hay datos con los filtros seleccionados. Ajusta el sidebar.")
        st.stop()

    # ------------------------------------------------------------------
    # HERO
    # ------------------------------------------------------------------
    st.markdown('<div class="hero-eyebrow">Visualización de Datos · Proyecto Final</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-title">La IA como <span class="accent">sistema operativo</span><br>'
        'del asesor de negocios</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="hero-sub">No uso la inteligencia artificial para tener una opinión: la uso '
        'para <b>construir sistemas que operan negocios reales</b>. Este tablero mide el impacto '
        'de la IA en 6 verticales que diseño y opero — de la clínica de gastro al trading — '
        'traduciendo estrategia en horas ahorradas, clientes atendidos e ingresos generados.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="hero-rule"></div>', unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # KPIs — estado más reciente vs línea base pre-IA
    # ------------------------------------------------------------------
    ult_mes = df["mes"].max()
    df_ult = df[df["mes"] == ult_mes]

    horas_ahorradas_mes = df_ult["horas_ahorradas"].sum()
    ingresos_mes = df_ult["ingresos_mxn"].sum()
    clientes_mes = df_ult["clientes_activos"].sum()
    auto_prom = df_ult["pct_automatizado"].mean()
    nps_prom = df_ult["nps"].mean()

    # Comparación con primer mes del rango
    prm_mes = df["mes"].min()
    df_prm = df[df["mes"] == prm_mes]
    delta_ingresos = (ingresos_mes / max(df_prm["ingresos_mxn"].sum(), 1) - 1) * 100
    delta_clientes = (clientes_mes / max(df_prm["clientes_activos"].sum(), 1) - 1) * 100

    section("Panel ejecutivo", f"Estado al {ult_mes.strftime('%B %Y')}",
            "Indicadores clave del portafolio de sistemas con IA.")

    c1, c2, c3, c4, c5 = st.columns(5)
    kpi_card(c1, "Horas liberadas / mes", f"{horas_ahorradas_mes:,.0f} h",
             foot="Trabajo manual sustituido por IA")
    kpi_card(c2, "Ingresos del mes", f"${ingresos_mes/1e6:,.2f} M",
             delta=f"{delta_ingresos:,.0f}% en el rango", up=delta_ingresos >= 0,
             foot="MXN · suma de verticales")
    kpi_card(c3, "Clientes activos", f"{clientes_mes:,.0f}",
             delta=f"{delta_clientes:,.0f}% en el rango", up=delta_clientes >= 0,
             foot="Capacidad ampliada por IA")
    kpi_card(c4, "Automatización", f"{auto_prom:,.0f}%",
             foot="Tareas operadas por IA")
    kpi_card(c5, "Satisfacción (NPS)", f"{nps_prom:,.0f}",
             foot="Escala 0–100")

    # ------------------------------------------------------------------
    # STORYTELLING 1: El antes y después de la IA
    # ------------------------------------------------------------------
    section("El punto de inflexión", "Horas manuales que la IA me devolvió",
            "Cada vertical adoptó IA en un momento distinto. La curva muestra cómo las horas de "
            "trabajo manual caen tras esa adopción — tiempo que se reinvierte en estrategia.")

    col_a, col_b = st.columns([1.6, 1])

    with col_a:
        agg = (df.groupby("mes")
                 .agg(horas_manuales=("horas_manuales", "sum"),
                      horas_ahorradas=("horas_ahorradas", "sum"))
                 .reset_index())
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=agg["mes"], y=agg["horas_manuales"], name="Horas manuales",
            mode="lines", line=dict(color=CORAL, width=3),
            fill="tozeroy", fillcolor="rgba(255,122,107,0.10)"))
        fig.add_trace(go.Scatter(
            x=agg["mes"], y=agg["horas_ahorradas"], name="Horas liberadas por IA",
            mode="lines", line=dict(color=CYAN, width=3),
            fill="tozeroy", fillcolor="rgba(56,225,198,0.10)"))
        fig.update_layout(title="Carga operativa: manual vs. liberada por IA")
        st.plotly_chart(style_fig(fig, 400), width='stretch')

    with col_b:
        total_ahorradas = df["horas_ahorradas"].sum()
        st.markdown(
            f'<div class="insight">En el rango seleccionado, la IA liberó '
            f'<b>{total_ahorradas:,.0f} horas</b> de trabajo operativo. A un costo de '
            f'oportunidad conservador de <b>$450 MXN/hora</b> de asesoría, eso equivale a '
            f'<b>${total_ahorradas*450/1e6:,.1f} M MXN</b> en capacidad estratégica '
            f'recuperada — el verdadero retorno de la IA no es el software, es el '
            f'<b>tiempo del experto</b>.</div>',
            unsafe_allow_html=True,
        )
        # Donut: reparto de horas ahorradas por sector
        by_sector = df.groupby("sector")["horas_ahorradas"].sum().reset_index()
        fig_d = go.Figure(go.Pie(
            labels=by_sector["sector"], values=by_sector["horas_ahorradas"],
            hole=0.62,
            marker=dict(colors=[SECTOR_COLORS.get(s, VIOLET) for s in by_sector["sector"]]),
            textinfo="percent"))
        fig_d.update_layout(title="Horas liberadas por sector")
        st.plotly_chart(style_fig(fig_d, 260, legend=True), width='stretch')

    # ------------------------------------------------------------------
    # STORYTELLING 2: Crecimiento de ingresos y clientes
    # ------------------------------------------------------------------
    section("El resultado de negocio", "Ingresos por vertical en el tiempo",
            "Al liberar capacidad, cada sistema atiende a más clientes y genera más ingresos. "
            "El área apilada muestra la contribución de cada vertical al portafolio.")

    piv = (df.pivot_table(index="mes", columns="vertical",
                          values="ingresos_mxn", aggfunc="sum")
             .fillna(0))
    fig_area = go.Figure()
    palette = [VIOLET, CYAN, GOLD, CORAL, "#9B8CFF", "#5AD1B8"]
    for i, col in enumerate(piv.columns):
        fig_area.add_trace(go.Scatter(
            x=piv.index, y=piv[col], name=col, mode="lines",
            stackgroup="one", line=dict(width=0.5, color=palette[i % len(palette)]),
            fillcolor=palette[i % len(palette)].replace(")", ",0.55)").replace("#", "rgba(")
            if False else None))
    # Recolorear con opacidad usando px para robustez
    fig_area = px.area(
        df, x="mes", y="ingresos_mxn", color="vertical",
        color_discrete_sequence=palette,
        labels={"ingresos_mxn": "Ingresos (MXN)", "mes": ""},
    )
    fig_area.update_layout(title="Ingresos mensuales apilados por vertical")
    st.plotly_chart(style_fig(fig_area, 420), width='stretch')

    # ------------------------------------------------------------------
    # STORYTELLING 3: Matriz de casos de uso (impacto vs esfuerzo)
    # ------------------------------------------------------------------
    section("Priorización con IA", "Matriz impacto vs. esfuerzo de los casos de uso",
            "Cada burbuja es un caso de uso de IA implementado. Arriba a la izquierda = alto "
            "impacto, bajo esfuerzo (ganancias rápidas). El tamaño representa horas ahorradas/mes.")

    casos_f = casos[casos["vertical"].isin(sel_verticales)] if sel_verticales else casos
    if casos_f.empty:
        casos_f = casos
    fig_bub = px.scatter(
        casos_f, x="esfuerzo", y="impacto",
        size="horas_mes_ahorradas", color="vertical",
        hover_name="caso_uso", size_max=42,
        color_discrete_sequence=palette,
        labels={"esfuerzo": "Esfuerzo de implementación →",
                "impacto": "Impacto en el negocio →"},
    )
    fig_bub.add_shape(type="rect", x0=0.5, x1=5.5, y0=6.5, y1=9.8,
                      line=dict(color="rgba(56,225,198,0.4)", width=1, dash="dot"),
                      fillcolor="rgba(56,225,198,0.05)")
    fig_bub.add_annotation(x=1.4, y=9.6, text="Ganancias rápidas",
                           showarrow=False, font=dict(color=CYAN, size=12))
    fig_bub.update_layout(title="Portafolio de casos de uso de IA")
    fig_bub.update_xaxes(range=[0.5, 9.8])
    fig_bub.update_yaxes(range=[4.5, 9.8])
    st.plotly_chart(style_fig(fig_bub, 440), width='stretch')

    top = casos_f.sort_values("roi_score", ascending=False).iloc[0]
    st.markdown(
        f'<div class="insight">El caso de mayor retorno relativo es '
        f'<b>{top["caso_uso"]}</b> ({top["vertical"]}), con un ROI-score de '
        f'<b>{top["roi_score"]:.0f}</b> y <b>{top["horas_mes_ahorradas"]:.0f} h/mes</b> '
        f'ahorradas. Priorizar con datos —y no por intuición— es en sí mismo una '
        f'ventaja que la IA me da como asesor.</div>',
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------------
    # STORYTELLING 4: Automatización vs satisfacción + stack
    # ------------------------------------------------------------------
    section("Calidad, no solo velocidad", "¿Automatizar mejora la experiencia del cliente?",
            "Relación entre el nivel de automatización por IA y la satisfacción (NPS). "
            "La tendencia positiva refuta el mito de que automatizar deshumaniza el servicio.")

    col_x, col_y = st.columns([1.4, 1])
    with col_x:
        fig_sc = px.scatter(
            df, x="pct_automatizado", y="nps", color="sector",
            trendline="ols", opacity=0.7,
            color_discrete_map=SECTOR_COLORS,
            labels={"pct_automatizado": "% de tareas automatizadas por IA",
                    "nps": "Satisfacción del cliente (NPS)"},
        )
        fig_sc.update_layout(title="Automatización vs. satisfacción")
        st.plotly_chart(style_fig(fig_sc, 400), width='stretch')

    with col_y:
        section("", "Mi stack de IA", "")
        stack_sorted = stack.sort_values("dominio_pct", ascending=True)
        fig_bar = go.Figure(go.Bar(
            x=stack_sorted["dominio_pct"], y=stack_sorted["herramienta"],
            orientation="h",
            marker=dict(color=stack_sorted["dominio_pct"],
                        colorscale=[[0, VIOLET], [1, CYAN]], showscale=False),
            text=[f"{v}%" for v in stack_sorted["dominio_pct"]],
            textposition="outside",
        ))
        fig_bar.update_layout(title="Nivel de dominio por herramienta")
        fig_bar.update_xaxes(range=[0, 108])
        st.plotly_chart(style_fig(fig_bar, 360, legend=False), width='stretch')

    # ------------------------------------------------------------------
    # Cierre / tabla de detalle
    # ------------------------------------------------------------------
    section("Del dato a la decisión", "Detalle por vertical (mes más reciente)",
            "El resumen que llevaría a una reunión de dirección.")

    tabla = (df_ult[["vertical", "sector", "clientes_activos", "ingresos_mxn",
                     "horas_ahorradas", "pct_automatizado", "nps"]]
             .sort_values("ingresos_mxn", ascending=False)
             .rename(columns={
                 "vertical": "Vertical", "sector": "Sector",
                 "clientes_activos": "Clientes", "ingresos_mxn": "Ingresos (MXN)",
                 "horas_ahorradas": "Horas ahorradas", "pct_automatizado": "% Auto",
                 "nps": "NPS"}))
    st.dataframe(
        tabla.style.format({
            "Ingresos (MXN)": "${:,.0f}",
            "Horas ahorradas": "{:,.0f} h",
            "% Auto": "{:.0f}%",
            "NPS": "{:.0f}",
        }),
        width='stretch', hide_index=True,
    )

    st.markdown(
        '<div class="foot">Proyecto Final · Visualización de Datos — IA aplicada a Negocios · '
        'Reyes Betancourt García · Datos sintéticos con fines académicos · '
        'Construido con Streamlit + Plotly</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
