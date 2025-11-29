# Maine Ticket Sale Analyis </h1>
## A visualiztion of trends in local ticket sales</h2>

This interactive dashboard was made using data provided by the Main Trust for Local News to look at trends from <a href="https://www.tickets207.com/" title="Tickets207">Tickets207</a>
<br>
<br>
Our goal is to create a dashboard to offer insight into
- Who is buying tickets?
- When are they buying them?
- What are they buying?

<br>

We also have some additional customer data which we have used to partially explore the "why" behind ticket purchases.




<style>
.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: var(--sans-serif);
  margin: 2rem 0 2rem;
  text-wrap: balance;
  text-align: center;
}

.hero h1 {
  margin: 2rem 0;
  max-width: none;
  font-size: 14vw;
  font-weight: 900;
  line-height: 1.2;
  background: linear-gradient(30deg, var(--theme-foreground-focus), currentColor);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero h2 {
  margin: 0;
  max-width: 34em;
  font-size: 20px;
  font-style: initial;
  font-weight: 500;
  line-height: 1.5;
  color: var(--theme-foreground-muted);
}

@media (min-width: 640px) {
  .hero h1 {
    font-size: 90px;
  }
}

.explore {
  font-family: var(--sans-serif);
  margin: 2rem 0 2rem;
  text-wrap: balance;
  text-align: left;
}

.nav-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin: 2rem 0;
  text-align: center;
}

.nav-button {
  padding: 0.75rem 1.5rem;
  background: #a6bdf0ff;  
  color: #ffffff;  
  text-decoration: none;
  border-radius: 0.5rem;
  font-weight: 600;
  transition: all 0.2s;
  font-family: var(--sans-serif);
}

.nav-button:hover {
  background: #1d4ed8;  
  transform: translateY(-2px);
}
</style>

<div class="nav-buttons">
  <a href="./totalevents" class="nav-button">All Events <br>(Who & When)</a>
  <a href="./tables" class="nav-button">Individual Events <br>(What, Who, & When)</a>
  <a href="./maptry" class="nav-button">Customer Data <br>(What & Why)</a>