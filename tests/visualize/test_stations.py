import pytest

from plotly.graph_objs import Figure

from visualize.stations import stations_map


def test_stations_map():
    assert isinstance(stations_map(), Figure)


if __name__ == '__main__':
    pytest.main()
