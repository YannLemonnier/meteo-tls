import dash
import dash_core_components as dcc
import dash_html_components as html

from visualize.stations import stations_map

dash_app = dash.Dash()
app = dash_app.server

dash_app.layout = html.Div(children=[
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

if __name__ == '__main__':
    dash_app.run_server(debug=True)
