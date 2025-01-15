# -*- coding: utf-8 -*-
import numpy as np
from click import style
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import requests

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


circuits = pd.read_csv('./data/circuits.csv')
constructor_standings = pd.read_csv('./data/constructor_standings.csv')
constructors = pd.read_csv('./data/constructors.csv')
driver_standings = pd.read_csv('./data/driver_standings.csv')
drivers = pd.read_csv('./data/drivers.csv')
lap_times = pd.read_csv('./data/lap_times.csv')
pit_stops = pd.read_csv('./data/pit_stops.csv')
races = pd.read_csv('./data/races.csv')
qualifying = pd.read_csv('./data/qualifying.csv')
results = pd.read_csv('./data/results.csv')
seasons = pd.read_csv('./data/seasons.csv')
sprint_results = pd.read_csv('./data/sprint_results.csv')
status = pd.read_csv('./data/status.csv')
constructor_results = pd.read_csv('./data/constructor_results.csv')

races_with_laps_and_drivers = races.merge(lap_times, on='raceId').merge(drivers, on='driverId')

base_url = 'https://www.meteosource.com'
params = {
    "lat": '0',
    "lon": '0',
    "sections": "current,hourly",
    "language": "en",
    "units": "metric",
    "key": "5vc7dled7kaot0sl6jr71b7i3zmhaj6kaqllltk8"
}


app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Circuits',
                children=[
            dbc.Row(
                children=[
                html.Label("Select a season:", style={"fontWeight": "bold"}),
                dcc.Dropdown(
                    id="season-dropdown",
                    options=[{"label": str(year), "value": year} for year in
                             seasons.sort_values(by='year', ascending=True, inplace=False)['year'].unique()],
                    style={
                        "width": "400px",
                        "borderRadius": "12px",
                        # "boxShadow": "0 2px 6px rgba(0, 0, 0, 0.1)"
                    }
                ),
                html.Label("Select race style:", style={"fontWeight": "bold"}),
                dcc.Dropdown(
                    id="race-type-dropdown",
                    options=['Races', 'Sprints'],
                    style={
                        "width": "400px",
                        "borderRadius": "12px",
                        # "boxShadow": "0 2px 6px rgba(0, 0, 0, 0.1)"
                    }
                )
            ], justify="center", style={
                    "display": "grid",
                    "grid-template-columns": "repeat(4, auto)",
                    "marginBottom": "30px",
                    "gap": "10px",
                    "margin-left": "50px",
                    "margin-right": "50px",
                    "align-items": "center",
                }),

            dbc.Row([
                dbc.Col(dcc.Graph(id="geo-map"), width=12)
            ], justify="center", style={"marginBottom": "30px"}),

            dbc.Alert([
                html.H2(id='circuit-name', style={
                    'textAlign': 'center',
                    'color': 'white',
                    'fontFamily': 'Arial, sans-serif',
                    'fontWeight': 'bold',
                    'fontSize': '24px'
                }),
            ], style={
                'backgroundColor': '#1E3D58',
                'borderColor': '#1E3D58',
                'borderRadius': '15px',
                'padding': '20px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
            }),

            dbc.Row([
                dbc.Col(dbc.Alert([
                    html.H2(id='total-races', style={
                        'textAlign': 'center',
                        'color': 'white',
                        'fontFamily': 'Arial, sans-serif',
                        'fontWeight': 'bold',
                        'fontSize': '20px'
                    })
                ], style={
                    'backgroundColor': '#3E6A88',
                    'borderColor': '#3E6A88',
                    'borderRadius': '12px',
                    'padding': '15px',
                    'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
                }), width=6),

                dbc.Col(dbc.Alert([
                    html.Img(
                        id="actual-weather-icon",
                        alt="Select a circuit",
                        style={
                            "width": "50px",
                            "height": "50px",
                            "display": "block",
                            "margin": "0 auto"
                        }
                    ),
                ], style={
                    'backgroundColor': '#3E6A88',
                    'borderColor': '#3E6A88',
                    'borderRadius': '12px',
                    'padding': '15px',
                    'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
                }), width=6),
            ], justify="center", style={"marginBottom": "30px"}),

            dbc.Row([
                dbc.Col(dcc.Graph(id="circuit-info"), width=12)
            ], justify="center"),
        ]),
        dcc.Tab(label='Drivers',
                children=[
            dbc.Row([
                html.Label("Driver name:", style={"fontWeight": "bold", "text-align": "center"}),
                html.Label("Select a season:", style={"fontWeight": "bold", "text-align": "center"}),
                html.Label("Select a race:", style={"fontWeight": "bold", "text-align": "center"}),
                dbc.Col(dcc.Input(
                    id="driver-name-input",
                    placeholder="Write a driver's name",
                    type="text",
                    style={
                        "width": "400px",
                        "borderRadius": "12px",
                        # "boxShadow": "0 2px 6px rgba(0, 0, 0, 0.1)"
                    }
                ), width=4),
                dbc.Col(dcc.Dropdown(
                    id="season-races-dropdown",
                    options=[{"label": str(year), "value": year} for year in races_with_laps_and_drivers['year'].sort_values(ascending=True).unique()],
                    placeholder="Select the season",
                    style={
                        "width": "400px",
                        "borderRadius": "12px",
                        # "boxShadow": "0 2px 6px rgba(0, 0, 0, 0.1)"
                    }
                ), width=4),
                dbc.Col(dcc.Dropdown(
                    id="race-dropdown",
                    options=[''],
                    placeholder="Select the race",
                    disabled=True,
                    style={
                        "width": "400px",
                        "borderRadius": "12px",
                        # "boxShadow": "0 2px 6px rgba(0, 0, 0, 0.1)"
                    }
                ), width=4),
            ], justify="center", style={
                    "display": "grid",
                    "grid-template-rows": "repeat(2, auto)",
                    "grid-template-columns": "repeat(3, auto)",
                    "marginBottom": "30px",
                    "gap": "10px",
                    "margin-left": "50px",
                    "margin-right": "50px",
                    "align-items": "center",
                }),
            dbc.Row([
                dbc.Col(dcc.Graph(id='race-info'))
            ]),
            dbc.Row([
                html.Label("Race evolution", style={"fontWeight": "bold", "text-align": "center"}),
                dbc.Col(dcc.Input(
                    id="lap-input",
                    type="range",
                    disabled=True,
                    min=2,
                    max=1,
                    step=1,
                    style={
                        "width": "400px",
                        "borderRadius": "12px",
                        # "boxShadow": "0 2px 6px rgba(0, 0, 0, 0.1)"
                    }
                ))
            ], justify="center", style={
                    "display": "grid",
                    "grid-template-rows": "repeat(4, auto)",
                    "marginBottom": "30px",
                    "gap": "10px",
                    "margin-left": "50px",
                    "margin-right": "50px",
                    "align-items": "center",
                })
        ])
    ])
])


