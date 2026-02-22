# Solar Labs Ltd.
![gif](https://github.com/user-attachments/assets/f55af637-bcb5-49aa-898d-961024c171f4)


## Inspiration
We were inspired by Planet Labs PBC. With the availability of high-resolution satellite imagery, we wanted to build an analytics tool to simplify logistics for urban solar panel development. Calculating solar panel coverage for a city would require retrieving the dimensions of tens of thousands of buildings. That's a lot of paper work... and money.

## What it does
Solar Labs Ltd. provides a live, interactive map dashboard. It scans satellite imagery to detect building rooftops automatically. It highlights roofs and calculates the estimated solar energy they can produce. As you drag the map around, the live analytics panel updates to show the total money saved, carbon emissions prevented, and how many electric vehicles could be charged based on the buildings currently on your screen.

<img width="1696" height="1798" alt="edmonton" src="https://github.com/user-attachments/assets/f7d10573-9993-4203-b901-d1ce727609b3" />

## How we built it
We pulled publicly available, 7.5 cm spatial resolution satellite imagery that captured Edmonton. 
This data ended up being 444 GB. Using a fine-tuned Mask2Former model, we extracted building pixels and mapped them into polygons. A Streamlit interface provides the interactive map and analytics.

Energy potential is calculated using this formula:

$$E = A \times 0.7 \times 1246 \times 0.2$$

Where A is the roof area in square meters.

* **0.7 (Usable Roof Space):** Since we cannot cover a whole roof with solar panels. Space is lost to vents, skylights, and mandatory fire code setbacks. Because of these required safety pathways and physical obstacles, a standard industry packing factor assumes only about 70% of a roof is usable.

* **1246 (Edmonton Solar Potential):** This is the specific solar energy potential for the city. According to data from Natural Resources Canada, a 1 kW solar system in Edmonton produces an average of 1,246 kWh of electricity per year.

* **0.2 (Panel Efficiency):** Solar panels cannot convert 100% of sunlight into power. Standard residential solar panels today operate at an average efficiency rating between 15% and 22%. Since modern solar panels installed today consistently operate at 20% efficiency or higher. We use 20% (0.2) because it is the most realistic baseline for new solar installations.

## Sustainability 

* **0.424 kg (CO₂ Prevented):** Alberta's electricity grid produces exactly 424 grams (0.424 kg) of CO₂ per kWh. This is based on the latest National Inventory Report for Alberta.

* **7,200 (Homes Powered):** The average home in Alberta consumes 7,200 kWh of electricity per year. We divide the total solar potential by 7,200 to find out exactly how many average homes the roof could power.

* **3,040 (EVs Charged):** An average Canadian drives about 15,200 kilometers per year. Because an electric vehicle requires roughly 20 kWh to travel 100 kilometers, it uses exactly 3,040 kWh of electricity per year. We divide the total solar energy by 3,040 to calculate how many EVs the roof could fully charge.

## Challenges we ran into
Being rate limited by Google. After confirming our first batch of data, we were pressed for time as we had less than 24 hours at that point. It took 10 hours to download the dataset and an additional 5 to perform inference. In addition, rendering thousands of polygons in a web browser is difficult, especially if you have a low-spec computer.

## Accomplishments that we're proud of
We are proud of building a dynamic, real time map filter. Instead of just showing a static image, we successfully linked the map's visual boundaries to our data layer. This allows the app to instantly recalculate financial and environmental metrics the moment a user drags the screen.

## What we learned
We learned how to build interactive web applications using Streamlit, which was a completely new framework for us. We also learned how to process geographic data using mapping tools like GeoPandas and Folium. Most importantly, we learned how to combine these new technical skills to create a functioning tool dedicated to sustainability.

## What's next for Solar Labs Ltd.
Improving the model and including more metrics to make the energy and financial estimates more accurate. We will proceed to process the rest of the country and eventually the whole world. #EnergyPower #Money

---

## References
* **Usable Roof Space:** Azul Roofing Solutions. "Is Your Roof Ready for Solar Panels?" https://www.azulroof.com/blog/is-your-roof-ready-for-solar-panels
* **Edmonton Solar Potential:** CER – Provincial and Territorial Energy Profiles. https://www.cer-rec.gc.ca/en/data-analysis/energy-markets/provincial-territorial-energy-profiles/provincial-territorial-energy-profiles-alberta.html
* **Panel Efficiency:** ConsumerAffairs. "Solar Panel Efficiency." https://www.consumeraffairs.com/solar-energy/how-efficient-are-solar-panels.html
* **CO₂ Prevented (0.424 kg):** Government of Alberta. "Alberta's greenhouse gas emissions reduction performance." https://www.alberta.ca/albertas-greenhouse-gas-emissions-reduction-performance
* **Homes Powered (7,200 kWh):** ATCO Energy. "Alberta Electricity Rates & Prices." https://www.atcoenergy.com/blog/alberta-electricity-rates
* **EVs Charged (3,000 kWh):** CBC News. "Does Calgary have the power to charge a million electric vehicles?" https://www.cbc.ca/news/canada/calgary/electric-vehicle-power-demand-calgary-electricity-grid-1.7107192
* EnergyHub. "Solar Power Alberta (2024 Guide)." https://www.energyhub.org/alberta/
* Joinsun. "Solar Panel Efficiency Comparison 2026." https://joinsunnow.com/solar-panel-efficiency-comparison-2026-top-brands-ranked-by-performance/
