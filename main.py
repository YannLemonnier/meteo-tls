import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from ingest.main import main

from visualize.stations import stations_map

BS = "https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/cyborg/bootstrap.min.css"

dash_app = dash.Dash(external_stylesheets=[BS])
app = dash_app.server

main_layout = html.Div(children=[
    html.H1(children='Weather at Toulouse'),

    html.Div(children='''
        This is a map with all weather stations.
    '''),

    dcc.Graph(
        id='stations',
        figure=stations_map(),
        style={'width': '98vw', 'height': '90vh'}
    ),
])

dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@dash_app.callback(Output('page-content', 'children'),
                   Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return main_layout
    elif pathname == '/tasks/ingest':
        main('data', 'context')
        return '200'
    else:
        return '404'


if __name__ == '__main__':
    dash_app.run_server(debug=True)
