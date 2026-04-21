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
df.loc[df['crop_rotation_factor'] == "Single-crop", 'crop_rotation_factor'] = '1 crops'
df.loc[df['crop_rotation_factor'] == "2 crops ", 'crop_rotation_factor'] ='2 crops'
df_merged = pd.merge(df, coord, on='location', how='left')

# List of practices to compare
practices = ['soil_order', 'tillage_factor', 'crop_rotation_factor', 'drainage']
# List of indicators to compare
indicators = ['pH', 'OM-LOI', 'STP', 'STK', 'TOC',
       'TC', 'TN', 'WAS', 'Min-C', 'WEOC', 'ACE-N']
# List of soil types
soils = ['All', 'Alfisol', 'Ultisol','Mollisol','Vertisol']

# Load data for the modal
df_readme = pd.read_excel('data/data.xlsx', sheet_name="readme" ,engine='openpyxl')
df_info = df_readme.loc[df_readme['Variables'].isin(practices + indicators), ['Variables', 'Description', 'Unit']]

# Define external stylesheets (optional)
external_stylesheets = [dbc.themes.CERULEAN]

# Create the Dash app
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Create the layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div([
            html.H1("Impact of agricultural practices on soil health in soybean-based crop systems"),
            html.H2("Global visualization and analysis",
                     style={'color': 'green', 'fontSize': 24, 'fontWeight': 'bold'}),
            html.P("This section allows you to select a soil type and visualize the map" +
                    " of the locations and the results of the global tests for each practice and health indicator.",
                    style={'color': 'black', 'fontSize': 14, 'fontStyle': 'italic'}),
            html.H4("Select a soil option :", style={'color': 'black', 'fontSize': 18})
        ])
    ]),
    dbc.Row([
        dcc.RadioItems(options= soils,
                    value = 'All',
                    inline=True,
                    id = 'soil_selector',)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='map_graph'), width=6),
        dbc.Col(dag.AgGrid(id='global_test_table',
                        defaultColDef={"filter": True},
                        columnSize="sizeToFit"),
                        width=6)
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H2("Pairwise comparisons", style={'color': 'green', 'fontSize': 24, 'fontWeight': 'bold'}),
                html.P("This section allows you to select a practice and an health indicator to visualize the boxplots" +
                    " and the pairwise comparisons table. The button 'Details' displays information about the practices and indicators.",
                    style={'color': 'black', 'fontSize': 14, 'fontStyle': 'italic'}),
                                dcc.Button("Details", id="open", n_clicks=0),
                dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Details abouts practices and indicators")),
                    dbc.ModalBody(
                        dash_table.DataTable(
                            data=df_info.to_dict('records'),
                            columns=[{"name": i, "id": i} for i in df_info.columns],
                        )
                    ),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close", className="ms-auto", n_clicks=0)
                    ),
                ],
                id="modal",
                size="lg",
                is_open=False,
                ),
            ]),
            width=6),
        dbc.Col(
            html.Div([
                html.H4("Choose a practice and an indicator for pairwise comparisons", style={'color': 'black', 'fontSize': 18}),
                dcc.Dropdown(practices, 'tillage_factor', id='practice_dropdown'),
                dcc.Dropdown(indicators, 'pH', id='indicator_dropdown')
            ]),
            width=6)
    ]),
    dbc.Row([
         dbc.Col(dcc.Graph(id='box_plot'), width=6),
         dbc.Col(dag.AgGrid(id='pairwise_comparisons_table'), width=6)
    ])
])

# Create a callback for global viasualization and analysis
@app.callback(
    Output('map_graph', 'figure'),
    Output('global_test_table', 'rowData'),
    Output('global_test_table', 'columnDefs'),
    Output('practice_dropdown', 'options'),
    Input('soil_selector', 'value'),
)
def update_global_figures(soil_choice):
    # Filter the merged dataframe based on the selected soil type
    if soil_choice != 'All':
        dt = df_merged.loc[df_merged['soil_order'] == soil_choice]
        ## remove soil_order from the practices list and keep the ones with more than 1 factor level
        list_practices = [fact for fact in practices[1:] if len(dt[fact].unique()) > 1]
    else:
        dt = df_merged
        list_practices = practices

    # Update the map
    fig_map = px.scatter_geo(
        dt,
        lat='latitude',
        lon='longitude',
        locationmode='USA-states',
        hover_name='location',
    )
    fig_map.update_layout(
        title = f"Map of soils: {soil_choice}",
        geo = dict(
            scope = 'usa',
            landcolor = 'rgb(217, 217, 217)')
        )
    fig_map.update_traces(
        showlegend=False
    )

    # Update the global test table
    df_res = pd.DataFrame(columns= indicators, index=list_practices)
    for pract in list_practices:
        for indic in indicators:
            pval = global_test(dt, indic, pract)["pvalue"]
            interp = pval_interp(pval)
            df_res.loc[pract, indic] = interp
    df_res.insert(0, 'Practice', df_res.index)
    rowData = df_res.to_dict('records')
    columnDefs = [{"field": col} for col in df_res.columns]

    return fig_map, rowData, columnDefs, list_practices

# Create a callback for boxplots and pairwise comparison
@app.callback(
    Output('box_plot', 'figure'),
    Output('pairwise_comparisons_table', 'rowData'),
    Output('pairwise_comparisons_table', 'columnDefs'),
    Input('soil_selector', 'value'),
    Input('practice_dropdown', 'value'),
    Input('indicator_dropdown', 'value'),
    prevent_initial_call=False
)
def update_box_plot(soil_choice, practice_choice, indicator_choice):
    if soil_choice != 'All':
        dt = df_merged.loc[df_merged['soil_order'] == soil_choice]
    else:
        dt = df_merged
    
    # update the box plot
    fig_box = boxplots_trait_factor(dt, indicator_choice, practice_choice)

    # update the pairwise comparisons table
    pairwaise_res = post_hoc_test(dt, indicator_choice, practice_choice)
    df_pvals = pd.DataFrame(pairwaise_res)
    interp = df_pvals.map(pval_interp)
    interp.insert(0, 'practice', interp.index)
    rowData = interp.to_dict('records')
    columnDefs = [{"field": col} for col in interp.columns]

    return fig_box, rowData, columnDefs

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
