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
df_merged['POX_C'] = df_merged['POX_C'].astype("float")
df_merged['texture_class'] = df_merged['texture_class'].str.strip()

# List of practices to compare
practices = ['tillage_factor', 'crop_rotation_factor', 'drainage', 'cover_crop']
# List of indicators to compare
indicators = ['pH', 'OM_LOI', 'STP', 'STK', 'TOC',
       'TC', 'TN', 'POX_C', 'WAS', 'Min_C', 'WEOC', 'ACE_N']
# List of condition factors
conditions = ['soil_order', 'texture_class', 'state']
styling_conditions = [
                    {"condition" : "params.data.Condition == 'soil_order'",
                    "style": {"backgroundColor": "lightblue"}},
                    {"condition": "params.data.Condition == 'texture_class'",
                    "style": {"backgroundColor": "lightgreen"}},
                    {"condition": "params.data.Condition == 'state'",
                    "style": {"backgroundColor": "lightyellow"}}]

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
            html.H4("Practices are displayed are discribed as follow : Tillage_Crop rotation_Drainage_Cover crop." +
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
                    "colored depending on regional or soil conditions factor (soil order, soil texture " +
                    "type and state where the site is located)" +
                    " and with a size depending on the value of the selected indicator."),
            html.P(" - The boxplot on the right shows the distribution of the selected indicator depending on " + 
                "the regional or soil condition factor."),
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
    dbc.Row([
        html.Div([
            html.P("The visuals above show that :"),
            html.P(" - The map as well as the boxplot show that, for the same practices indicators " +
                "can variates a lot depending on the soil or regional conditions"),
            html.P(" - The boxplot show that there can be a lot of variability in the distribution of the indicators " +
                "within a level of a selcted conditions, espacially when this this level is spread across several sites"),
            html.H4("In the tables below, the effects of the conditions and the sites on the indicators are tested for each practices combination. " +
                    "The cells are colored based on the conditions",
                    style={'color': 'black', 'fontSize': 15},)
        ])
    ],
    style={'marginBottom': 10},
    className='bg-light'
    ),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H4("Conditions effects tests :"),
                dag.AgGrid(id='conditions_effects',
                           getRowStyle={
                               "styleConditions": styling_conditions
                           }),
            ]),
            width=6
        ),
        dbc.Col(
            html.Div([
                html.H4("Site effects tests :"),
                dag.AgGrid(id='site_effects',
                            getRowStyle={
                            "styleConditions": styling_conditions
                            })
            ]),
            width=6
        ),
    ],
    style={'marginBottom': 20},
    className='bg-light')
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
    if not condition_choice or practice_choice is None or indicator_choice is None:
        return go.Figure(), go.Figure()

    # Filter the merged dataframe based on the selected practice
    dt = df_merged.loc[df_merged['practices'] == practice_choice].copy()

    if isinstance(condition_choice, list):
        combo_name = ' | '.join(condition_choice)
        dt['condition_combo'] = dt[condition_choice].astype(str).agg(' | '.join, axis=1)
        color_col = 'condition_combo'
        title_condition = combo_name
    else:
        color_col = condition_choice
        title_condition = condition_choice

    # Update the map
    fig_map = px.scatter_geo(
        dt,
        lat='latitude',
        lon='longitude',
        locationmode='USA-states',
        hover_name='location',
        color=color_col,
        size=indicator_choice
    )
    list_practices = practice_choice.split("_")
    fig_map.update_layout(
        title=f"Map of the {len(dt.site_number.unique())} sites colored " +
              f"depending on {title_condition} : ",
        title_subtitle={'text': f"Tillage : " + list_practices[0] + "<br>" +
                        "Crop rotation : " + list_practices[1] + "<br>" +
                        "Drainage : " + list_practices[2] + "<br>" +
                        "Cover crop : " + list_practices[3],
                        'font': {'style': 'italic'}},
        geo=dict(
            scope='usa',
            landcolor='rgb(217, 217, 217)')
    )
    fig_map.update_traces(showlegend=False)

    # Update the boxplot
    fig_box = px.box(dt, y=indicator_choice, x=color_col,
                      title=f"{indicator_choice} depending on {title_condition}",
                      color=color_col)

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

# Create callback for the grids
@app.callback(
    Output("conditions_effects", "columnDefs"),
    Output("conditions_effects", "rowData"),
    Output("site_effects", "columnDefs"),
    Output("site_effects", "rowData"),
    Input('practices_selector', 'value'),
)
def update_grids(tests_practice_choice):
    # Filter data frame
    data = df_merged.loc[df_merged['practices'] == tests_practice_choice]
    # Only test the conditions with at least two levels
    condtions_tokeep = [c for c in conditions if len(data[c].unique()) > 1]
    
    # Update contions effects tests :
    df_cond = pd.DataFrame(columns= ['Condition'] + indicators)
    for c in condtions_tokeep :
        row_data = {'Condition': c}
        for i in indicators :
            test_res = global_test(data, i, c)
            row_data[i] = pval_interp(test_res['pvalue'])
        df_cond = df_cond._append(row_data, ignore_index=True)   
    conditions_columnDefs = [{"field": i, "headerName": i} for i in df_cond.columns]
    conditions_rowData = df_cond.to_dict('records')

    # Update site effects tests :
    df_site = pd.DataFrame(columns=['Condition', 'Level'] + indicators)
    for cond in conditions :
        list_levels = data[cond].unique()
        for l in list_levels :
            d = data.loc[data[cond] == l]
            if len(d['site_number'].unique()) > 1 :
                row_data = {'Condition': cond, 'Level': l}
                for i in indicators :
                    t = global_test(d, i, 'site_number')
                    row_data[i] = pval_interp(t['pvalue'])
                df_site = df_site._append(row_data, ignore_index=True)
    site_columnDefs = [{"field": i, "headerName": i} for i in df_site.columns]
    site_rowData = df_site.to_dict('records')

    return conditions_columnDefs, conditions_rowData, site_columnDefs, site_rowData

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
