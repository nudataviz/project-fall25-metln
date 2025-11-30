---
title: Customer Overview
---

<link rel="stylesheet" href="https://unpkg.com/maplibre-gl@5.13.0/dist/maplibre-gl.css" />
 
```js
import maplibregl from "npm:maplibre-gl";
```
```js
let customers_full = await FileAttachment("/data/Event_Purchaser_2025-11-10T1531_CLEAN - Event_Purchaser_2025-11-10T1531.csv").csv({typed: true})
```

```js
//is this the correct Column? The correct number for that column?! I do not know. 
let customer_data = Array.from(customers_full)
for (let i = 0; i < customer_data.length; i++){
    if (customer_data[i]["mr_geo_latlong"]) {  // a few null categories
        const [lat, lon] = customer_data[i]["mr_geo_latlong"].split(";")[0].split(",").map(Number);
        customer_data[i]["latitude"] = lat;
        customer_data[i]["longitude"] = lon;
    } else {
        customer_data[i]["latitude"] = null;
        customer_data[i]["longitude"] = null;
    }
}
```

```js
const us = await fetch(
  import.meta.resolve("npm:us-atlas/counties-10m.json")
).then(r => r.json());
```
```js
const new_england = {
  type: "FeatureCollection",
  features: topojson
    .feature(us, us.objects.states)
    .features
    .filter(d => ["23", "25", "33", '09', '44','50','36'].includes(d.id))
};
```

```js
const mapv1=Plot.plot({
  height:400,
  projection: {
    type: "albers",
    domain: new_england
  },
  marks: [
    Plot.geo(new_england, {
      stroke: "black",
      fill: "white"
    }),
    Plot.dot(customer_data.filter(d => d.latitude && d.longitude), {
      x: "longitude",
      y: "latitude",
      fill: "red",
      r: 3,
      fillOpacity: 0.5,
      tip:true,
      title: d => [d.mr_geo_city_name, d.event_purchased]
  .filter(v => v != null)
  .join('\n')
    })
  ]
})
  
```
<div class="card">
<h1>Regional Overview</h1>
<h2>Hover to see Location and Events Purchased </h2>
  ${mapv1}
</div>

<div class="card">

  <div id="mapv2" style="height: 400px; width: 100%;"></div> 
</div>

```js
const mapv2 = (() => {

  const map = new maplibregl.Map({
    container: 'mapv2',
    style: 'https://tiles.openfreemap.org/styles/bright',
    center: [-70.2, 43.6], //portland
    zoom: 6
  });
  
  map.addControl(new maplibregl.NavigationControl());
  
  map.on('load', () => {
    // Add GeoJson Layer ie classnotes
    const geojson = {
      type: 'FeatureCollection',
      features: customer_data
        .filter(d => d.latitude && d.longitude)
        .map(d => ({
          type: 'Feature',
          geometry: {
            type: 'Point',
            coordinates: [d.longitude, d.latitude]
          },
          properties: {}
        }))
    };
    
    map.addSource('customers', {
      type: 'geojson',
      data: geojson
    });
    
    map.addLayer({
      id: 'customers-heat',
      type: 'heatmap',
      source: 'customers',
      maxzoom:15,
      paint: {
        'heatmap-weight': 1,
        'heatmap-intensity': 1,
        'heatmap-color': [
          'interpolate',
          ['linear'],
          ['heatmap-density'],
          0, 'rgba(33,102,172,0)',
          0.2, 'rgb(103,169,207)',
          0.4, 'rgb(209,229,240)',
          0.6, 'rgb(253,219,199)',
          0.8, 'rgb(239,138,98)',
          1, 'rgb(178,24,43)'
        ],
        'heatmap-radius': 30,
        'heatmap-opacity': 0.8
      }
    });
    
    // Add circle layer for zoomed in view
    map.addLayer({
      id: 'customers-point',
      type: 'circle',
      source: 'customers',
      minzoom: 1,
      paint: {
        'circle-radius': 5,
        'circle-color': 'rgb(178,24,43)',
        'circle-stroke-width': 1,
        'circle-stroke-color': '#fff'
      }
    });
  });
  
  //return container;
})();
//from heatmap documentation on maplibre
```


```js
const categoryCount = d3.rollup(
  customers_full.filter(d => d.preferred_main_category != null),
  v => v.length,
  d => d.preferred_main_category
);

const bubbleData = Array.from(categoryCount, ([preferred_main_category, count]) => ({
  preferred_main_category: preferred_main_category.charAt(0).toUpperCase() + preferred_main_category.slice(1).toLowerCase(),
  count
}));
```


