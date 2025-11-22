---
title: Tentative Dashboard
---

```js
/* Summary of variables
transactionArray - basic transformation of data, 1 row per transaction with types converted and additional columns added
chosenEvents - object with key : val pairs. key = event name, val = all rows from transactionArray for that event
singleEventTable - array which is displayed in the interactive table, contains calculations for gender distribution, total tickets, total rev, and event date
genderCounts - map of gender for all selected events
pie_array - array for usage in gender pie chart
iterable_array - interim array, contains a slice of the singleEventTable reactively based table selection
specificTransacts - filtered version of transactionArray that reactively updates based on table selection, 1 row per transaction with all same fields
*/
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
// NPM library for detecting gender from a name
import { getGender } from "gender-detection-from-name";
const gender_guesser = getGender;
```

```js

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
    transactionArray[i]["Gender"] = gender_guesser(transactionArray[i]["First Name"])



}
```



```js
/* POTENTIAL ISSUE WITH CODE
For both events and event types, the overarching type is an object with a series of key vals where the vals are events/event types
Ideally, this would be an array for iteration, but the code does not function without.  Need to revisit to make sure nothing is being overlooked.
When changing to an array, it sometimes works but the array is shown as having 0 items. May be a non-issues */
//Below code creates an object with key : val pairs where each key is an event name, val = an array with each transaction for that event

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
// Code creates array of objects to use in interactive table
/* A couple important choices
1. Total tickets calculated by a count of rows where the net rev of the transaction was greater than 0
2. Not really sure why the male and female counts are behaving weirdly, the currnet code appears to work, but the code I think should work
e.g. d3.count(val, d => d["Gender"] == "M") does not work
*/
const singleEventTable = []
for (const [key, val] of Object.entries(chosenEvents)){
  singleEventTable.push({"Name" : key,
                        "Tickets" : d3.count(val, d => d["Net Revenue"] > 0),
                        "Net Revenue" : d3.sum(val, d => d["Net Revenue"]),
                        "Male Count" : d3.filter(val, d => d["Gender"] == "male").length,
                        "Female Count" : d3.filter(val, d => d["Gender"] == "female").length,
                        "Event Date" : val[0]["Event Date"],
  }
  )
}

```

```js
//Next few code blocks are used for gender pie
let data=specificTransacts

```

```js
//Excludes unknown gender from selection
const data_filter=data.filter(d => d.Gender === "male" || d.Gender === "female")
```

```js
//Calculates count of each gender
const genderCounts = d3.rollup(
  data_filter,
  v => v.length,
  d => d.Gender
)
//Creates array from counts for plotting
const pie_array = Array.from(genderCounts, ([gender, count]) => ({
  name: gender,
  value: count
}));
```


```js
// Removing final object from array
// this array is for the gender graph
const iterableArray = selection.slice(0, selection.length)
```

```js
/* Code creates an array for bar graph
Believe not necessary because we are opting for pie chart
const genderArray = [{Gender: "Male", Count: d3.sum(iterableArray, d => d["Male Count"])},
                     {Gender: "Female", Count: d3.sum(iterableArray, d => d["Female Count"])}]
                     */
```

```js
/* Commenting out bar chart, can revisit if we want it or remove before submitting to METLN
Plot.plot({
  title: 'Gender Breakdown',
  marginLeft:150,
  color: {
    range: ["pink", "blue"]},
  marks: [
    Plot.barY(genderArray, {
              x: "Gender",
              y: "Count",
              fill: "Gender"
    })
  ]

})
*/
```


```js
/* Commenting out scatterplot in body of md, can likely remove
// Weird indexing but you can see below how to get to specific event times
// Chosen events is an object, selection["Name"] is an array of transactions all corresponding to one event
Plot.plot({
    title: "Time of Purchase",
    y: {label: "Hour"},
    x: {label: "Day"},
    marks: [
        Plot.dot(specificTransacts, {
        x: d => new Date(d.Date),
        y: d => new Date(d.Date).getHours(),
        stroke: "Item Name",
        tip: true}),
    ]
})
*/
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
// Function for creating a pie chart
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
// Creating separate array just to log names of checkboxed items
const selectedNames = []
for (const event of iterableArray){
    if (!(event["Name"] in selectedNames)){
          selectedNames.push(event["Name"])
    }
}
```

```js
//Creating array that just contains transaction details for the selected events
//Should be used for the pie chart and other graphs
const specificTransacts = transactionArray.filter(d => selectedNames.includes(d["Item Name"]))
```


