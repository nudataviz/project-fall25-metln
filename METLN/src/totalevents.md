---
title: All Event Overview
---
# Demographics Across Events

When taking all events into account we can see who is buying 
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
import { getGender } from "gender-detection-from-name";
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
  const height = Math.min(width, 550);
  const radius = Math.min(width, height) / 2;

  const arc = d3.arc()
      .innerRadius(radius * 0.67)
      .outerRadius(radius - 1);

  const order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  data_dow.sort((a, b) => order.indexOf(a.name) - order.indexOf(b.name));

  const color = d3.scaleOrdinal()
      .domain(order)
      .range(["#ffd725", "#e78a19", "#5955d3", "#ff6b6b", "#4ecdc4", "#95e1d3", "#f38181"]);

  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [-width / 2, -height / 2, width, height / 2])
      .attr("style", "max-width: 100%; height: auto;");

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
      .attr("font-size", 12)
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

      //.call(text => text.filter(d => (d.endAngle - d.startAngle) > 0.25)
          //.append("tspan")
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
```html
<div class="grid grid-cols-2" style="grid-auto-rows: auto;">
  <div class="card">
    <h2>Who is Buying?</h2>
    <h3>Names are guessed using gender-detection-from-name — some room for error here</h3>
    ${PieChart(pie_array, {
      name: d => d.name,
      value: d => d.value,
      width: 500,
      height: 400,
      colors: ["blue", "lavender"],
      labelRadius: 90,
      title: (d) => {
        const total = d3.sum(pie_array, p => p.value);
        const percentage = ((d.value / total) * 100).toFixed(1);
        return `${d.name}\n${percentage}%\n${d.value}`;
      }
    })}
  </div>

  <div class="card">
    <h2>When Are they Buying</h2>
    <h3>Morning: Before 12p; Afternoon: 12p-6p; Evening: After 6pm<h3>
    ${PieChart(tod_pie, {
  name: d => d.name,
  value: d => d.value,
  width: 500,
  height: 400,
  colors: ["#ffd725ff", "#e78a19ff", "#5955d3ff"],
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

<div class="card" style="grid-column: span 2; padding: 0 0.5rem; min-height: 0; max-height: 450px;">
    <h2>What Day of the week are you most likely to get a response</h2>
    ${chart_dow()}
</div>
```
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