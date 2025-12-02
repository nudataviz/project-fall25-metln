---
title: Total Event Overview
---
# Who & When
## Overview Across All Events

Visualizations on this page draw from transaction data to highlight purchase dates, times, and client demographics. To see this data for indiviudal events please head to the event table in <a href="./tables">Selected Events</a>

These charts are intended to provide a high-level overview, helping you quickly identify broad patterns and emerging trends across all events.

```js
//need to download npm i gender-detection-from-name
```

```js
let customers = await FileAttachment("/data/customer_summary_clean.csv").csv({typed: true})
```

```js
let transactions = await FileAttachment("/data/cleaned_transaction.csv").csv({typed: true})
```
```js
const formatDay = d3.timeFormat("%A");

```


```js
import { getGender } from "npm:gender-detection-from-name";
const gender_guesser = getGender;
```
```js
//Function for identifying time of day for transaction
function getTimeofDay(dateVal){
    let hour = dateVal.getHours()
    
    if (hour <= 12){
        return "Morning"
    }
    if (hour > 12 && hour < 18){
        return "Afternoon"
    }
    return "Evening"
}
```
```js
//Creates array from file attachment
let customerArray = Array.from(customers)
for (let i = 0; i < customerArray.length; i++){
    //Iterates through each object and converts dollar amount strings to numbers
    for (var property in customerArray[i]){
        let value = customerArray[i][property]
        if (typeof value === 'string' && value.includes("$")){
            //Used Chat GPT, W3 schools, MDN docs to get regEx help and troubleshoot
            customerArray[i][property] = parseFloat(value.replace(/[^0-9.-]+/g, '')) 
        }
    }

}

let transactionArray = Array.from(transactions)
for (let i = 0; i < transactionArray.length; i++){
    //Iterates through each object and converts dollar amount strings to numbers
    for (var property in transactionArray[i]){
        let value = transactionArray[i][property]
        if (typeof value === 'string' && value.includes("$")){
            //Used Chat GPT, W3 schools, MDN docs to get regEx help and troubleshoot
            transactionArray[i][property] = parseFloat(value.replace(/[^0-9.-]+/g, '')) 
        }
    }

    //Updates date strings to date values
    transactionArray[i]["Event Date"] = new Date(transactionArray[i]["Event Date"])
    transactionArray[i]["Date"] = new Date(transactionArray[i]["Date"])
    transactionArray[i]["Day_Of_Week"] = formatDay(transactionArray[i]["Date"])
    transactionArray[i]["Gender"] = gender_guesser(transactionArray[i]["First Name"])
    transactionArray[i]["timeOfDay"] = getTimeofDay(transactionArray[i]["Date"])
    transactionArray[i]["Season"] = getSeason(transactionArray[i]["Event Date"])


}

```

```js
function getSeason(dateVal){
  const month = dateVal.getMonth()
  let season = null
  if (month == 0 || month == 1 || month == 2){
    season = "Winter"
  }
  else if (month == 2 || month == 3 || month == 4){
    season = "Spring"
  }
  else if (month == 5 || month == 6 || month == 7){
    season = "Summer"
  }
  else if (month == 8 || month == 9 || month == 10){
    season = "Autumn"
  }
  return season
}
```

```js
let data=transactionArray

```

```js
const data_filter=data.filter(d => d.Gender === "male" || d.Gender === "female")
```

```js
const genderCounts = d3.rollup(
  data_filter,
  v => v.length,
  d => d.Gender
);

const pie_array = Array.from(genderCounts, ([gender, count]) => ({
  name: gender,
  value: count
}));
```

```js
const tod_pie = Array.from(
  d3.rollup(
    data,  
    v => v.length,
    d => d.timeOfDay
  ),
  ([name, value]) => ({name, value}) 
);
```

```js
const transaction_array_dow = Array.from(
  d3.rollup(
    transactionArray,  
    v => v.length,
    d => d.Day_Of_Week
  ),
  ([name, value]) => ({name, value}) 
);
```

```js
let data_dow=transaction_array_dow
```


```js
// Adds the DOW the event occurs to the array
// Used to show what day of week the events are occuring
const days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];

const dataWithDay = transactionArray.map(d => ({
  ...d,
  day: days[d["Event Date"].getDay()]
}));

```

```js
// Separate rollup for the event DOW bubble chart
//const eventDOW = Array.from(d3.rollup(dataWithDay, v => v.length, d=> d["Item Name"]), ([name, count]) => ({name, count}))
```


