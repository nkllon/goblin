import * as d3 from "d3";

type NodeDatum = {
  id: string;
  label: string;
  score?: number | null;
  tier?: string | null;
  type: string;
};

type EdgeDatum = {
  source: string;
  target: string;
  type: string;
};

function scoreColor(score?: number | null): string {
  if (score == null || isNaN(score)) return "#d3d3d3";
  const s = Math.min(1, Math.max(0, score));
  let r = 0, g = 0;
  if (s < 0.5) {
    r = Math.floor(2 * s * 255);
    g = 255;
  } else {
    r = 255;
    g = Math.floor((1 - 2 * (s - 0.5)) * 255);
  }
  return `rgb(${r},${g},0)`;
}

async function loadData() {
  const res = await fetch("goblin.json", { cache: "no-store" });
  return (await res.json()) as {
    nodes: NodeDatum[];
    edges: EdgeDatum[];
  };
}

function renderGraph(container: HTMLElement, nodes: NodeDatum[], edges: EdgeDatum[]) {
  const width = container.clientWidth || 960;
  const height = container.clientHeight || 600;

  const svg = d3.select(container).append("svg")
    .attr("width", width)
    .attr("height", height);

  const zoomLayer = svg.append("g");

  const link = zoomLayer.append("g")
    .attr("stroke", "#999")
    .attr("stroke-opacity", 0.6)
    .selectAll("line")
    .data(edges)
    .join("line")
    .attr("stroke-dasharray", d => d.type === "overlapsWith" ? "4,3" : d.type === "dependsOn" ? "2,3" : "0");

  const node = zoomLayer.append("g")
    .selectAll("g")
    .data(nodes)
    .join("g")
    .call(d3.drag<SVGGElement, NodeDatum>()
      .on("start", (event, d: any) => {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x; d.fy = d.y;
      })
      .on("drag", (event, d: any) => {
        d.fx = event.x; d.fy = event.y;
      })
      .on("end", (event, d: any) => {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null; d.fy = null;
      })
    );

  node.append("rect")
    .attr("rx", 8).attr("ry", 8)
    .attr("x", -60).attr("y", -16)
    .attr("width", 120).attr("height", 32)
    .attr("fill", d => scoreColor(d.score))
    .attr("stroke", "#333");

  node.append("text")
    .attr("text-anchor", "middle")
    .attr("dominant-baseline", "middle")
    .attr("font-family", "Helvetica, Arial, sans-serif")
    .attr("font-size", 11)
    .text(d => d.label);

  const idToNode: Record<string, any> = {};
  nodes.forEach((n: any) => { idToNode[n.id] = n; });

  const simulation = d3.forceSimulation(nodes as any)
    .force("link", d3.forceLink(edges as any).id((d: any) => d.id).distance(120))
    .force("charge", d3.forceManyBody().strength(-180))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .on("tick", () => {
      link
        .attr("x1", (d: any) => idToNode[d.source].x)
        .attr("y1", (d: any) => idToNode[d.source].y)
        .attr("x2", (d: any) => idToNode[d.target].x)
        .attr("y2", (d: any) => idToNode[d.target].y);

      node.attr("transform", (d: any) => `translate(${d.x},${d.y})`);
    });

  svg.call(d3.zoom<SVGSVGElement, unknown>()
    .scaleExtent([0.3, 3])
    .on("zoom", (event) => zoomLayer.attr("transform", event.transform)));
}

async function main() {
  const app = document.getElementById("app")!;
  app.innerHTML = "<div class='loading'>Loading goblin graph…</div>";
  try {
    const { nodes, edges } = await loadData();
    app.innerHTML = "";
    renderGraph(app, nodes, edges);
  } catch (e) {
    app.innerHTML = "<div class='error'>Failed to load goblin.json</div>";
    console.error(e);
  }
}

main();
