import dash
import dash_core_components as dcc
import dash_html_components as html

from ingest.main import start_data_ingestion

dash_app = dash.Dash()
app = dash_app.server

dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

dash_example_layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.H1(children='Hello Dash', id='title'),

    html.Div(children='''
        This is Dash running on Google App Engine.
    ''', id='subtitle'),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
], id='page-content')


@dash_app.callback(dash.dependencies.Output('page-content', 'children'),
                   [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/tasks/ingest':
        html.Div([
            html.H3('Start data ingestion')])
        return html.Div([
            html.H3(start_data_ingestion())
        ])
    else:
        return dash_example_layout


if __name__ == '__main__':
    dash_app.run_server(debug=True)
