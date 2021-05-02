import pandas as pd
import pytest

from unittest.mock import patch

from plotly.graph_objs import Figure

from visualize.stations import stations_map


def test_stations_map():
    with patch('ingest.queries.table_to_df') as df:
        df.return_value = pd.DataFrame([[1.42, 43.6, 135, 'factice']],
                                       columns=['longitude', 'latitude', 'altitude', 'id_nom'])
        assert isinstance(stations_map(), Figure)


if __name__ == '__main__':
    pytest.main()