```js
const data = { 
  name: "root", 
  children: bubbleData.map(d => ({
    name: d.preferred_main_category,
    value: d.count
  }))
};
```
```js
const bubbleChart = (() => {
const width = 928;
const height = width;
const margin = 1;

const format = d3.format(",d");

const pack = d3.pack()
  .size([width - margin * 2, height - margin * 2])
  .padding(3);

const root = pack(
  d3.hierarchy(data)
    .sum(d => d.value)
    .sort((a, b) => b.value - a.value)
);

const svg = d3.create("svg")
  .attr("width", width)
  .attr("height", height)
  .attr("viewBox", [-margin, -margin, width, height])
  .attr("style", "width: 100%; height: auto; font-family: 'Segoe UI', Tahoma, sans-serif;")
  .attr("text-anchor", "middle");

const node = svg.append("g")
  .selectAll("g")
  .data(root.descendants())
  .join("g")
    .attr("transform", d => `translate(${d.x},${d.y})`);

node.append("title")
  .text(d => `${d.data.name}\n${format(d.value)}`);

node.append("circle")
  .attr("fill", d => d.children ? "#fff" : "#ddd")
  .attr("stroke", d => d.children ? "#bbb" : null)
  .attr("r", d => d.r);

const text = node
  .filter(d => !d.children && d.r > 10)
  .append("text")
    .attr("clip-path", d => `circle(${d.r})`)
    .style("font-size", d => `${Math.min(d.r / 3, 16)}px`)
    .style("font-weight", "600");

// Wrap text using foreignObject for automatic wrapping
node
  .filter(d => !d.children && d.r > 20)
  .append("foreignObject")
    .attr("x", d => -d.r)
    .attr("y", d => -d.r)
    .attr("width", d => d.r * 2)
    .attr("height", d => d.r * 2)
    .append("xhtml:div")
      .style("display", "flex")
      .style("flex-direction", "column")
      .style("align-items", "center")
      .style("justify-content", "center")
      .style("height", "100%")
      .style("text-align", "center")
      .style("padding", "5px")
      .style("font-family", "'Segoe UI', Tahoma, sans-serif")
      .style("overflow", "hidden")
      .html(d => {
        const fontSize = Math.min(d.r / 3, 16);
        const countSize = Math.min(d.r / 4, 12);
        return `
          <div style="font-size: ${fontSize}px; font-weight: 600; line-height: 1.2;">
            ${d.data.name}
          </div>
          <div style="font-size: ${countSize}px; opacity: 0.7; margin-top: 4px;">
            ${format(d.value)}
          </div>
        `;
      });

return (svg.node());
})()
```

<div class="card" style="background-color: #e3f2fd;">
<h1>Preferred Main Category</h1> 
 ${bubbleChart}
</div>`

```js
const gettingCurrent_cat = customer_data
  .filter(d => d.current_category != null && d.current_category !== "null" && d.current_category !== "")
  .flatMap(d => {
    const categories = d.current_category.split(/[,;|]+/); //
    return categories
      .map(cat => cat.trim())
      .filter(cat => cat !== "" && cat !== "null" && cat.toLowerCase() !== "null")
      .map(cat => ({
        ...d,
        current_category: cat
      }));
  });
```
```js
// histogram
const chart = Plot.plot({
  title: "Hover over me to see the Current Category",
  y: {grid: true},
  x: {tickFormat: null},
  marks: [
    Plot.barY(gettingCurrent_cat, Plot.groupX({y: "count"}, 
         {x: "current_category", fill: "steelblue", tip: true, sort: {x: "-y"}})),
    Plot.ruleY([0])
  ]
});
```

<div class="card">
<h1>Current Category</h1>
  ${chart}
</div>


```js
const RegistrationArray = Array.from(
  d3.rollup(
    customers_full.filter(d => d.registration_status != null),  
    v => v.length,
    d => d.registration_status
  ),
  ([name, value]) => ({name, value}) 
);
```



```js
const registration_bar = Plot.plot({
  title:"Registration Status",
  marks: [
    Plot.barY(customers_full.filter(d => d.registration_status != null), 
      Plot.groupX(
        {y: "count"}, 
        {x: "registration_status", fill: "registration_status", tip: true}
      )
    ),
    Plot.ruleY([0])
  ],
  x: {label: "registration_status"},
  y: {label: "Count"},
  //color: {legend: true}
})
```
<div class="card">
<h1>Registration Status</h1>
  ${registration_pie}
</div>


```js
const timeOrder = [
  "4 AM - 5 AM", "5 AM - 6 AM", "6 AM - 7 AM", "7 AM - 8 AM", "8 AM - 9 AM",
  "9 AM - 10 AM", "10 AM - 11 AM", "11 AM - 12 PM",
  "12 PM - 1 PM", "1 PM - 2 PM", "2 PM - 3 PM", "3 PM - 4 PM",
  "4 PM - 5 PM", "5 PM - 6 PM", "6 PM - 7 PM", "7 PM - 8 PM",
  "8 PM - 9 PM", "9 PM - 10 PM", "10 PM - 11 PM", "11 PM - 12 AM", "1 AM - 2 AM", "2 AM - 3 AM", "3 AM - 4 AM",
];