```js
// data wrangling to 
const dayEventCount = {Sunday : 0, Monday : 0, Tuesday: 0, Wednesday: 0, Thursday:0, Friday:0, Saturday:0}
const setOfEvents = new Set()
for (const row of dataWithDay){
  if (!setOfEvents.has(row["Item Name"])){
    setOfEvents.add(row["Item Name"])
    dayEventCount[row["day"]] += 1
  }
}
```

```js
// Used in bubblechart for event counts for each DOW
const numEventsperDOW = Object.entries(dayEventCount).map(([day, count]) => ({
  Name: day,
  count: count
}));
```





```js
// Copyright 2021-2023 Observable, Inc.
// Released under the ISC license.
// https://observablehq.com/@d3/bubble-chart
function BubbleChart(data, {
  name = ([x]) => x, // alias for label
  label = name, // given d in data, returns text to display on the bubble
  value = ([, y]) => y, // given d in data, returns a quantitative size
  group, // given d in data, returns a categorical value for color
  title, // given d in data, returns text to show on hover
  link, // given a node d, its link (if any)
  linkTarget = "_blank", // the target attribute for links, if any
  width = 640, // outer width, in pixels
  height = width, // outer height, in pixels
  padding = 3, // padding between circles
  margin = 1, // default margins
  marginTop = margin, // top margin, in pixels
  marginRight = margin, // right margin, in pixels
  marginBottom = margin, // bottom margin, in pixels
  marginLeft = margin, // left margin, in pixels
  groups, // array of group names (the domain of the color scale)
  colors = d3.scaleOrdinal(d3.schemeAccent), // an array of colors (for groups), changed val to match dash
  fill = "#ccc", // a static fill color, if no group channel is specified
  fillOpacity = 0.7, // the fill opacity of the bubbles
  stroke, // a static stroke around the bubbles
  strokeWidth, // the stroke width around the bubbles, if any
  strokeOpacity, // the stroke opacity around the bubbles, if any
} = {}) {
  // Compute the values.
  const D = d3.map(data, d => d);
  const V = d3.map(data, value);
  const G = group == null ? null : d3.map(data, group);
  const I = d3.range(V.length).filter(i => V[i] > 0);

  // Unique the groups.
  if (G && groups === undefined) groups = I.map(i => G[i]);
  groups = G && new d3.InternSet(groups);

  // Construct scales.
  const color = G && d3.scaleOrdinal(groups, colors);

  // Compute labels and titles.
  const L = label == null ? null : d3.map(data, label);
  const T = title === undefined ? L : title == null ? null : d3.map(data, title);

  // Compute layout: create a 1-deep hierarchy, and pack it.
  const root = d3.pack()
      .size([width - marginLeft - marginRight, height - marginTop - marginBottom])
      .padding(padding)
    (d3.hierarchy({children: I})
      .sum(i => V[i]));

  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [-marginLeft, -marginTop, width, height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;")
      .attr("fill", "currentColor")
      .attr("font-size", 30)
      .attr("font-family", "sans-serif")
      .attr("text-anchor", "middle");

  const leaf = svg.selectAll("a")
    .data(root.leaves())
    .join("a")
      .attr("xlink:href", link == null ? null : (d, i) => link(D[d.data], i, data))
      .attr("target", link == null ? null : linkTarget)
      .attr("transform", d => `translate(${d.x},${d.y})`);

  leaf.append("circle")
      .attr("stroke", stroke)
      .attr("stroke-width", strokeWidth)
      .attr("stroke-opacity", strokeOpacity)
      .attr("fill", G ? d => color(G[d.data]) : fill == null ? "none" : fill)
      .attr("fill-opacity", fillOpacity)
      .attr("r", d => d.r);

  if (T) leaf.append("title")
      .text(d => T[d.data]);

  if (L) {
    // A unique identifier for clip paths (to avoid conflicts).
    const uid = `O-${Math.random().toString(16).slice(2)}`;

    leaf.append("clipPath")
        .attr("id", d => `${uid}-clip-${d.data}`)
      .append("circle")
        .attr("r", d => d.r);

    leaf.append("text")
        .attr("clip-path", d => `url(${new URL(`#${uid}-clip-${d.data}`, location)})`)
      .selectAll("tspan")
      .data(d => `${L[d.data]}`.split(/\n/g))
      .join("tspan")
        .attr("x", 0)
        .attr("y", (d, i, D) => `${i - D.length / 2 + 0.85}em`)
        .attr("fill-opacity", (d, i, D) => i === D.length - 1 ? 0.7 : null)
        .text(d => d);
  }

  return Object.assign(svg.node(), {scales: {color}});
}
```

