---
title: Exploratory Data Analysis
---

```js
let customerSum = await FileAttachment("data/customer_summary_clean.csv").csv({typed: true})
let transactSum = await FileAttachment ("data/transactions_clean.csv").csv({typed: true})
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

```


### Transaction Information
```js
Inputs.table(updatedTransact)
```
---

### Customer Information
```js
Inputs.table(updatedCustomers)
```

---

## Preliminary Ideas
Jotting down some preliminary ideas for data exploration.  Some of these match those provided in the google folder.

- Ticket count by event type (bar graph)
- Ticket count by date (calendar heat map)
- Ticket purchase count by time of day (potential clock heat map)
- Ticket purchase count by day of week (heat map)
- Quantity of tickets purchased by customer per event (could offer insight into ticket buyer demographic (e.g. couples, families, etc.))

- Ticket purchases by gender is "hypothetically" possible although may be difficult algorithmically.  All we have is name info
- Maybe gender (Erin)