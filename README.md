This project is meant to showcase a simple dashboard using Python, synthesizing the analysis of different agricultural practices on soil health in soybean-based crop systems across different soil orders.

# Description
The study from which this project is based on (see Resources) investigates whether management practices are associated with changes in recommended soil health indicators at the 0–15 cm depth in 4 to 50 year soybean cropping system trials across the US. A total of **21 experiements** were included in the study across 17 locations in the US.

## Soil Health Indicators

The project tracks :
  * **Chemical/Physical** : pH, organic matter loss-on-ignition (OM-LOI), total nitrogen (TN), soil test phosphorus (STP), and soil test potassium (STK).
  * **Biological/Carbon** : Wet aggregate stability (WAS), permanganate oxidizable carbon (POXC), mineralizable carbon (Min-C), water extractable organic carbon (WEOC), total organic carbon (TOC), and soil extractable protein (ACE-N).

## Management practices & findings
The study compare the effect on each practice levels for each indicator. They found out the following results:
* **Crop rotation** : two-crop rotations were associated with greater soil 
test phosphorus (STP) values
* **Tillage** : no-tillage resulted in more acidic 
pH compared to conventional tillage
* **Cover cropping** : associated with greater mineralizable carbon (Min-C) and water extractable organic carbon (WEOC), indicating improved biological activity and labile carbon pools in the 
soil
* **Artificial drainage** : no significant differences between tile-drained and undrained treatments for any of the indicators

## Goal of the project
As suggested in the conclusion of the study, this project extends the analysis across specific soil conditions (soil order), to get a more comprehensive soil health assessment. We use several statistical tests to compare the impact of practices on soil health across different **soil orders**. The results of these tests, along with the corresponding visuals, are displayed in the dashboard.

# Usage
1. Install dependencies

<div style="position: relative; border-radius: 6px; overflow: hidden; border: 1px solid #222324;">
  <!-- Styled button -->
  <button 
    style="position: absolute; top: 8px; right: 8px; padding: 3px 8px; font-size: 12px; font-weight: 500; color: #f7fafd; background-color: #f6f8fa33; border: 1px solid #020202; border-radius: 4px; cursor: pointer; z-index: 1;"
    onclick="navigator.clipboard.writeText(document.getElementById('styled-code').textContent.trim()).then(() => {this.textContent = 'Copied!'; setTimeout(() => this.textContent = 'Copy', 2000);})"
  >
  
  </button>
  <!-- Code block with syntax highlighting (GFM style) -->
  <pre style="margin: 0; background-color: #212122; padding: 16px;"><code id="styled-code" style="font-family: SFMono-Regular, Consolas, monospace; color: #f6f7f7;">
pip install Dash plotly pandas
  </code></pre>
</div>


2. Download the repository
3. Run the app
<div style="position: relative; border-radius: 6px; overflow: hidden; border: 1px solid #222324;">
  <!-- Styled button -->
  <button 
    style="position: absolute; top: 8px; right: 8px; padding: 3px 8px; font-size: 12px; font-weight: 500; color: #f7fafd; background-color: #f6f8fa33; border: 1px solid #020202; border-radius: 4px; cursor: pointer; z-index: 1;"
    onclick="navigator.clipboard.writeText(document.getElementById('styled-code').textContent.trim()).then(() => {this.textContent = 'Copied!'; setTimeout(() => this.textContent = 'Copy', 2000);})"
  >
  
  </button>
  <!-- Code block with syntax highlighting (GFM style) -->
  <pre style="margin: 0; background-color: #212122; padding: 16px;"><code id="styled-code" style="font-family: SFMono-Regular, Consolas, monospace; color: #f6f7f7;">
python app.py
  </code></pre>
</div>

A browser tab will open, displaying the dashboard.

# Resources
The data used are from the **study:** https://doi.org/10.1016/j.agee.2025.109950
The coordinate data were generated using AI with the `location` column of the data file as input and manually checked for accuracy.

# Analysis
## 1. Statistics and visualization
The `utils` package contains two modules:
* `comparison_tests` : Performs statistical tests
* `descriptive_plots`: Generates visuals
The statistical tests are carried out as follows :
* Step 1 : test whether there is an effect of each practice on the considered indicators
* Step 2 : compare the each levels of the practice (ex: for drainage it will be 'yes' and 'no') for each considered indicator

The p-value is interpreted with the following convention :
  - `***` : p <= 0.001
  - `**`: p <= 0.01 and p > 0.001
  - `*`: p <= 0.05 and p > 0.01
  - `ns` : not significant (p > 0.05)

## 2. Dashboard
The dashboard sums up the analysis in interactive, user-friendly visuals. It is built on the `app.py` script using Dash and Plotly Python libraries. ![Demo](https://github.com/norapic/Impact-of-agricultural-practices-on-soil-health-in-soybean-based-crop-systems/blob/main/demo.gif)
