from unittest.mock import patch

import pytest

from ingest_to_bigquery import ingest_station_description, ingest_station_data
from queries import table_to_df


@pytest.fixture
def mock_ingest_station_description():
    with patch('import_toulouse_dataset.ImportToulouseDataset.upload') as upload_url:
        with patch('import_gs_file_in_bq.ImportGsFileInBq.load') as load_table:
            ingest_station_description('fake_dataset')

            yield upload_url, load_table


def test_upload_url(mock_ingest_station_description):
    upload_url, load_table = mock_ingest_station_description
    assert upload_url.called


def test_load_table(mock_ingest_station_description):
    upload_url, load_table = mock_ingest_station_description
    assert load_table.called


@pytest.fixture
def mock_ingest_station_data():
    with patch('import_toulouse_dataset.ImportToulouseDataset.upload') as upload_url:
        with patch('import_gs_file_in_bq.ImportGsFileInBq.load') as load_table:
            ingest_station_data('fake_dataset')
            yield upload_url, load_table


def test_ingest_station_data_upload_url(mock_ingest_station_data):
    expected_call_count = len(table_to_df('stations-meteo-en-place'))
    upload_url, load_table = mock_ingest_station_data
    assert upload_url.call_count == expected_call_count


def test_ingest_station_data_load_table(mock_ingest_station_data):
    upload_url, load_table = mock_ingest_station_data
    assert load_table.call_count == 1


if __name__ == '__main__':
    pytest.main()
