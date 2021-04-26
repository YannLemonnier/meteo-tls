from unittest.mock import patch

import pytest

from ingest.ingest_station_description import ingest_station_description


@pytest.fixture
def mock_ingest_station_description():
    with patch('import_toulouse_dataset.ImportToulouseDataset.upload') as upload_url:
        with patch('import_gs_file_in_bq.ImportGsFileInBq.load') as load_table:
            ingest_station_description('fake_dataset')

            yield upload_url, load_table


def test_upload_url(mock_ingest_station_description):
    upload_url, load_session = mock_ingest_station_description
    assert upload_url.called


def test_load_table(mock_ingest_station_description):
    upload_url, load_session = mock_ingest_station_description
    assert load_session.called


if __name__ == '__main__':
    pytest.main()
