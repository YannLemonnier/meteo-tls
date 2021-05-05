import pandas
import plotly.express as px
from plotly.graph_objs import Figure

from ingest.queries import get_all_temp_to_df

all_temp = pandas.DataFrame()


def stations_map(date: str = None) -> Figure:

    global all_temp
    if all_temp.index.empty:
        all_temp = get_all_temp_to_df('stations-meteo-en-place', 'stations')

    if date == '' or date is None:
        stations_info = all_temp.groupby(['id_nom', 'longitude', 'latitude', 'altitude'], as_index=False).mean()
        mean = stations_info.temperature.mean().round(2)
        std = stations_info.temperature.std().round(2)
        title = f'Températures moyennes {mean}°C ± {std}'
    else:
        stations_info = all_temp.loc[all_temp['datetime'] == date]
        mean = stations_info.temperature.mean().round(2)
        std = stations_info.temperature.std().round(2)
        title = f'Température {mean}°C ± {std} à l\'instant: {date}'

    figure = px.scatter_mapbox(stations_info, lat="latitude", lon="longitude", color="temperature",
                               hover_name="id_nom",
                               color_continuous_scale="bluered", size_max=15, zoom=10, title=title)

    figure.update_layout(mapbox_style="carto-darkmatter",
                         paper_bgcolor="rgba(0,0,0,0)",
                         font_color="white")

    figure.update_layout(margin={"r": 0, "t": 80, "l": 0, "b": 0})
    figure.update_traces(marker=dict(size=30),
                         selector=dict(mode='markers'))

    return figure
