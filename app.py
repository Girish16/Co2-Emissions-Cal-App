import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px



df = pd.read_csv('emissions.csv')

# Dash web application
app = dash.Dash(__name__)

# Layout of the web application with CSS styles
app.layout = html.Div([
    html.Div([
        html.H1("CO2 Gas Emissions Data Visualization",
                style={
                    'background-color': '#C7CC33',
                    'color': 'white',
                    'padding': '20px',
                    'border-radius': '5px',
                    'margin-bottom': '20px',
                    'text-align': 'center',
                    'font-family': 'Arial, sans-serif',
                }
        ),
    ],
        
       )
    ,

    html.Div([
        html.Label("Select Countries:", 
            style={
                'font-size': '16px',
                'font-weight': 'bold',
                'margin-right': '20px',
                'vertical-align': 'middle',
                'color': '#3366CC',
            }
        ),
        dcc.Dropdown(
            id="country-dropdown",
            options=[{'label': country, 'value': country} for country in df['Country/Region']],
            multi=True,
            value=['China', 'United States'],
            style={'width': '50%', 'font-size': '16px', 'color': '#4CAF50'}
        ),
    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '20px'}),

    html.Div([
        html.Label("Select Year Range:", 
            style={
                'font-size': '16px',
                'font-weight': 'bold',
                'margin-right': '20px',
                'vertical-align': 'middle',
                'color': '#3366CC',
            }
        ),
        dcc.Input(
            id="start-year",
            type="number",
            placeholder="Start Year",
            min=int(df.columns[3]),
            max=int(df.columns[-1]),
            step=1,
            value=int(df.columns[3]),
            style={'width': '10%', 'font-size': '16px', 'color': '#4CAF50'}
        ),
        dcc.Input(
            id="end-year",
            type="number",
            placeholder="End Year",
            min=int(df.columns[3]),
            max=int(df.columns[-1]),
            step=1,
            value=int(df.columns[-1]),
            style={'width': '10%', 'font-size': '16px', 'color': '#4CAF50'}
        ),
    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '20px'}),

    dcc.Graph(id="emissions-plot", style={'height': '60vh'}),
    dcc.Graph(id="total-emissions-bar-chart", style={'height': '60vh'}), 
])

@app.callback(
    Output("emissions-plot", "figure"),
    [Input("country-dropdown", "value"), Input("start-year", "value"), Input("end-year", "value")]
)
def update_emissions_plot(selected_countries, start_year, end_year):
    selected_columns = ['Country/Region'] + [str(year) for year in range(start_year, end_year + 1)]
    filtered_data = df[df['Country/Region'].isin(selected_countries)][selected_columns]
    melted_data = pd.melt(filtered_data, id_vars=['Country/Region'], var_name='Year', value_name='Emissions')

    fig = px.line(
        melted_data,
        x="Year",
        y="Emissions",
        color="Country/Region",
        title="Greenhouse Gas Emissions",
        labels={'Year': 'Year', 'Emissions': 'Emissions'},
        
    )

    return fig

@app.callback(
    Output("total-emissions-bar-chart", "figure"),  
    [Input("country-dropdown", "value"), Input("start-year", "value"), Input("end-year", "value")]
)
def update_total_emissions_bar_chart(selected_countries, start_year, end_year):
    selected_columns = ['Country/Region'] + [str(year) for year in range(start_year, end_year + 1)]
    filtered_data = df[df['Country/Region'].isin(selected_countries)][selected_columns]
    total_emissions = filtered_data.iloc[:, 2:].sum(axis=1)

    fig = px.bar(
        x=filtered_data['Country/Region'],  
        y=total_emissions,
        color = filtered_data['Country/Region'],
        labels={'x': 'Country/Region', 'y': 'Total Emissions'},
        title="Total Emissions by Country/Region",
    )

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