```js
//Defining color map to match colors across DOW charts
// Any changes to these colors should also be made to the pie chart call to make sure day colors align
const colorMap = {
  Sunday:  "#4CBF70",
  Monday: "#FF6F61",
  Tuesday: "#7FCECC",
  Wednesday: "#C985FF",
  Thursday: "#B4D96A",
  Friday: "#FF9F4A",
  Saturday: "#6E89FF"
};
```
```js
// Function call for bubblechart, uses same color
const bubbles = BubbleChart(numEventsperDOW, {
  label: d => `${d.Name}\n${d.count}`,
  value: d => d.count,
  group: d => d.Name,
  
  // Correct alignment:
  groups: Object.keys(colorMap),
  colors: Object.values(colorMap)
});

```


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
function chart_dow() {
  const chartHeight = 280; 
  const chartWidth = Math.min(width, 700);
  const radius = Math.min(chartWidth, chartHeight * 2) / 2;

  const arc = d3.arc()
      .innerRadius(radius * 0.67)
      .outerRadius(radius - 1);

  const order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  data_dow.sort((a, b) => order.indexOf(a.name) - order.indexOf(b.name));

  const color = d3.scaleOrdinal()
      .domain(order)
      .range(["#4CBF70", "#FF6F61", "#7FCECC", "#C985FF", "#B4D96A", "#FF9F4A", "#6E89FF"]);

  const svg = d3.create("svg")
      .attr("width", chartWidth)
      .attr("height", chartHeight)
      .attr("viewBox", [-chartWidth / 2, -radius, chartWidth, radius + 20]) //changed this to fit on a page
      .attr("style", "max-width: 100%; height: auto; display: block;");

  svg.append("g")
    .selectAll()
    .data(pie_dow(data_dow))
    .join("path")
      .attr("fill", d => color(d.data.name))
      .attr("d", arc)
    .append("title")
      .text(d => `${d.data.name}: ${d.data.value.toLocaleString()}`);

  svg.append("g")
      .attr("font-family", "sans-serif")
      .attr("font-size", 14)
      .attr("text-anchor", "middle")
    .selectAll()
    .data(pie_dow(data_dow))
    .join("text")
      .attr("transform", d => `translate(${arc.centroid(d)})`)
      .call(text => text.append("tspan")
          .attr("y", "-0.4em")
          .attr("font-weight", "bold")
          .text(d => d.data.name))
      .call(text => text.append("tspan")
          .attr("x", 0)
          .attr("y", "0.7em")
          .attr("fill-opacity", 0.7)
          .text(d => d.data.value.toLocaleString("en-US")));

  return svg.node();
}
```


```js
const height = Math.min(width, 700);
const radius = Math.min(width, height) / 2;

const pie_dow = d3.pie()
    .padAngle(1 / radius)
    .sort(null)
    .value(d => d.value)
    .startAngle(-Math.PI / 2)
    .endAngle(Math.PI / 2);
```

```js
// Used for season chart
const aggregated = Array.from(
  d3.rollup(
    transactionArray,
    v => v.length, 
    d => d.Season,
    d => d["Item Name"]
  ),
  ([Season, eventMap]) =>
    Array.from(eventMap, ([Event, Tickets]) => ({
      Season,
      Event,
      Tickets
    }))
).flat();
```

```js
// Cumulative graph for the weeks leading up to an event for all selected events
// Does not use dates but instead uses a measure of how far out from the event the ticket purchase is
const salesByWeek = d3.rollup(
  transactionArray,
  v => v.length, // count tickets
  d => {
    const eventDate = new Date(d["Event Date"]);
    const purchaseDate = new Date(d.Date);
    const daysUntil = Math.floor((eventDate - purchaseDate) / (1000 * 60 * 60 * 24));
    const weeksUntil = Math.floor(daysUntil / 7);
    return weeksUntil;
  }
);
```
```js
// Array with weeks until event date, tickets sold that week, and total tickets sold
const salesData = Array.from(salesByWeek, ([week, count]) => ({
  weeksUntil: week,
  ticketsSold: count
})).sort((a, b) => b.weeksUntil - a.weeksUntil);

// Updates salesData cumulative values to be cumululative
let cumulative = 0;
salesData.forEach(d => {
  cumulative += d.ticketsSold;
  d.cumulativeTickets = cumulative;
});
```

<!-- ```js
const reactiveSales = salesData.filter(d => d["weeksUntil"] <= userWeeks)
```

```js
const salesDataInput = Inputs.range([1, d3.max(salesData, d => d.weeksUntil)], {step: 1, label: "Weeks Until Event", placeholder: 30})
const userWeeks = Generators.input(salesDataInput)
``` -->

```js
// Uses above inputs
const cumulativeTicketsSold = Plot.plot({
    height: 400,
    width: 860,
    x: {label: "Weeks Before Event", 
      reverse: true,
      domain: salesData.slice(-10).map(d => d.weeksUntil)},
    marks: [
      Plot.lineY(salesData.slice(-10), {
        x: "weeksUntil",
        y: "cumulativeTickets",
        stroke: "steelblue",
        strokeWidth: 2,
        tip: true
      }),
      Plot.dot(salesData.slice(-10), {
        x: "weeksUntil",
        y: "cumulativeTickets",
        fill: "steelblue"
      }),
      Plot.gridX({strokeDasharray: "5,3"}),
      Plot.gridY({strokeDasharray: "5,3"})
    ],
    y: {label: "Tickets Sold"},
    x: {label: "Weeks Before Event", reverse: true}
    })
    
