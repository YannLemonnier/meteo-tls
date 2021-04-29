from unittest.mock import patch

import pytest

from queries import table_to_df


def test_table_to_df():
    with patch('google.cloud.bigquery.client.Client.query') as query:
        table_to_df('fake-table')
        assert query.called


if __name__ == '__main__':
    pytest.main()
