import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from flask import request

from ingest.main import start_ingest

from visualize.stations import stations_map
from visualize.std_plot import std_plot

BS = "https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/cyborg/bootstrap.min.css"

dash_app = dash.Dash(external_stylesheets=[BS], title='Temperatures à Toulouse')
app = dash_app.server

dash_app.layout = html.Div(children=[
    html.H1(children='Températures à Toulouse'),

    html.Div(children='''
        Voici une carte des stations météo de la métropole de Toulouse. 
        Vous pouvez cliquer sur un point (température ou écart-type) 
        dans le deuxième graphe pour faire apparaitre les données de températures
        à cet instant.
    '''),

    dcc.Graph(
        id='stations',
        figure=stations_map(),
        style={'width': '98vw', 'height': '42vh'}
    ),
    dcc.Graph(
        id='ecart',
        figure=std_plot(),
        style={'width': '98vw', 'height': '42vh'}
    ),
])


# Define the decorator to protect your end points
def validate_cron_header(protected_function):
    def cron_header_validator_wrapper(*args, **kwargs):
        header = request.headers.get('X-Appengine-Cron')

        if not header:
            # here you can raise an error, redirect to a page, etc.
            return '403'

        # Run and return the protected function
        return protected_function(*args, **kwargs)

    # The line below is necessary to allow the use of the wrapper on multiple endpoints
    cron_header_validator_wrapper.__name__ = protected_function.__name__
    return cron_header_validator_wrapper


@app.route('/tasks/ingest')
@validate_cron_header
def long_run_ingestion():
    """
    Start a process to perform data ingestion
    :return: 200 if everything is done
    """
    start_ingest()
    return '200'


@dash_app.callback(
    Output('stations', 'figure'),
    Input('ecart', 'clickData'))
def display_clicked_data(clickData):
    date = ''
    try:
        date = clickData['points'][0]['x']
    except TypeError:
        pass
    return stations_map(date)


if __name__ == '__main__':
    dash_app.run_server(debug=False)
