import plotly.express as px
from plotly.graph_objs import Figure

from ingest.queries import get_std_by_date_hour


def std_plot() -> Figure:
    stations_data = get_std_by_date_hour('stations')

    figure = px.scatter(stations_data, x='datetime', y=['std', 'temperature'])

    figure.update_layout(plot_bgcolor="rgba(0,0,0,0)",
                         paper_bgcolor="rgba(0,0,0,0)",
                         font_color="white")

    figure.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    figure.update_traces(marker=dict(size=15),
                         selector=dict(mode='markers'))

    return figure