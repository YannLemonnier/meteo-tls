import pandas as pd
import pytest

from unittest.mock import patch

from plotly.graph_objs import Figure

from visualize.std_plot import std_plot


def test_std_plot():
    with patch('ingest.queries.get_std_by_date_hour') as df:
        df.return_value = pd.DataFrame([[1.42, 43.6, 135]],
                                       columns=['datetime', 'temperature', 'std'])
        assert isinstance(std_plot(), Figure)


if __name__ == '__main__':
    pytest.main()
