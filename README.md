This project is meant to showcase a simple dashboard using Python, synthesizing the analysis of different agricultural practices on soil health in soybean-based crop systems.

# Description
In this project, we use several statistical tests to compare the impact of practices on soil health across different soil orders.
The results of these tests, along with the corresponding visuals, are displayed in the dashboard.

# Usage
* 1/ Install Dash et plotly

<div style="position: relative; border-radius: 6px; overflow: hidden; border: 1px solid #222324;">
  <!-- Styled button -->
  <button 
    style="position: absolute; top: 8px; right: 8px; padding: 3px 8px; font-size: 12px; font-weight: 500; color: #f7fafd; background-color: #f6f8fa33; border: 1px solid #020202; border-radius: 4px; cursor: pointer; z-index: 1;"
    onclick="navigator.clipboard.writeText(document.getElementById('styled-code').textContent.trim()).then(() => {this.textContent = 'Copied!'; setTimeout(() => this.textContent = 'Copy', 2000);})"
  >
  
  </button>
  <!-- Code block with syntax highlighting (GFM style) -->
  <pre style="margin: 0; background-color: #212122; padding: 16px;"><code id="styled-code" style="font-family: SFMono-Regular, Consolas, monospace; color: #f6f7f7;">
pip install Dash plotly.express plotly.graph_object
  </code></pre>
</div>


* 2/ Download the whole folder
* 3/ Run the app

A browser tab or window will open, displaying the dashboard.

# Resources
The data used are from the **study:** https://doi.org/10.1016/j.agee.2025.109950
The coordinate data were generated using AI with the `location` column of the data file as input.

# Analysis
## 1. Statistics and visualization
The `utils` package contains a module to perform the statistical tests called `comparison_tests` and another module called `descriptive_plots` to create the corresponding plots.

## 2. Dashboard
The dashboard sums up the analysis in interactive, user-friendly visuals. It is built on the `app.py` script using Dash and Plotly Python libraries. [![Demo](https://github.com/norapic/Impact-of-agricultural-practices-on-soil-health-in-soybean-based-crop-systems/blob/main/thumbnail.png)](https://github.com/norapic/Impact-of-agricultural-practices-on-soil-health-in-soybean-based-crop-systems/blob/main/demo_app.mp4)
