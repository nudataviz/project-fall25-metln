---
title: Interactive Tables
---


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
    transactionArray[i]["timeOfDay"] = getTimeofDay(transactionArray[i]["Date"])



}

```


```js
/* POTENTIAL ISSUE WITH CODE
For both events and event types, the overarching type is an object with a series of key vals where the vals are events/event types
Ideally, this would be an array for iteration, but the code does not function without.  Need to revisit to make sure nothing is being overlooked.
When changing to an array, it sometimes works but the array is shown as having 0 items. May be a non-issues */
//Creating separate array with details on each individual event
const groupedCategories = {};

for (const customer of customerArray) {
  const event = customer["Event Categories"];

    // Check if event name is in other array
  if (!groupedCategories[event]) {
    groupedCategories[event] = [];
  }

  // Add the customer details under this event
  groupedCategories[event].push(customer);
}

const chosenEvents = {}
for (const row of transactionArray) {
  const singleEvent = row["Item Name"]

  if (!chosenEvents[singleEvent]){
    chosenEvents[singleEvent] = []
  }

  chosenEvents[singleEvent].push(row)
}

```




```js
// Creates array which is displayed within table for viewing pleasure, collates some of the values, graphs calculated separately
const arrayforTable = []
for (const [key, val] of Object.entries(groupedCategories)){
    arrayforTable.push({"Event Type" : key,
                        "Total Tickets" : d3.sum(val, d => d["Ticket Count"]),
                        "Total Sales" : d3.sum(val, d => d["Ticket Total"])

    }
  )

}

```


```js
// Code creates array of objects to use in interactive table
/* A couple important choices
1. Total tickets calculated by a count of rows where the net rev of the transaction was greater than 0
2. Not really sure why the male and female counts are behaving weirdly, the currnet code appears to work, but the code I think should work
e.g. d3.count(val, d => d["Gender"] == "M") does not work
*/
const singleEventTable = []
for (const [key, val] of Object.entries(chosenEvents)){
  singleEventTable.push({"Name" : key,
                        "Total Tickets" : d3.count(val, d => d["Net Revenue"] > 0),
                        "Net Revenue" : d3.sum(val, d => d["Net Revenue"]),
                        "Male Count" : d3.filter(val, d => d["Gender"] == "M").length,
                        "Female Count" : d3.filter(val, d => d["Gender"] == "F").length,
                        "Event Date" : val[0]["Event Date"]
  }
  )
}

