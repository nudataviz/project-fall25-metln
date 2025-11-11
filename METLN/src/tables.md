---
title: Interactive Tables
---

```js
```

```js
let customers = await FileAttachment("/data/customer_summary_clean.csv").csv({typed: true})
```

```js
let transactions = await FileAttachment("/data/cleaned_transaction.csv").csv({typed: true})
```

Queries to standardize inputs
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

}


```

Customer array
```js
display(customerArray)
```
Transaction array
```js
display(transactionArray)
```


Grouped Categories/Keys
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

display(groupedCategories)
display(Object.keys(groupedCategories))
```

Grouped By Single Event
```js
display(chosenEvents)
display(Object.keys(chosenEvents))
```




Should show arrayforTable
```js
const arrayforTable = []
for (const [key, val] of Object.entries(groupedCategories)){
    arrayforTable.push({"Event Type" : key,
                        "Total Tickets" : d3.sum(val, d => d["Ticket Count"]),
                        "Total Sales" : d3.sum(val, d => d["Ticket Total"])

    }
  )

}
display(arrayforTable)
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
                        "Female Count" : d3.filter(val, d => d["Gender"] == "F").length
  }
  )
}

```


```js
// May need to revisit here for disallowing multiple row selections, talking point
const search = view(Inputs.search(singleEventTable, {placeholder: "Search events"}));
```
```js
const selection = view(Inputs.table(search));
```

```js
display(selection)
```