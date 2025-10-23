---
title: Graph Options
---

```js
let transactions = await FileAttachment("/data/transactions_clean - transactions.csv").csv({typed: true})
```


```js
//Creates array from file attachment
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

## All Events
```js

Plot.plot({
    title: "Scatterplot: Time of Purchase",
    marks: [
        Plot.dot(transactionArray, {x: d => new Date(d.Date), y: d => new Date(d.Date).getHours(), stroke: "Item Name", tip: true}),
        Plot.ruleY([5], {label: "Morning"}),
        Plot.ruleY([12], {label: "Afternoon"}),
        Plot.ruleY([18], {label: "Evening"})
    ]
})

```



```js


Plot.plot({
    title: "Time of Purchase: Maine Voices Atsuko Fujimoto and Barak Olins",
    y: {label: "Hour"},
    x: {label: "Day"},
    marks: [
        Plot.dot(transactionArray.filter(d => d["Item Name"] ==  "Maine Voices Live with James Beard Award winners Atsuko Fujimoto and Barak Olins"), {
        x: d => new Date(d.Date),
        y: d => new Date(d.Date).getHours(),
        stroke: "Item Name",
        tip: true})
    ]
})
```


---

```js

Plot.plot({
    title: "Single Event: Morning Sentinel Reader's",
    y: {domain: [0,24]},
    marks: [
        Plot.dot(transactionArray.filter(d => d["Item Name"] == "Morning Sentinel Readers' Choice Awards Ceremony"), {x: d => new Date(d.Date),
        y: d => new Date(d.Date).getHours()})
    ]
})

```

---

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
const updatedTransactions = transactionArray
  .map(d => ({
    //Used chat GPT for help understanding this notation
    ...d,
    timeOfDay: getTimeofDay(d.Date)
  }));

```




```js

Plot.plot({
    title: "Bar of Purchase Times",
    xLabel: "Time of Day",
    yLabel: "Frequency",
    marks: [
        Plot.barY(updatedTransactions.filter(d => d["Item Name"] == "Maine Voices Live with James Beard Award winners Atsuko Fujimoto and Barak Olins"), 
        Plot.groupX({y:"count"}, {x: "timeOfDay"}))
        
    ]
})

```
