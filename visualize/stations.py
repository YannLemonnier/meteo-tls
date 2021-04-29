import plotly.express as px
from plotly.graph_objs import Figure

from visualize.queries import table_to_df


def stations_map() -> Figure:
    stations_info = table_to_df('stations-meteo-en-place')

    figure = px.scatter_mapbox(stations_info, lat="latitude", lon="longitude", color="altitude",
                               hover_name="id_nom",
                               color_continuous_scale="earth", size_max=15, zoom=12)

    figure.update_layout(mapbox_style="carto-darkmatter")

    figure.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    figure.update_traces(marker=dict(size=30),
                         selector=dict(mode='markers'))

    return figure
