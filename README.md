# ◆ La IA como Sistema Operativo del Asesor de Negocios

> Dashboard de visualización de datos que mide el impacto de la Inteligencia Artificial
> en el trabajo de un asesor en estrategia y transformación de negocios, a través de
> **6 sistemas reales** construidos y operados con IA.

**Proyecto Final — Visualización de Datos · Especialidad en IA aplicada a Negocios**
Autor: **Reyes Betancourt García**

---

## 📌 Descripción

Este proyecto no habla de la IA en abstracto. Cuenta, con datos, cómo la inteligencia
artificial transforma un rol profesional concreto: el de un asesor que **diseña y opera
sistemas de negocio de punta a punta** (estrategia + full-stack). El tablero traduce esa
transformación en métricas defendibles: horas de trabajo manual liberadas, clientes
atendidos, ingresos generados y satisfacción del cliente.

Las 6 verticales analizadas son sistemas que efectivamente desarrollo con apoyo de IA:

| Vertical | Sector | Descripción |
|---|---|---|
| Clínica de Gastroenterología (UEGE) | Salud | Agendado, ingesta de documentos y resúmenes clínicos |
| Gestión de Activos Familiares (PatrimonioOS) | Fintech | Motor de reglas fiscales por estado + clasificación de activos |
| Coworking Dental (B·GREAT) | Salud | Ocupación de sillones, facturación CFDI, retención |
| Sistema para Barberías | Servicios | Reservas por WhatsApp con IA, predicción de demanda |
| Administración de Rentas | Real Estate | Screening de inquilinos, cobranza y contratos asistidos |
| Trading de Criptomonedas | Fintech | Señales cuantitativas y gestión de riesgo asistidas por IA |

---

## 🎯 Objetivo

Demostrar, mediante storytelling con datos, que la IA no reemplaza al asesor: **amplifica
su capacidad**. El retorno real de la IA no es el software, sino el **tiempo del experto**
que se reinvierte en estrategia y en atender a más clientes con mayor calidad.

---

## 🧩 Estructura del dashboard

1. **Panel ejecutivo** — 5 KPIs: horas liberadas, ingresos, clientes, automatización, NPS.
2. **El punto de inflexión** — Carga operativa manual vs. liberada por IA (área temporal) + reparto por sector (donut).
3. **El resultado de negocio** — Ingresos apilados por vertical en el tiempo.
4. **Priorización con IA** — Matriz impacto vs. esfuerzo de los casos de uso (bubble chart).
5. **Calidad, no solo velocidad** — Correlación automatización ↔ satisfacción (scatter + OLS) y stack de IA.
6. **Del dato a la decisión** — Tabla ejecutiva de detalle por vertical.

**Filtros interactivos:** sector, vertical de negocio y rango de meses.

---

## 🛠️ Tecnologías

- **Python 3.10+**
- **Streamlit** — framework del tablero
- **Plotly** — visualizaciones interactivas
- **pandas / numpy** — manipulación de datos
- **statsmodels** — línea de tendencia (OLS)

---

## 🚀 Cómo correr la app

    # 1. Clonar el repositorio
    git clone https://github.com/Reyesbetancourt/ai-advisor-dashboard.git
    cd ai-advisor-dashboard

    # 2. (Opcional) crear entorno virtual
    python -m venv .venv
    source .venv/bin/activate        # Windows: .venv\Scripts\activate

    # 3. Instalar dependencias
    pip install -r requirements.txt

    # 4. (Opcional) regenerar los datos sintéticos
    python data/generate_data.py

    # 5. Ejecutar la app
    streamlit run app.py

La app se abrirá en `http://localhost:8501`.

### Despliegue en Streamlit Community Cloud

1. Sube el repo a GitHub.
2. Entra a [share.streamlit.io](https://share.streamlit.io), conecta el repo y apunta a `app.py`.
3. Streamlit instala `requirements.txt` automáticamente y publica la URL.

---

## 📁 Estructura del repositorio

    ai-advisor-dashboard/
    ├── app.py                      # Aplicación principal de Streamlit
    ├── requirements.txt            # Dependencias
    ├── README.md                   # Este archivo
    ├── .gitignore
    ├── .streamlit/
    │   └── config.toml             # Tema visual (dark "Holographic Slate")
    └── data/
        ├── generate_data.py        # Generador de datasets sintéticos (semilla fija)
        ├── series_mensual.csv      # 18 meses × 6 verticales (métricas de negocio)
        ├── casos_uso.csv           # 17 casos de uso de IA (impacto/esfuerzo/ROI)
        └── stack_ia.csv            # Herramientas de IA del stack del asesor

---

## 📊 Sobre los datos

Los datos son **sintéticos pero realistas**, generados con una semilla fija para total
reproducibilidad. Modelan una curva de adopción logística de IA por vertical y calibran
tickets promedio en MXN, ciclos de clientes y benchmarks de productividad. Están pensados
para fines académicos y para ilustrar la narrativa; no representan cifras financieras reales.

---

## 🧠 Conclusión

La IA está redefiniendo qué significa ser asesor de negocios: de *dar recomendaciones* a
*entregar sistemas que operan*. Este tablero es, en sí mismo, una muestra de esa tesis —
diseñado, poblado y contado con las mismas herramientas de IA que uso a diario.

> *"Pienso en sistemas. Y los construyo."*