customers_full.sort((a, b) => 
  timeOrder.indexOf(a.visit_time) - timeOrder.indexOf(b.visit_time)
);
```
```js
const time_of_visit = Plot.plot({
  //title:"Time Visited",
  marginLeft: 100,
  y: {
    domain: timeOrder, label: "Time of Visit"},
  marks: [
    Plot.barX(customers_full.filter(d => d.visit_time != null), 
      Plot.groupY(
        {x: "count"}, 
        {y: "visit_time", fill: "visit_time", tip: true}
      )
    ),
    Plot.ruleX([0])
  ],
})
```

<div class="card">
<h1>Time of Visit</h1>
  ${time_of_visit}
</div>

```js
// copied from observable
function PieChart(data, {
  name = ([x]) => x,  // given d in data, returns the (ordinal) label
  value = ([, y]) => y, // given d in data, returns the (quantitative) value
  title, // given d in data, returns the title text
  width = 640, // outer width, in pixels
  height = 400, // outer height, in pixels
  innerRadius = 0, // inner radius of pie, in pixels (non-zero for donut)
  outerRadius = Math.min(width, height) / 2, // outer radius of pie, in pixels
  labelRadius = (innerRadius * 0.2 + outerRadius * 0.8), // center radius of labels
  format = ",", // a format specifier for values (in the label)
  names, // array of names (the domain of the color scale)
  colors, // array of colors for names
  stroke = innerRadius > 0 ? "none" : "white", // stroke separating widths
  strokeWidth = 1, // width of stroke separating wedges
  strokeLinejoin = "round", // line join of stroke separating wedges
  padAngle = stroke === "none" ? 1 / outerRadius : 0, // angular separation between wedges, in radians
} = {}) {
  // Compute values.
  const N = d3.map(data, name);
  const V = d3.map(data, value);
  const I = d3.range(N.length).filter(i => !isNaN(V[i]));

  // Unique the names.
  if (names === undefined) names = N;
  names = new d3.InternSet(names);

  // Chose a default color scheme based on cardinality.
  if (colors === undefined) colors = d3.schemeSpectral[names.size];
  if (colors === undefined) colors = d3.quantize(t => d3.interpolateSpectral(t * 0.8 + 0.1), names.size);

  // Construct scales.
  const color = d3.scaleOrdinal(names, colors);

  // Compute titles.
  if (title === undefined) {
    const formatValue = d3.format(format);
    title = i => `${N[i]}\n${formatValue(V[i])}`;
  } else {
    const O = d3.map(data, d => d);
    const T = title;
    title = i => T(O[i], i, data);
  }

  // Construct arcs.
  const arcs = d3.pie().padAngle(padAngle).sort(null).value(i => V[i])(I);
  const arc = d3.arc().innerRadius(innerRadius).outerRadius(outerRadius);
  const arcLabel = d3.arc().innerRadius(labelRadius).outerRadius(labelRadius);
  
  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [-width / 2, -height / 2, width, height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

  svg.append("g")
      .attr("stroke", stroke)
      .attr("stroke-width", strokeWidth)
      .attr("stroke-linejoin", strokeLinejoin)
    .selectAll("path")
    .data(arcs)
    .join("path")
      .attr("fill", d => color(N[d.data]))
      .attr("d", arc)
    .append("title")
      .text(d => title(d.data));

  svg.append("g")
      .attr("font-family", "sans-serif")
      .attr("font-size", 20)
      .attr("text-anchor", "middle")
    .selectAll("text")
    .data(arcs)
    .join("text")
      .attr("transform", d => `translate(${arcLabel.centroid(d)})`)
    .selectAll("tspan")
    .data(d => {
      if ((d.endAngle - d.startAngle) < 0.1) return [];
      const lines = `${title(d.data)}`.split(/\n/);
      return (d.endAngle - d.startAngle) > 0.25 ? lines : lines.slice(0, 1);
    })
    .join("tspan")
      .attr("x", 0)
      .attr("y", (_, i) => `${i * 1.1}em`)
      .attr("font-weight", (_, i) => i ? null : "bold")
      .text(d => d);

  return Object.assign(svg.node(), {scales: {color}});
}
```

```js
const registration_pie=PieChart(RegistrationArray, {
      name: d => d.name,
      value: d => d.value,
      width: 500,
      height: 400,
      //colors: ["#89CFF0", "#FFB7CE"],
      labelRadius: 90,
      title: (d) => {
        const total = d3.sum(RegistrationArray, p => p.value);
        const percentage = ((d.value / total) * 100).toFixed(1);
        return `${d.name}\n${percentage}%\n${d.value}`;
      }
    })
```