```
```js
const seasonBar = Plot.plot({
    height: 500,
    style: {fontSize: "20px"},
  x: {label: "", style: {size: 20}},
  color :{scheme: "set3"},
  marks: [
  Plot.barY(aggregated, {x: "Season", y:"Tickets", fill: "Event", tip: true}),
  Plot.axisY({interval: 40})
  ]
  })
```

```js
display(seasonBar)
```

<style>
@media print {
  .grid {
    break-inside: avoid;
    page-break-inside: avoid;
  }

  .card {
    break-inside: avoid !important;
    page-break-inside: avoid !important;
    -webkit-column-break-inside: avoid !important;
    box-decoration-break: clone;
    margin-bottom: 12px;
  }
}
</style>

<div class="grid grid-cols-2" style="grid-auto-rows: auto;">
  <div class="card">
    <h1>Who is Buying?</h1>
    <h2>Gender distribution based on customer name.<br>Some error expected.</h2>
    ${PieChart(pie_array, {
      name: d => d.name,
      value: d => d.value,
      width: 500,
      height: 400,
      colors: ["#89CFF0", "#FFB7CE"],
      labelRadius: 90,
      title: (d) => {
        const total = d3.sum(pie_array, p => p.value);
        const percentage = ((d.value / total) * 100).toFixed(1);
        return `${d.name}\n${percentage}%\n${d.value}`;
      }
    })}
  </div>

  <div class="card">
    <h1>What Time?</h1>
    <h2>Morning: Before 12:00 pm<br> Afternoon: 12:00 pm - 6:00 pm<br> Evening: After 6:00 pm<h2>
  ${PieChart(tod_pie, {
  name: d => d.name,
  value: d => d.value,
  width: 500,
  height: 400,
  colors: ["#FFE86A",  "#9895C9", "#E9A33A"],
  labelRadius: 90,
  startAngle: -Math.PI / 2,
  endAngle: Math.PI / 2,
  innerRadius: 0,
  title: (d) => {
    const total = d3.sum(tod_pie, p => p.value); // make sure tod_pie exists here
    const percentage = ((d.value / total) * 100).toFixed(1);
    return `${d.name}\n${percentage}%\n${d.value}`;
  }
})}
  </div>

<div class="card" style="grid-column: span 2">
    <h1>What Day?</h1>
    <h2>Distribution of ticket sales by the day of week they were purchased.</h2>
    ${chart_dow()}

</div>
<div class="card" style="grid-column: span 1">
  <h1> When are the events being held? </h1> <h2>Bubble size represents number of events held on that day.  Event counts included.</h2>
  ${bubbles}

</div>
<div class="card"><h1>What season?</h1>
<h2>Total number of events for each season.  Stacked bar further shows number of tickets per event.<br><br>
  <b>Winter: ${aggregated.filter(d => d["Season"] == "Winter").length} events.</b><br>
    <b>Spring: ${aggregated.filter(d => d["Season"] == "Spring").length} events.</b><br>
    <b>Summer: ${aggregated.filter(d => d["Season"] == "Summer").length} events.<br>
    Autumn: ${aggregated.filter(d => d["Season"] == "Autumn").length} events.</b><br>
    <br>
  ${seasonBar}
</div>
<div class="card grid-rowspan-2 grid-colspan-3"" style="grid-column: span 2">
  <h1>How far in advance?</h1>
  <h2>This shows how many weeks in advance tickets are purchased</h2>
 
  ${cumulativeTicketsSold}
</div>

```js

htl.html`<button onclick="window.print()" style="padding: 10px 20px; background: #487eb7ff; color: white; border: none; border-radius: 5px; cursor: pointer; margin: 20px 0;">
Print/Save as PDF
</button>`

```
```js
{
  const button = document.getElementById("print-button");
  if (button) {
    button.addEventListener("click", () => {
      window.print();
    });
  }
}
```

```js
/*${Plot.plot({
  marks:[
    Plot.barY(dataWithDay, Plot.groupX({y:"count"}, {x: "day"}))
  ]
})}*/
```
