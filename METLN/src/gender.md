---
title: Gender Analysis (Can be merged into final - Pryor Prototype)
---

```js
const data = await FileAttachment("data/merged.csv").csv({typed: true})
```
```js
const data_filter=data.filter(d => d.Gender === "M" || d.Gender === "F")
```

```js
Plot.plot({
  color: {legend: true},
  title: 'Ticket Purchased by Event',
  x: {tickRotate: -60}, //this is a mess these are so lengthy
  marginBottom:450,
  marginLeft:150,
  marks: [
    Plot.barY(data_filter, 
      Plot.groupX(
        {y: "count"},
        {x: "Item Names", fill: "Gender"}
      )
    )
  ]
 
})
```