```


```js
// May need to revisit here for disallowing multiple row selections, talking point
const search = view(Inputs.search(singleEventTable, {placeholder: "Search events"}));
```
```js
const selection = view(Inputs.table(search, {sort: "Total Tickets", reverse: true, multiple: false}));
```


To-do for gender breakdown:
1. Reactive title
2. Change colors
3. Add total revenue values to bars and maybe percentage
```js
// What is best way to disable error message?  Currently get error when first loading dashboard
// This is becaus
Plot.plot({
  title: 'Gender Breakdown',
  marginLeft:150,
  color: {
    range: ["pink", "blue"]},
  marks: [
    Plot.barY(chosenEvents[selection["Name"]], 
      Plot.groupX(
        {y: "count"},
        {x: "Gender", fill: "Gender"}
      )
    )
  ]
 
})
```


Shows scatterplot of purchases for selected event
Still to-do:
1. Add reactive title so that the event name is also displayed
2. Add some type of markers indicating time of day (thinking maybe coloring the background lightly)
3. Fix red dot to show time of event
4. Change axis labels
```js
// Weird indexing but you can see below how to get to specific event times
// Chosen events is an object, selection["Name"] is an array of transactions all corresponding to one event
Plot.plot({
    title: "Time of Purchase",
    y: {label: "Hour"},
    x: {label: "Day"},
    marks: [
        Plot.dot(chosenEvents[selection["Name"]], {
        x: d => new Date(d.Date),
        y: d => new Date(d.Date).getHours(),
        stroke: "black",
        tip: true}),
        Plot.ruleX([chosenEvents[selection["Name"]][0]["Event Date"]], {stroke: "red", tip: true}),
        Plot.dot([chosenEvents[selection["Name"]][0]["Event Date"]], {stroke: "red"})
    ]
})
```

```js
// data_filter will be the object containing individual transactions
/*Plot.plot({
  padding: 0,
  x: {axis: null},
  y: {tickFormat: Plot.formatMonth("en", "narrow"), tickSize: 0},
  fy: {tickFormat: ""},
  color: {scheme: "PiYG"},
  marks: [
    Plot.cell(chosenEvents[selection["Name"]], {
      x: (d) => d3.utcWeek.count(d3.utcYear(d.Date), d.Date),
      y: (d) => d.Date.getUTCDay(),
      fy: (d) => d.Date.getUTCFullYear(),
      fill: (d, i) => i > 0 ? (d.Close - dji[i - 1].Close) / dji[i - 1].Close : NaN,
      title: (d, i) => i > 0 ? ((d.Close - dji[i - 1].Close) / dji[i - 1].Close * 100).toFixed(1) : NaN,
      inset: 0.5
    })
  ]
})

display(transactionArray.filter(d => d["Item Name"] == "Maine Voices Live with Dr. Nirav Shah"))
//const eventData = (chosenEvents[selection["Name"]])
const eventData = transactionArray.filter(d => d["Item Name"] == "Maine Voices Live with James Beard Award winners Atsuko Fujimoto and Barak Olins")
Plot.plot({
  width: width,
  x: {
    axis: null
  },
  y: {
    tickFormat: i => "SMTWTFS"[i],
    tickSize: 0
  },
  color: {
    scheme: "blues",
    // type: "sqrt"
  },
  facet: {
    data: eventData,
    y: d => d["Date"].getUTCMonth(),
  },
  marks: [
    Plot.frame({stroke: "#ccc"}),
    Plot.cell(eventData, {
      x: d => d3.utcDay.count(d3.utcYear(d["Date"]), d["Date"]),
      y: d => d["Date"].getUTCDay(), 
      fill: "count",
      title: "Calendar",
      inset: 0.5,
    })
  ]
})
*/
```



```js
//I ADDED THE PIE GRAPH WE CAN GO BACK TO BAR
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
//THE NEXT 3 BLOCKS ARE THE TOD PIE CHART 
const tod_pie = Array.from(
  d3.rollup(
    chosenEvents[selection["Name"]],  
    v => v.length,
    d => d.timeOfDay
  ),
  ([name, value]) => ({name, value}) 
);
```

```js
const tod_pie_ordered = [
  tod_pie.find(d => d.name === "Morning"),
  tod_pie.find(d => d.name === "Afternoon"),
  tod_pie.find(d => d.name === "Evening")
].filter(d => d !== undefined);
```

```js

PieChart(tod_pie_ordered, {
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
    const total = d3.sum(tod_pie, p => p.value);
    const percentage = ((d.value / total) * 100).toFixed(1);
    return `${d.name}\n${percentage}%\n${d.value}`;
  }
})

```


```js
const salesByWeek = d3.rollup(
  chosenEvents[selection["Name"]],
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
const salesData = Array.from(salesByWeek, ([week, count]) => ({
  weeksUntil: week,
  ticketsSold: count
})).sort((a, b) => b.weeksUntil - a.weeksUntil);
```
```js
let cumulative = 0;
salesData.forEach(d => {
  cumulative += d.ticketsSold;
  d.cumulativeTickets = cumulative;
});
```

```js
Plot.plot({
  title: "Cumulative Tickets Sold By Week",
  height: 400,
  marks: [
    Plot.lineY(salesData, {
      x: "weeksUntil",
      y: "cumulativeTickets",
      stroke: "steelblue",
      strokeWidth: 2
    }),
    Plot.dot(salesData, {
      x: "weeksUntil",
      y: "cumulativeTickets",
      fill: "steelblue"
    })
  ],
  y: {label: "Tickets Sold"},
  x: {label: "Weeks Before Event", reverse: true}
})
```
