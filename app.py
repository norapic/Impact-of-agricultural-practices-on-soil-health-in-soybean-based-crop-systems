from dash import Dash, html, dcc, Input, Output, State, dash_table, callback
import plotly.express as px
import pandas as pd
import openpyxl
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
from utils.desciptive_plots import *
from utils.comparison_tests import *

# Load the data for anamlysis and visualization
df = pd.read_excel('data/data.xlsx', sheet_name="meta" ,engine='openpyxl')
coord = pd.read_excel('data/coord.xlsx', engine='openpyxl')

# Clean and transform the data
coord.columns = ['location', 'latitude', 'longitude']
df.loc[df['crop_rotation_factor'] == "Single-crop", 'crop_rotation_factor'] = '1 crop'
df.loc[df['crop_rotation_factor'] == "2 crops ", 'crop_rotation_factor'] ='2 crops'
df_merged = pd.merge(df, coord, on='location', how='left')
df_merged.columns = [col.replace('-', '_') for col in df_merged.columns]

# List of practices to compare
practices = ['tillage_factor', 'crop_rotation_factor', 'drainage', 'cover_crop']
# List of indicators to compare
indicators = ['pH', 'OM_LOI', 'STP', 'STK', 'TOC',
       'TC', 'TN', 'POX_C', 'WAS', 'Min_C', 'WEOC', 'ACE_N']
# List of condition factors
conditions = ['soil_order', 'texture_class', 'state']
# List of factors to add
factors_to_add = ['site_number', 'rep']

# Add a columns with the combination of practices for each data point
df_merged['practices'] = df_merged[practices].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)

# Load data for the modal
df_readme = pd.read_excel('data/data.xlsx', sheet_name="readme" ,engine='openpyxl')
df_readme.Variables = [col.replace('-', '_') for col in df_readme.Variables]
df_info = df_readme.loc[df_readme['Variables'].isin(practices + conditions + indicators), ['Variables', 'Description', 'Unit']]

# Define external stylesheets (optional)
external_stylesheets = [dbc.themes.MINTY]

# Create the Dash app
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Create the layout
app.layout = dbc.Container([
    dbc.Row(
        [
        html.H2("Exploration of the impact of practices on soil indicators in soybean cropping systems in the US",
                    className='text-center',
                    style={'color': 'darkgreen', 'fontSize': 22, 'fontWeight': 'bold',
                            'marginBottom': 15},
                    )
        ],
        style={"height": "5vh", 'marginBottom': 20},
        className='bg-primary text-white font-italic',
    ),
    dbc.Row([
        html.H2("The figures below allow to explore the impact of differents agricultural practices on soil " +
                " indicators in soybean cropping systems in the US.",
                style={'color': 'black', 'fontSize': 19},
        ),
        html.Div([
            html.H4("Practices are displayed are discribed as follow : Tillage_Crop rotation_Drainage_Cover crop.\n" +
                    "See `Details` button for more information",
                    style={'color': 'black', 'fontSize': 15},),
            dcc.Button("Details", id="open", n_clicks=0),
                dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Information")),
                    dbc.ModalBody(
                        dash_table.DataTable(
                            data=df_info.to_dict('records'),
                            columns=[{"name": i, "id": i} for i in df_info.columns],
                        )
                    ),
                    dbc.ModalFooter(dbc.Button("Close", id="close", className="ms-auto", n_clicks=0)),
                ],
                id="modal",
                size="xl",
                is_open=False,
                scrollable=True,
                ),
            html.P(" - The map on the left shows the location of the sites having the same practices, " +
                    "colored depending on regional or soil conditions factor (soil order, soil texture type and state where the site is located)" +
                    " and with a size depending on the value of the selected indicator."),
            html.P(" - The boxplot on the right shows the distribution of the selected indicator depending on the regional or soil " + 
                "condition factor."),
        ])
        ],
        style={'marginBottom': 10},
        className='bg-light'
    ),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='practices_selector',
                options=[{"label": v, "value": v} for v in np.sort(df_merged['practices'].unique())],
                placeholder="Select practice"
            ),
            width=3
            ),
        dbc.Col(
            dcc.Dropdown(
                id='conditions_selector',
                options=[{"label": v, "value": v} for v in conditions],
                placeholder="Select condition"
            ),
            width=3
        ),
        dbc.Col(
            dcc.Dropdown(
                id='indicators_selector',
                options=[{"label": v, "value": v} for v in indicators],
                placeholder="Select indicator"
            ),
            width=3
        ),
        ],
        style={'marginBottom': 20},
        className='bg-light'
    ),
    dbc.Row([
        dbc.Col(dcc.Graph(id='map_graph'), width=6),
        dbc.Col(dcc.Graph(id='boxplot_soil'), width=6),
        ],
        style={'marginBottom': 20},
        className='bg-light'
    ),
])

# Create a callback for global viasualization and analysis
@app.callback(
    Output('map_graph', 'figure'),
    Output('boxplot_soil', 'figure'),
    Input('conditions_selector', 'value'),
    Input('practices_selector', 'value'),
    Input('indicators_selector', 'value'),
)
def update_global_figures(condition_choice, practice_choice, indicator_choice):
    # Return empty figures if any dropdown value is not selected yet
    if condition_choice is None or practice_choice is None or indicator_choice is None:
        return go.Figure(), go.Figure()

    # Filter the merged dataframe based on the selected practice
    dt = df_merged.loc[df_merged['practices'] == practice_choice]

    # Update the map
    fig_map = px.scatter_geo(
        dt,
        lat='latitude',
        lon='longitude',
        locationmode='USA-states',
        hover_name='location',
        color=condition_choice,
        size = indicator_choice
    )
    list_practices = practice_choice.split("_")
    fig_map.update_layout(
        title = f"Map of the {len(dt.site_number.unique())} sites colored depending on {condition_choice} practicing : ",
        title_subtitle = {'text' : f"Tillage : " + list_practices[0] + "<br>" +
                          "Crop rotation : " + list_practices[1] + "<br>" +
                          "Drainage : " + list_practices[2] + "<br>" +
                          "Cover crop : " + list_practices[3],
                        'font': {'style': 'italic'}},
        geo = dict(
            scope = 'usa',
            landcolor = 'rgb(217, 217, 217)')
        )
    fig_map.update_traces(
        showlegend=False
    )

    # Update the boxplot
    fig_box = px.box(dt, y=indicator_choice, x=condition_choice,
                      title=f"{indicator_choice} depending on {condition_choice}",
                      color=condition_choice)
    
    return fig_map, fig_box

# Create a callback for the modal
@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
