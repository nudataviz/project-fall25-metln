---
title: Customer Overview
---

# What & Why
## Supplemental Data

Analyses on this page use a distinct dataset.

This was a large set of data with a variety of dimensions.  Explanation of column names is included in graphs, but we don't have details on 
data definitions.

<link rel="stylesheet" href="https://unpkg.com/maplibre-gl@5.13.0/dist/maplibre-gl.css" />

```js
import {Mutable} from 'npm:@observablehq/stdlib';

```
```js
import maplibregl from "npm:maplibre-gl";
```
```js
let customers_full = await FileAttachment("/data/Event_Purchaser_2025-11-10T1531_CLEAN - Event_Purchaser_2025-11-10T1531.csv").csv({typed: true})
```

```js
//is this the correct Column? The correct number for that column?! I do not know. 
let customer_data = Array.from(customers_full)
for (let i = 0; i < customer_data.length; i++) {
    if (customer_data[i]["mr_geo_latlong"]) {  // some entries may be null
        const [lat, lon] = customer_data[i]["mr_geo_latlong"].split(";")[0].split(",").map(Number);
        customer_data[i]["latitude"] = lat;
        customer_data[i]["longitude"] = lon;
    } else {
        customer_data[i]["latitude"] = null;
        customer_data[i]["longitude"] = null;
    }
}

// Extract city name
for (let i = 0; i < customer_data.length; i++) {
    if (customer_data[i]["geo_city_name"]) {  
        const city_name = customer_data[i]["geo_city_name"].split(";")[0];
        customer_data[i]["City"] = city_name;
    } else {
        customer_data[i]["City"] = null;
    }
}
```
```js
const filteredData = new Mutable(customers_full)
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
// Plot of lat/long and 
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
    Plot.dot(filteredData.filter(d => d.latitude && d.longitude), {
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
<h2>Hover to see Location and Events Purchased<br>Graph displays rows which had latitude and longitude points and places dots labeled with the corresponding event purchase.</h2>
  ${mapv1}
</div>

<div class="card"><h1>Regional Heatmap</h1><h2>Uses same data as above map.  Higher intensity color indicates more data present for that location.</h2>

  <div id="mapv2" style="height: 400px; width: 100%;"></div> 

</div>

```js
const mapv2 = (() => {

  const map = new maplibregl.Map({
    container: 'mapv2',
    style: 'https://tiles.openfreemap.org/styles/bright',
    center: [-96, 37], // center on US 
    zoom: 3
  });
  
  map.addControl(new maplibregl.NavigationControl());
  
  map.on('load', () => {
    // Prepare GeoJSON data
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
          properties: {
            name: d.mr_geo_city_name || 'Unknown Town', 
            event:d.event_purchased||'Unknown',        
            category: d.preferred_main_category || 'Unknown', // add preferred 
            status:d.registration_status|| 'Unknown',
            time:d.visit_time|| 'Unknown'
          }
        }))
    };
    
    // Add source
    map.addSource('customers', {
      type: 'geojson',
      data: geojson
    });
    
    // Heatmap layer
    map.addLayer({
      id: 'customers-heat',
      type: 'heatmap',
      source: 'customers',
      maxzoom: 15,
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
    
    // Circle layer
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

    
    map.on('click', 'customers-point', (e) => {
      const features = map.queryRenderedFeatures(e.point, {
        layers: ['customers-point']
      });
      if (!features.length) return;

      const feature = features[0];
      const { name,event, category,status,time } = feature.properties;

      new maplibregl.Popup()
        .setLngLat(feature.geometry.coordinates)
        .setHTML(`<strong>${name}</strong><br>Event Purchased:${event}<br>Category: ${category}<br>Status:${status}<br>Visit Time: ${time}`)
        .addTo(map);
    });


    map.on('mouseenter', 'customers-point', () => {
      map.getCanvas().style.cursor = 'pointer';
    });
    map.on('mouseleave', 'customers-point', () => {
      map.getCanvas().style.cursor = '';  //asked claude "How to format a mouse click on maplibre using geojson" 
    });

  });

})();

//https://maplibre.org/maplibre-gl-js/docs/API/classes/Popup/
```

<!-- ```js
const mapv2 = (() => {

  const map = new maplibregl.Map({
    container: 'mapv2',
    style: 'https://tiles.openfreemap.org/styles/bright',
    center: [-96, 37], //center on US 
    zoom: 3 //zoomed out 
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
``` -->


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
  .attr("r", d => d.r)
  .style("cursor", "pointer")
  .on("click", e => {
    const bubbleselect = d3.select(e.target).data()[0];
    const chosen_one=bubbleselect.data.name.toLowerCase()
    display(`You just clicked ${bubbleselect.data.name}`)
    filteredData.value = customers_full.filter(d => d.preferred_main_category === chosen_one);
    

  });

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
    .style("pointer-events", "none")
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
<h1>Preferred Main Category</h1><h2>Bubble size changes with count of preferred category.  Each customer can have multiple main categories and so can appear in multiple bubbles, thus the bubbles are not numbered.</h2>
 ${bubbleChart}
</div>

```js
const gettingCurrent_cat = filteredData
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
<h1>Current Category</h1><h2>Shows counts of each current category from the customer data.  Hover each bar to see the applicable category.</h2>
  ${chart}
</div>


```js
const RegistrationArray = Array.from(
  d3.rollup(
    filteredData.filter(d => d.registration_status != null),  
    v => v.length,
    d => d.registration_status
  ),
  ([name, value]) => ({name, value}) 
);
```



```js
const registration_bar = Plot.plot({
  marks: [
    Plot.barY(filteredData.filter(d => d.registration_status != null), 
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



  




