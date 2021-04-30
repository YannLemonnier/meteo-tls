import dash
import dash_core_components as dcc
import dash_html_components as html
from flask import request

from ingest.main import start_ingest

from visualize.stations import stations_map

BS = "https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/cyborg/bootstrap.min.css"

dash_app = dash.Dash(external_stylesheets=[BS])
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
    # https://stackoverflow.com/a/42254713
    cron_header_validator_wrapper.__name__ = protected_function.__name__
    return cron_header_validator_wrapper


@app.route('/tasks/ingest')
@validate_cron_header
def start():
    """Return a friendly HTTP greeting."""
    start_ingest()
    return '200'


if __name__ == '__main__':
    dash_app.run_server(debug=True)
