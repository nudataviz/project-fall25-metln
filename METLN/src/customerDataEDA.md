---
title: New Customer Data
---

```js
let cleanedData =  await FileAttachment("/data/Event_Purchaser_2025-11-10T1531_CLEAN - Event_Purchaser_2025-11-10T1531.csv").csv({typed: true})

```


```js
const utmcontentTypes = []

for (const row of cleanedData){
    if (!(utmcontentTypes.includes(row["utm_content"]))){
        utmcontentTypes.push(row["utm_content"])
    }
}
```



```js
const utmSources = []

for (const row of cleanedData){
    if (!(utmSources.includes(row["utm_source"]))){
        utmSources.push(row["utm_source"])
    }
}
```


```js
// Graph showing number of customers with specific content types
// Should also show engagement score?
//

const uniqueutmSources = new Set()

for (const row of utmSources){
    if (row === null){
        uniqueutmSources.add(null)
    }
    else {
        const sources = row.split(";")
        for (const item of sources){
            uniqueutmSources.add(item)
        }
    }
}
```



```js
const utmMediums = []

for (const row of cleanedData){
    if (!(utmMediums.includes(row["utm_medium"]))){
        utmMediums.push(row["utm_medium"])
    }
}
```




Engagement Scores
```js
const engagementScores = []
for (const row of cleanedData){
    if (!(engagementScores.includes(row["engagement_score"])))
    engagementScores.push(row["engagement_score"])
}
```

```js
display(engagementScores)
```

```js
Plot.plot({
    marks: [
        Plot.boxY(cleanedData, {x:"engagement", y:"engagement_score", tip:true})
    ]
})
```

```js
const engagementBar = [{"Category" :"High", "Count" : cleanedData.filter(d => d["engagement"] == "high").length},
                        {"Category" : "Medium", "Count" : cleanedData.filter(d => d["engagement"] == "medium").length},
                        {"Category" : "Low", "Count": cleanedData.filter(d => d["engagement"] == "low").length},
                        {"Category" :"Null", "Count": cleanedData.filter(d => d["engagement"] === null).length}]
```

Shows the number of customers in each engagement category.
May need to swap to % of total number of customers so can be compared with the other graph about revenue based off event category.
```js
Plot.plot({
    marks: [
        Plot.barY(engagementBar, {x: "Category", y:"Count", tip:true})
    ]
})

```

```js
const eventSpending = []
for (const row of cleanedData){
    if (!(eventSpending.includes(row["event_purchased_amount"])))
    eventSpending.push(row["event_purchased_amount"])
}
```

```js
const uniqueEvents = new Set()
for (const row of cleanedData){
    uniqueEvents.add(row["event_purchased"])
}
```




Comparing Amount Spent on Events with Engagement Level
```js
display(d3.count(cleanedData, d => d["event_purchased_amount"]))
```
```js
// Setting this variable as the boxplot did not identify amounts sold above like 200 as outliers.
const boxData = cleanedData.filter(d => d["event_purchased_amount"] < 200)
```

Graph shows that mean expenditure is the same across engagement categories.
May not be useful depending on definition for each category.
```js
Plot.plot({
    marks:[
        Plot.boxY(boxData, {x: "engagement", y:"event_purchased_amount", tip: true})
    ]
})
```

Total Spending per Engagement Level
```js

for (const row of cleanedData){

}
const totalSpendingBar = [{"Category" : "High", "Total Revenue": d3.sum(cleanedData.filter(d => d["engagement"] == "high"), d => d["event_purchased_amount"]), "Total Customers": d3.filter(cleanedData, d => d["engagement"] == "high").length},
                          {"Category" : "Medium", "Total Revenue": d3.sum(cleanedData.filter(d => d["engagement"] == "medium"), d => d["event_purchased_amount"]), "Total Customers": d3.filter(cleanedData, d => d["engagement"] == "medium").length},
                          {"Category" : "Low", "Total Revenue": d3.sum(cleanedData.filter(d => d["engagement"] == "low"), d => d["event_purchased_amount"]), "Total Customers": d3.filter(cleanedData, d => d["engagement"] == "low").length},
                          {"Category" : "Null", "Total Revenue": d3.sum(cleanedData.filter(d => d["engagement"] === null), d => d["event_purchased_amount"]), "Total Customers": d3.filter(cleanedData, d => d["engagement"] === null).length}]
// repeat customers are those with event_purchased.split(;).length > 1

for (const cat of totalSpendingBar){
    cat["Revenue / Customer"] = cat["Total Revenue"] / cat["Total Customers"]
    }

```


```js
display(cleanedData)
```

Bar Chart of total amount made off of different engagement groups
May be useful depending on definition of "null" engagement vals.  May also be useful for fill options.  Had trouble with striations rather than the things appearing as a block
```js
Plot.plot({
    marks:[
        Plot.barY(cleanedData, {x:"engagement", y: "event_purchased_amount", fill: "preferred_main_category", tip:true, order:"preferred_main_category"})
    ]
})
```

Add cell heatmap for some of the utm vals.
```js
display(cleanedData)
```

```js
Plot.plot({
    marks:[
        Plot.cell(cleanedData, {x: "})
    ]
})
```