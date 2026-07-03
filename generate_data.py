"""
Generador de datasets sintéticos realistas para el dashboard
"IA como Sistema Operativo del Asesor de Negocios".

Modela el impacto medible de la IA en 6 verticales de negocio
reales sobre las que Reyes Betancourt asesora y construye sistemas.

Todos los datos son SINTÉTICOS pero calibrados con supuestos de mercado
razonables (MXN, ciclos de adopción, benchmarks de productividad de IA).
Se fija una semilla para reproducibilidad total.
"""

import numpy as np
import pandas as pd

RNG = np.random.default_rng(2026)

# ---------------------------------------------------------------------------
# Catálogo maestro de verticales (los 6 sistemas que Reyes desarrolla con IA)
# ---------------------------------------------------------------------------
VERTICALES = [
    {"id": "UEGE",          "nombre": "Clínica de Gastroenterología", "sector": "Salud",        "ticket_mxn": 2800},
    {"id": "PATRIMONIO",    "nombre": "Gestión de Activos Familiares", "sector": "Fintech",      "ticket_mxn": 5200},
    {"id": "BGREAT",        "nombre": "Coworking Dental",              "sector": "Salud",        "ticket_mxn": 3400},
    {"id": "BARBER",        "nombre": "Sistema para Barberías",        "sector": "Servicios",    "ticket_mxn": 380},
    {"id": "RENTAS",        "nombre": "Administración de Rentas",      "sector": "Real Estate",  "ticket_mxn": 14500},
    {"id": "CRIPTO",        "nombre": "Trading de Criptomonedas",      "sector": "Fintech",      "ticket_mxn": 1900},
]

# Meses de operación: 18 meses (ene 2025 -> jun 2026)
MESES = pd.date_range("2025-01-01", "2026-06-01", freq="MS")


# ---------------------------------------------------------------------------
# 1) SERIE MENSUAL POR VERTICAL — el corazón del storytelling "antes/después de IA"
# ---------------------------------------------------------------------------
def build_series() -> pd.DataFrame:
    rows = []
    for v in VERTICALES:
        # Punto de adopción de IA: cada vertical la incorpora en un mes distinto
        mes_adopcion = RNG.integers(3, 9)  # entre mar-2025 y sep-2025
        base_horas = RNG.uniform(90, 160)  # horas manuales/mes antes de IA
        base_clientes = RNG.uniform(40, 220)
        for i, mes in enumerate(MESES):
            adoptado = i >= mes_adopcion
            # Curva de adopción suave (logística) tras el punto de adopción
            ramp = 1 / (1 + np.exp(-(i - mes_adopcion - 2))) if adoptado else 0.0

            # Horas de trabajo manual: caen con la IA
            reduccion = 0.55 * ramp  # hasta -55% de horas manuales
            horas = base_horas * (1 - reduccion) * RNG.uniform(0.95, 1.05)

            # Crecimiento de clientes: la IA libera capacidad -> más clientes
            crecimiento = 1 + (0.9 * ramp)
            clientes = base_clientes * crecimiento * (1 + 0.015 * i) * RNG.uniform(0.96, 1.04)

            ingresos = clientes * v["ticket_mxn"] * RNG.uniform(0.95, 1.05)

            # Satisfacción del cliente (NPS-like 0-100)
            nps = np.clip(58 + 28 * ramp + RNG.normal(0, 3), 40, 95)

            # % de tareas automatizadas por IA
            pct_auto = np.clip(72 * ramp + RNG.normal(0, 4), 0, 88)

            # Horas ahorradas frente a la línea base pre-IA
            horas_ahorradas = max(base_horas - horas, 0)

            rows.append({
                "vertical_id": v["id"],
                "vertical": v["nombre"],
                "sector": v["sector"],
                "mes": mes,
                "adopcion_ia": bool(adoptado),
                "horas_manuales": round(horas, 1),
                "horas_ahorradas": round(horas_ahorradas, 1),
                "clientes_activos": int(clientes),
                "ingresos_mxn": round(ingresos, 0),
                "pct_automatizado": round(pct_auto, 1),
                "nps": round(nps, 1),
                "ticket_mxn": v["ticket_mxn"],
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 2) CASOS DE USO DE IA — matriz de impacto vs esfuerzo (para bubble chart)
# ---------------------------------------------------------------------------
def build_use_cases() -> pd.DataFrame:
    casos = [
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
    df = pd.DataFrame(casos, columns=[
        "vertical_id", "caso_uso", "categoria", "impacto", "esfuerzo", "horas_mes_ahorradas"
    ])
    mapa = {v["id"]: v["nombre"] for v in VERTICALES}
    df["vertical"] = df["vertical_id"].map(mapa)
    # ROI estimado = beneficio / esfuerzo (proxy visual)
    df["roi_score"] = (df["impacto"] * df["horas_mes_ahorradas"] / df["esfuerzo"]).round(1)
    return df


# ---------------------------------------------------------------------------
# 3) ADOPCIÓN DE HERRAMIENTAS DE IA EN EL STACK DEL ASESOR
# ---------------------------------------------------------------------------
def build_stack() -> pd.DataFrame:
    stack = [
        ("Claude (LLM)",        "Razonamiento / Estrategia", 95, "Diario"),
        ("Python + pandas",     "Análisis de datos",         88, "Diario"),
        ("Supabase",            "Backend / Base de datos",   82, "Diario"),
        ("n8n",                 "Automatización de flujos",  70, "Semanal"),
        ("Plotly / Streamlit",  "Visualización",             78, "Semanal"),
        ("React + TypeScript",  "Frontend de sistemas",      85, "Diario"),
        ("LightGBM / ML",       "Modelos predictivos",       55, "Mensual"),
        ("OCR + Vision",        "Ingesta de documentos",     48, "Semanal"),
    ]
    return pd.DataFrame(stack, columns=["herramienta", "funcion", "dominio_pct", "frecuencia"])


if __name__ == "__main__":
    series = build_series()
    casos = build_use_cases()
    stack = build_stack()

    series.to_csv("data/series_mensual.csv", index=False)
    casos.to_csv("data/casos_uso.csv", index=False)
    stack.to_csv("data/stack_ia.csv", index=False)

    print("Datasets generados:")
    print(f"  series_mensual.csv  -> {series.shape[0]} filas, {series.shape[1]} columnas")
    print(f"  casos_uso.csv       -> {casos.shape[0]} filas, {casos.shape[1]} columnas")
    print(f"  stack_ia.csv        -> {stack.shape[0]} filas, {stack.shape[1]} columnas")