```js
// Calculating total revenue of each morning, afternoon, and evening for the selected events
// Should be able to support differing ticket prices
const morningRev = d3.sum(specificTransacts.filter(d => d.timeOfDay == "Morning"), rev => rev["Gross Revenue"])
const afternoonRev = d3.sum(specificTransacts.filter(d => d.timeOfDay == "Afternoon"), rev => rev["Gross Revenue"])
const eveningRev = d3.sum(specificTransacts.filter(d => d.timeOfDay == "Evening"), rev => rev["Gross Revenue"])
```

```js
//THE NEXT 3 BLOCKS ARE THE TOD PIE CHART 
const tod_pie = Array.from(
  d3.rollup(
    //Updated data value to support multi select
    specificTransacts,
    //chosenEvents[selection["Name"]],  
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
/* Commenting out pie chart directlt on the page.  Pie chart is added later to the dashboard
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
*/
```


```js
// Cumulative graph for the weeks leading up to an event for all selected events
// Does not use dates but instead uses a measure of how far out from the event the ticket purchase is
const salesByWeek = d3.rollup(
  specificTransacts,
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
```

```js
// Updates salesData cumulative values to be cumululative
let cumulative = 0;
salesData.forEach(d => {
  cumulative += d.ticketsSold;
  d.cumulativeTickets = cumulative;
});
```

```js
/* Commenting out cumulative ticketr graph that is outside dashboard
Plot.plot({
  title: "Cumulative Tickets Sold By Week",
  height: 400,
  marks: [
    Plot.lineY(salesData, {
      x: "weeksUntil",
      y: "cumulativeTickets",
      stroke: "steelblue",
      strokeWidth: 2,
      tip: true
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
*/
```

```js
// Attempting to create async inputs for formatting in css
const userInput = Inputs.search(singleEventTable, {placeholder: "Search events"})
const search = Generators.input(userInput)
```
```js
const eventInput = Inputs.table(search, {sort: "Tickets", reverse: true, layout: "auto"})
const selection = Generators.input(eventInput);
```

```js
// Code for reactive title of all graphs
let allChosenEvents = "Event Summary for "

for (let i = 0; i < selectedNames.length; i++){
  allChosenEvents += selectedNames[0]
  
}


```

```js
const total = d3.sum(tod_pie, p => p.value)
```


<div class="grid grid-cols-3" style="grid-auto-rows: auto;">
  <div class="card grid-colspan-3"><h1>Events</h1>
    ${userInput}
    ${eventInput} 
  </div>
  <div class="card grid-colspan-3 grid-rowspan-1"><h1>Event(s) Summary<h1> </div>
  <div class="card grid-colspan-2 grid-rowspan-2"><h1>Gender of Ticket Buyers</h1>
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
    }})}
  </div>
  <div class="card grid-colspan-1 grid-rowspan-1" style="background-color:#89CFF0"><h1>Male</h1>
    Proof of concept
    Can place total revenue for gender here but this leaves a lot of white space<br>
    Still brainstorming other options
  </div>
  <div class="card grid-colspan-1" style="background-color:#FFB7CE"><h1>Female</h1>
    Same as for male
  </div>
  <div class="card grid-colspan-2 grid-rowspan-3"><h1>Total Tickets Sold by Time of Day</h1>
    ${PieChart(tod_pie_ordered, {
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
      return `${d.name}\n${percentage}%\n${d.value}`;}
    })}
  </div>
  <div class="card grid-rowspan-1" style="background-color: #ffd725ff;"><h1>Morning</h1>
    5 am - 12 pm<br>
    $${morningRev} in net sales
  </div>
  <div class="card grid-rowspan-1" style="background-color: #e78a19ff;"><h1>Afternoon</h1>
    12:01 pm - 5:59 pm<br>
    $${afternoonRev} in net sales
  </div>
  <div class="card grid-rowspan-1" style="background-color: #5955d3ff;"><h1>Evening</h1>
    6:00 pm - 4:59 am<br>
    $${eveningRev} in net sales
  </div>
  <div class="card grid-rowspan-2 grid-colspan-3"><h1>Cumulative Tickets Sold by Week</h1>
    ${Plot.plot({
    height: 400,
    marks: [
      Plot.lineY(salesData, {
        x: "weeksUntil",
        y: "cumulativeTickets",
        stroke: "steelblue",
        strokeWidth: 2,
        tip: true
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
    }
  </div>
  <div class ="card grid-rowspan-2 grid-colspan-3"><h1></h1>
  ${Plot.plot({
    title: "Time of Purchase",
    y: {label: "Hour"},
    x: {label: "Day"},
    marks: [
        Plot.dot(specificTransacts, {
        x: d => new Date(d.Date),
        y: d => new Date(d.Date).getHours(),
        stroke: "Item Name",
        tip: true}),
    ]
    })}
    </div>
</div>