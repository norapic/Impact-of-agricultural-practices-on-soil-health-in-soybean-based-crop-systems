This project is meant to showcase a simple dashboard using Python, synthesizing the analysis of different agricultural practices on soil health in soybean-based crop systems.

# Description
In this project, we use several statistical tests to compare the impact of practices on soil health across different soil orders.
The results of these tests, along with the corresponding visuals, are displayed in the dashboard.

# Usage
* 1/ Install Dash
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
The dashboard sums up the analysis in interactive, user-friendly visuals. It is built on the `app.py` script using Dash and Plotly Python libraries.