@app.callback(
    [Output('race-dropdown', 'options'),
     Output('race-dropdown', 'disabled')],
    Input('season-races-dropdown', 'value')
)
def update_race_dropdown(season_selected):
    if season_selected:
        races_in_season = races_with_laps_and_drivers[races_with_laps_and_drivers['year'] == int(season_selected)]

        unique_circuits = races_in_season[['raceId', 'circuitId']].drop_duplicates('circuitId')

        return ([
            {"label": f"Race {circuits[circuits.circuitId == circuit_id].name.unique()[0]}", "value": race_id}
            for race_id, circuit_id in zip(unique_circuits['raceId'], unique_circuits['circuitId'])
        ], False)
    return [], True

@app.callback(
    [Output('lap-input', 'max'),
     Output('lap-input', 'disabled'),
     Output('lap-input', 'value'),],
     Input('race-dropdown', 'value')
)
def update_max_laps(circuit):
    return (np.max(races_with_laps_and_drivers[races_with_laps_and_drivers.raceId == circuit]['lap']), False, 2) if circuit else (2, True, 2)



@app.callback(
    Output('race-info', 'figure'),
    [Input('driver-name-input', 'value'),
     Input('race-dropdown', 'value'),
     Input('lap-input', 'value')]
)
def update_race_figure(driver, circuit, lap):
    if circuit is None:
        fig = px.line(
            title="Select a race"
        )
        fig.update_layout(
            title_font=dict(size=24, family="Arial", color="darkred"),
            margin=dict(l=0, r=0, t=50, b=0),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        return fig

    laps_filtered = races_with_laps_and_drivers[races_with_laps_and_drivers.raceId == circuit]

    if lap:
        laps_filtered = laps_filtered[laps_filtered.lap <= int(lap)]

    if driver:
        laps_filtered = laps_filtered[laps_filtered['driverRef'].str.contains(driver, case=False, na=False)]

    if laps_filtered.empty:
        fig = px.line(
            title="No data available for the selected filters"
        )
        fig.update_layout(
            title_font=dict(size=24, family="Arial", color="red"),
            margin=dict(l=0, r=0, t=50, b=0),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        return fig

    fig = px.line(
        laps_filtered,
        x='lap',
        y='position',
        color='driverRef',
        title="Lap Analysis by Driver"
    )

    fig.update_layout(
        title_font=dict(size=24, family="Arial", color="darkblue"),
        xaxis_title="Lap",
        yaxis_title="Position",
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False, autorange="reversed"),
        margin=dict(l=0, r=0, t=50, b=0),
        showlegend=True,
    )

    fig.update_traces(
        line=dict(
            width=2,
        ),
        marker=dict(
            size=5,
            line=dict(width=1),
        ),
    )

    return fig


@app.callback(
    Output("geo-map", "figure"),
    [Input("season-dropdown", 'value'),
     Input("race-type-dropdown", "value")]
)
def map_graph(season, race_type):
    circuits_with_season = races[['raceId', 'circuitId', 'year']].merge(circuits, on='circuitId')

    if race_type == 'Sprints':
        circuits_with_season = circuits_with_season[circuits_with_season['raceId'].isin(sprint_results.raceId.unique())]
    elif race_type == 'Races':
        circuits_with_season = circuits_with_season[~circuits_with_season['raceId'].isin(sprint_results.raceId.unique())]

    filtered_data = circuits_with_season[circuits_with_season['year'] == int(season)] if season is not None else circuits_with_season

    fig = px.scatter_geo(
        filtered_data,
        lat="lat",
        lon="lng",
        color='alt',
        hover_name="name",
        title="Circuits",
        color_discrete_sequence=px.colors.qualitative.Prism
    )

    fig.update_layout(
        title={
            'text': "Circuits Around the World",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24, 'family': "Arial", 'color': "#4e4e4e"}
        },
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="LightBlue",
            landcolor="LightYellow",
            projection_type="natural earth",
            bgcolor="#f5f5f5",
        ),
        legend=dict(
            title="Altitude Levels",
            orientation="h",
            x=0.5,
            xanchor="center",
            y=-0.1,
            yanchor="top",
            bgcolor="rgba(255,255,255,0.7)",
            bordercolor="rgba(0,0,0,0.2)",
            borderwidth=1
        ),
        margin={"r": 10, "t": 50, "l": 10, "b": 10}
    )

    fig.update_traces(
        marker=dict(
            size=10,
            opacity=0.8,
            line=dict(width=1, color='DarkSlateGray')
        )
    )

    fig.update_layout(
        coloraxis_colorbar=dict(title="Altitude"),
        coloraxis=dict(cmin=0, cmax=1000)
    )

    fig.update_traces(customdata=filtered_data.circuitId, mode="markers")

    return fig

