import plotly.express as px
from plotly.graph_objs import Figure

from ingest.queries import get_temp_to_df


def stations_map() -> Figure:
    stations_info = get_temp_to_df('stations-meteo-en-place', 'stations')

    figure = px.scatter_mapbox(stations_info, lat="latitude", lon="longitude", color="temp",
                               hover_name="id_nom",
                               color_continuous_scale="bluered", size_max=15, zoom=12)

    figure.update_layout(mapbox_style="carto-darkmatter",
                         paper_bgcolor="rgba(0,0,0,0)",
                         font_color="white")

    figure.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    figure.update_traces(marker=dict(size=30),
                         selector=dict(mode='markers'))

    return figure
