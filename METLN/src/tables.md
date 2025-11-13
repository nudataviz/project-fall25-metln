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
/*  Code is for time of day bar graphs need to add accessory function to calculate morning, afternoon, night. May use the graphs Erin created instead, probably a better idea.
Plot.plot({
    title: "Bar of Purchase Times",
    xLabel: "Time of Day",
    yLabel: "Frequency",
    marks: [
        Plot.barY(chosenEvents[selection["Name"]], Plot.groupX({y:"count"}, {x: "timeOfDay"})){y: "count"}), 
        
    ]
})
*/
```