@app.callback(
    [Output("circuit-info", "figure"),
     Output('total-races', 'children'),
     Output('circuit-name', 'children'),
     Output('actual-weather-icon', 'src')],
    Input("geo-map", "clickData")
)
def display_click_data(circuit):
    if circuit is None:
        return px.bar(), 'Select a circuit', 'Select a circuit', ''

    circuit_id = circuit['points'][0]['customdata']
    df = results[results.positionOrder == 1][['raceId', 'constructorId', 'positionOrder']].merge(
        constructors[['constructorId', 'name']], on='constructorId').merge(races[['raceId', 'circuitId']], on='raceId')

    fig = px.bar(
        df[df.circuitId == circuit_id].groupby(by='name').size().reset_index(name='count'),
        x='name',
        y='count',
        text='count',
        title="Race Wins by Constructor",
        color='name',
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig.update_layout(
        title={
            'text': "Race Wins by Constructor",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'family': "Arial", 'color': "#4e4e4e"}
        },
        xaxis=dict(
            title="Constructor",
            titlefont=dict(size=14),
            tickangle=45,
            showgrid=False
        ),
        yaxis=dict(
            title="Number of Wins",
            titlefont=dict(size=14),
            showgrid=True,
            gridcolor='LightGray'
        ),
        plot_bgcolor="rgba(240, 240, 240, 0.7)",
        paper_bgcolor="rgba(255, 255, 255, 1)",
        margin=dict(l=40, r=20, t=60, b=40),
    )

    fig.update_traces(
        marker=dict(
            line=dict(width=1, color='DarkSlateGray')
        ),
        textposition='outside'
    )

    params['lat'] = circuits[circuits.circuitId == circuit_id]['lat']
    params['lon'] = circuits[circuits.circuitId == circuit_id]['lng']

    response = requests.get(base_url + '/api/v1/free/point', params=params)
    response.raise_for_status()

    data = response.json()

    return (
        fig,
        f'Total races: {races[races['circuitId'] == circuit_id].raceId.count()}',
        f'{circuit['points'][0]['hovertext']}',
        f"{base_url}/static/img/ico/weather/{data["current"]['icon_num']}.svg"
    )


if __name__ == '__main__':
    app.run_server(debug=True)
