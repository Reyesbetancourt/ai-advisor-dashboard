# La IA como Sistema Operativo del Asesor de Negocios

Tablero interactivo (Streamlit) que muestra **cómo aplico IA** para pasar de la
estrategia a la entrega técnica end-to-end, y **dónde la aplico** en seis ventures
reales. La pieza central es **Orey AI Assistant**: un grafo de conocimiento
gobernado que orquesta los proyectos y se replica dentro de cada uno.

## Qué incluye
1. **Hero + modelo de impacto ajustable** — mueves tus supuestos (tarifa,
   aceleración de la IA, horizonte) en el panel lateral y los KPIs y la gráfica
   de horas liberadas se recalculan en vivo. Nada simulado: son *tus* supuestos.
2. **El método** — pipeline con IA de 6 etapas (research → arquitectura → spec →
   generación → validación → deploy), con el pico en la generación asistida.
3. **Portafolio** — UEGE, Dentwork, BarberBROTHER, Viajes Zvezda, PatrimonioOS,
   Orey AI. Tarjetas con vertical, stack, rol de la IA y fase.
4. **La operación en datos** — ventures por vertical, fase de madurez, stack
   recurrente y horas liberadas por venture (modelo).
5. **El sistema Orey (sección estrella)** — el pipeline de promoción del
   conocimiento (learning → candidate → gate → pattern → capability), el gate de
   8 criterios, un caso real trazado y un **grafo de conocimiento interactivo**
   (D3, arrastrable) con relaciones tipadas `CONSUMES` y `SOURCED_FROM`.

## Efectos y dinamismo
Animaciones de entrada escalonadas, KPIs y tarjetas con hover, gráficas Plotly
interactivas, y un grafo de fuerzas D3 con física real (arrastra los nodos), halo
pulsante en el núcleo y puntos de flujo animados sobre las aristas.

## Correr localmente
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy
Streamlit Community Cloud conectado a este repositorio de GitHub. El grafo carga
D3 desde CDN (con fallback a jsDelivr y unpkg).

## Estructura
```
├── app.py                 # tablero principal
├── components/
│   ├── __init__.py
│   └── graph.py           # grafo de conocimiento D3 (force-directed)
├── requirements.txt
└── README.md
```

---
Reyes Betancourt García · Especialidad en IA y Ciencia de Datos
