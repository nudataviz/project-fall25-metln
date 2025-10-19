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
const  by_event = view(Inputs.select(d3.group(data_filter, d => d["Individual Event"]), {label: "Event"}))

```

```js
Plot.plot({
  title: 'Ticket Purchased by Event',
  marginLeft:150,
  marks: [
    Plot.barY(by_event, 
      Plot.groupX(
        {y: "count"},
        {x: "Gender", fill: "Gender"}
      )
    )
  ]
 
})
```