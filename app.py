import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from urllib.request import urlopen
import json


import plotly.graph_objects as go

app = dash.Dash(__name__)

mapbox_access_token = open("f:/mydrive/VyatkaSU/Bank Khlynov/mt.mapbox_token").read()
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"

with urlopen('https://raw.githubusercontent.com/VPcenter/GeoJSON/master/maps/vyatka.geojson') as response:
    counties = json.load(response)

df = pd.read_csv("f:/mydrive/VyatkaSU/Bank Khlynov/okato-credit.csv", dtype={"okato": str})

fig = go.Figure(go.Choroplethmapbox(geojson = counties, locations = df.okato, z = df.credits,
                                    colorscale = 'Tealgrn', zmin = 0, zmax = 100, marker_opacity = 0.8, marker_line_width = 0.85))
fig.update_layout(mapbox_style = "dark", mapbox_accesstoken = mapbox_access_token,
                  mapbox_zoom = 5.7, mapbox_center = {"lat": 58.6034, "lon": 49.6678})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

app.layout = html.Div(
    id = 'root',
    children = [
        html.Div(
            id = 'header',
            children = [
                html.Img(id = 'logo', src = app.get_asset_url('vyatsu-logo.png')),
                html.H4(children = 'Показатели скоринг-оценок юридических лиц Кировской области'),
                html.P(
                    id = 'description',
                    children = 'Интерактивная карта Кировской области. Муниципальные районы области окрашены \
                    в цвет отражающий объем закредитованных юридических лиц. Score графа показывает \
                    кредитоспособность субъекта (по даннм прогноза и оценок ЭММ).',
                ),
            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="heatmap-container",
                            children=[
                                html.P(id="heatmap-title",
                                    children = 'Тепловая карта'),
                                dcc.Graph(
                                    id="county-choropleth",
                                    figure=fig,
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    id="graph-container",
                    children=[
                        html.P(id="chart-selector", children="Выберите параметр из выпадающего списка:"),
                        dcc.Dropdown(
                            options=[
                                {
                                    "label": "Гистограмма один",
                                    "value": "show_absolute_deaths_single_year",
                                },
                                {
                                    "label": "Гистограмма два (1999-2016)",
                                    "value": "absolute_deaths_all_time",
                                },
                                {
                                    "label": "Гистограмма три (один год)",
                                    "value": "show_death_rate_single_year",
                                },
                                {
                                    "label": "Гистограмма четыре (1999-2016)",
                                    "value": "death_rate_all_time",
                                },
                            ],
                            value="show_death_rate_single_year",
                            id="chart-dropdown",
                        ),
                        dcc.Graph(
                            id="selected-data",
                        ),
                    ],
                ),
            ],
        ),
    ],
)

if __name__ == '__main__':
    app.run_server(debug=True)