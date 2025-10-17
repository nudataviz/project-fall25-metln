---
title: Time Graphs
---

```js
let customerSum = await FileAttachment("data/customer_summary_clean - customer_summary.csv").csv({typed: true})
let transactSum = await FileAttachment ("data/transactions_clean - transactions.csv").csv({typed: true})
```


```js
/*Updates time of transactions to date/time in the transactionSum array
Unsure why this is updating the original transactSum array too.  all of my googling seems to indicate that this should be a shallow copy
Happy to discuss/review further but it may not even be an issue in this scenario*/

let updatedTransact = Array.from(transactSum)
for (let i = 0; i < updatedTransact.length; i++){
    //Iterates through each object and converts dollar amount strings to numbers
    for (var property in updatedTransact[i]){
        let value = updatedTransact[i][property]
        if (typeof value === 'string' && value.includes("$")){
            //Used Chat GPT, W3 schools, MDN docs to get regEx help and troubleshoot
            updatedTransact[i][property] = parseFloat(value.replace(/[^0-9.-]+/g, '')) 
        }
    }
    //Updates date strings to date values
    updatedTransact[i]["Event Date"] = new Date(updatedTransact[i]["Event Date"])
    updatedTransact[i]["Date"] = new Date(updatedTransact[i]["Date"])

}

//Updates for customer summary, same issue with shallow copy
let updatedCustomers = Array.from(customerSum)
for (let i = 0; i < updatedCustomers.length; i++){
    //Iterates through each object and converts dollar amount strings to numbers
    for (var property in updatedCustomers[i]){
        let value = updatedCustomers[i][property]
        if (typeof value === 'string' && value.includes("$")){
            //Used Chat GPT, W3 schools, MDN docs to get regEx help and troubleshoot
            updatedCustomers[i][property] = parseFloat(value.replace(/[^0-9.-]+/g, '')) 
        }
    }
}
```




```js

//Creating map (dictionary) of total tickets sold per event

let totalTickets = d3.rollup(updatedCustomers, v => d3.sum(v, d => d["Ticket Count"]), d => d["Item Names"])
display(totalTickets)
//Creating array from map, used ChatGPT for assistance
let totalTicketsArray = Array.from(totalTickets, ([key, value]) => ({
  "Item Names": key,
  "Ticket Count": value
}));

let minTickets = view(Inputs.range([0, 300], {step: 1}))

const netSalesPerEvent = Plot.plot({
    title: "Ticket Sales per Event",
    width: 2000,
    height: 1000,
    
    
    marks: [
        Plot.barY(totalTicketsArray.filter(d => d["Ticket Count"] >= 60), {x: "Item Names", y: "Ticket Count"})
    ]
})

display(netSalesPerEvent)
```

```js



//I will create the time of day, date, tickets sold by event type, number of tickets purchased by event type
// dot plot of net earnings vs ticket price or maybe number of tickets sold
// first time attendees
// Value prop is to be able to look at these things by event type or by singular event to advertise to a new vendor
/* Interactive interface where they can see the best selling events in a table
Can then have them select a couple options
    - look at metrics by event type
    - metrics by individual events
Table should should certain stats on the events
    - net earnings
    - total tickets sold
    - price per ticket
    - 
*/
```