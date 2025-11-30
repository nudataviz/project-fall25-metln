# Visualization for Maine Trust for Local News

This project took data supplied by the [Maine Trust for Local News](https://www.metln.org/) to look at both information from indiviual events, common trends across all events as well as a customer overview. 
Many of these graphs are dynamic in nature so we recommend launching the obvservable webpage on your local machine by following the [instructions on how to run](#how-to-run) if you have the proper data.

## All Events Trends 

To get a general sense of who is buying interacting with the webpages we can look at the entire customer database. That will give us a sense of the reach of who is attending events.
By Hovering over the map we can see what town the customers are based in as well as their purchase patterns. 

<img src="img/regional_overview.png" width=500> 

We can also quickly see what time of day they are on the webpages as well as what they're preferred category is.  

<img src="img/time_of_visit.png" width=500> 
<img src="img/preferred_main.png" width=500> 

## Total Event Trends 
We can see what purchase patterns across all the provided events. 

<img src="img/whowhen.png" width=500> 
<img src="img/dow.png" width=500> 

*We used an NLP library to take customer first name and map it to likely gender. This will not be 100% accurate*


## Single Event Trends 

To get a bit more granular we can look at individual events by narrowing down the instances using the checkboxes.  For example, if you're only interested in the one event below: 

<img src="img/single_table.png" width=500> 

From there you can get information for the event or events that you care about including day of week, time of day they purchased, gender as well as how far in advance tickets were purchased 

<img src="img/advance.png" width=500> 

## How to Run 

This is made in Observable framework. For instructions on how to run that on your machine you can visit the documenation [here](METLN/README.md)

ONce you get the required data (this includes a csv for transactions as well as an Event_Purchaser csv) save the files to your local machine under in the [data folder](METLN/src/data)- this is located in the src file in the framework. 

If the data is where it should be you can run the following command in your terminal to launch the interactivable framework

```
make Launch 
```

Then what? make sure theyre named what we named them and/or is there a way to not hardcode this? 