"""
Grafo de conocimiento de Orey — D3 force-directed, interactivo (arrastrar + física).
Aristas tipadas: CONSUMES (venture usa capability) y SOURCED_FROM (venture devuelve learning).
Se embebe en Streamlit vía components.html.
"""
import json
import streamlit.components.v1 as components


def orey_graph(nodes, links, height=560, dark=True):
    palette = {
        "core":      "#38E1D6",   # Orey (núcleo)
        "capability":"#4C7DFF",   # lo que Orey sabe hacer
        "project":   "#F5B455",   # ventures
        "learning":  "#9B7DFF",   # aprendizajes crudos
        "pattern":   "#5FD3A0",   # patrones promovidos
        "ink":       "#0B1220",
        "line":      "#1F2E44",
        "text":      "#E6EDF7",
        "muted":     "#7C8CA6",
    }
    data = json.dumps({"nodes": nodes, "links": links})
    html = f"""
<div id="wrap" style="position:relative;width:100%;height:{height}px;background:transparent;">
  <svg id="g" width="100%" height="{height}"></svg>
  <div id="legend" style="position:absolute;top:10px;left:10px;font-family:'JetBrains Mono',monospace;
       font-size:11px;color:{palette['muted']};background:rgba(11,18,32,.55);
       border:1px solid {palette['line']};border-radius:10px;padding:8px 10px;line-height:1.8;">
    <div><span style="color:{palette['core']}">●</span> Orey (núcleo)</div>
    <div><span style="color:{palette['capability']}">●</span> capability</div>
    <div><span style="color:{palette['project']}">●</span> venture</div>
    <div><span style="color:{palette['pattern']}">●</span> pattern</div>
    <div><span style="color:{palette['learning']}">●</span> learning</div>
    <hr style="border:0;border-top:1px solid {palette['line']};margin:5px 0">
    <div><span style="color:{palette['capability']}">—</span> CONSUMES</div>
    <div><span style="color:{palette['learning']}">╌</span> SOURCED_FROM</div>
  </div>
  <div id="tip" style="position:absolute;pointer-events:none;opacity:0;transition:opacity .15s;
       font-family:'Inter',sans-serif;font-size:12px;color:{palette['text']};
       background:rgba(17,28,46,.96);border:1px solid {palette['line']};border-radius:8px;
       padding:8px 10px;max-width:230px;box-shadow:0 8px 24px rgba(0,0,0,.4);z-index:20;"></div>
  <div id="gfail" style="display:none;position:absolute;inset:0;align-items:center;justify-content:center;
       font-family:'Inter',sans-serif;color:{palette['muted']};font-size:13px;text-align:center;padding:2rem;">
    No se pudo cargar la librería del grafo (sin conexión). El grafo aparece al abrir el tablero en línea.
  </div>
</div>
<script>
// Carga robusta de D3: intenta varias fuentes y solo entonces dibuja.
(function loadD3(srcs, done){{
  if (window.d3) return done();
  if (!srcs.length) {{ document.getElementById('gfail').style.display='flex'; return; }}
  var s=document.createElement('script'); s.src=srcs[0];
  s.onload=function(){{ window.d3 ? done() : loadD3(srcs.slice(1), done); }};
  s.onerror=function(){{ loadD3(srcs.slice(1), done); }};
  document.head.appendChild(s);
}})([
  "https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js",
  "https://cdn.jsdelivr.net/npm/d3@7.8.5/dist/d3.min.js",
  "https://unpkg.com/d3@7.8.5/dist/d3.min.js"
], drawGraph);

function drawGraph(){{
const DATA = {data};
const PAL = {json.dumps(palette)};
const svg = d3.select("#g");
const W = document.getElementById("wrap").clientWidth;
const H = {height};
const tip = d3.select("#tip");

svg.append("defs").html(`
  <filter id="glow"><feGaussianBlur stdDeviation="3.2" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
`);

const color = t => PAL[t] || PAL.muted;
const radius = d => d.type==="core"?30 : d.type==="project"?15 : d.type==="capability"?13 : 9;

const sim = d3.forceSimulation(DATA.nodes)
  .force("link", d3.forceLink(DATA.links).id(d=>d.id)
      .distance(l => l.rel==="CONSUMES"?120:150).strength(0.35))
  .force("charge", d3.forceManyBody().strength(-520))
  .force("center", d3.forceCenter(W/2, H/2))
  .force("collide", d3.forceCollide().radius(d=>radius(d)+14));

// aristas
const link = svg.append("g").selectAll("line").data(DATA.links).join("line")
  .attr("stroke", d => d.rel==="CONSUMES"?PAL.capability:PAL.learning)
  .attr("stroke-opacity", 0.5)
  .attr("stroke-width", 1.6)
  .attr("stroke-dasharray", d => d.rel==="SOURCED_FROM"?"5,5":null);

// flujo animado sobre las aristas (puntos que viajan)
const flow = svg.append("g").selectAll("circle.flow").data(DATA.links).join("circle")
  .attr("class","flow").attr("r",2.4)
  .attr("fill", d => d.rel==="CONSUMES"?PAL.capability:PAL.learning)
  .attr("opacity",0.9);

const node = svg.append("g").selectAll("g").data(DATA.nodes).join("g")
  .style("cursor","grab")
  .call(d3.drag()
    .on("start",(e,d)=>{{if(!e.active)sim.alphaTarget(0.3).restart();d.fx=d.x;d.fy=d.y;}})
    .on("drag",(e,d)=>{{d.fx=e.x;d.fy=e.y;}})
    .on("end",(e,d)=>{{if(!e.active)sim.alphaTarget(0);d.fx=null;d.fy=null;}}));

// halo pulsante para el núcleo
node.filter(d=>d.type==="core").append("circle")
  .attr("r",30).attr("fill","none").attr("stroke",PAL.core).attr("stroke-width",1.5)
  .attr("opacity",0.5).append("animate")
  .attr("attributeName","r").attr("values","30;46;30").attr("dur","3s").attr("repeatCount","indefinite");
node.filter(d=>d.type==="core").select("circle").append("animate")
  .attr("attributeName","opacity").attr("values","0.5;0;0.5").attr("dur","3s").attr("repeatCount","indefinite");

node.append("circle")
  .attr("r", radius)
  .attr("fill", d=>color(d.type))
  .attr("stroke", PAL.ink).attr("stroke-width",2)
  .attr("filter", d=>d.type==="core"?"url(#glow)":null);

node.append("text")
  .text(d=>d.label)
  .attr("x",0).attr("y", d=> radius(d)+13)
  .attr("text-anchor","middle")
  .attr("fill", d=>d.type==="core"?PAL.core:PAL.text)
  .attr("font-family","'Inter',sans-serif")
  .attr("font-size", d=>d.type==="core"?"14px":"11px")
  .attr("font-weight", d=>d.type==="core"?"700":"500");

node.on("mouseover",(e,d)=>{{
    tip.style("opacity",1).html(`<b style="color:${{color(d.type)}}">${{d.label}}</b><br>${{d.desc||''}}`);
    link.attr("stroke-opacity",l=>(l.source.id===d.id||l.target.id===d.id)?0.95:0.08);
    node.style("opacity",n=>connected(d,n)?1:0.25);
  }})
  .on("mousemove",(e)=>{{
    const r=document.getElementById("wrap").getBoundingClientRect();
    tip.style("left",(e.clientX-r.left+14)+"px").style("top",(e.clientY-r.top+14)+"px");
  }})
  .on("mouseout",()=>{{
    tip.style("opacity",0);
    link.attr("stroke-opacity",0.5); node.style("opacity",1);
  }});

const adj = new Set();
DATA.links.forEach(l=>{{adj.add(l.source.id+"|"+l.target.id);adj.add(l.target.id+"|"+l.source.id);}});
function connected(a,b){{return a.id===b.id||adj.has(a.id+"|"+b.id);}}

let t=0;
sim.on("tick",()=>{{
  link.attr("x1",d=>d.source.x).attr("y1",d=>d.source.y)
      .attr("x2",d=>d.target.x).attr("y2",d=>d.target.y);
  node.attr("transform",d=>`translate(${{d.x}},${{d.y}})`);
  t=(t+0.006)%1;
  flow.attr("cx",d=>d.source.x+(d.target.x-d.source.x)*t)
      .attr("cy",d=>d.source.y+(d.target.y-d.source.y)*t);
}});
}} // end drawGraph
</script>
"""
    components.html(html, height=height + 10, scrolling=False)
