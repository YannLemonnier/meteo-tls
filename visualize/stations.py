import plotly.express as px

from visualize.queries import table_to_df

stations_info = table_to_df('stations-meteo-en-place')

stations_map = px.scatter_mapbox(stations_info, lat="latitude", lon="longitude", color="altitude", hover_name="id_nom",
                                 color_continuous_scale="earth", size_max=15, zoom=12)

stations_map.update_layout(mapbox_style="carto-darkmatter")

stations_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
stations_map.update_traces(marker=dict(size=30),
                           selector=dict(mode='markers'))
