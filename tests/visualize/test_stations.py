from unittest.mock import patch

import pandas as pd
import pytest

from plotly.graph_objs import Figure

from visualize.stations import stations_map


@pytest.fixture
def setup():
    with patch('visualize.stations.get_all_temp_to_df') as all_temp:
        all_temp.return_value = pd.DataFrame([['14-fake_id', 45, 2, 135, '2020-05-21', 13.4]],
                                             columns=['id_nom', 'longitude', 'latitude', 'altitude', 'datetime',
                                                      "temperature"])
        yield


def test_stations_map(setup):
    assert isinstance(stations_map(), Figure)


def test_stations_map_date(setup):
    assert isinstance(stations_map('2020-05-21'), Figure)


if __name__ == '__main__':
    pytest.main()
