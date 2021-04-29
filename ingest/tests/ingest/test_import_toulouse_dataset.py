from unittest.mock import patch
from urllib.parse import urlparse

import pytest
from google.api_core.exceptions import NotFound
from google.cloud.storage import Blob, Bucket

from ingest.import_toulouse_dataset import ImportToulouseDataset


class TestImportDatasetFile:
    @pytest.fixture
    def factice_dataset_import(self):
        yield ImportToulouseDataset('factice_dataset')

    def test_dataset_url_is_valid(self, factice_dataset_import):
        result = urlparse(factice_dataset_import.dataset_url)
        assert all([result.scheme, result.netloc, result.path])

    def test_error_when_url_is_not_reachable(self):
        with patch('google.cloud.storage.client.Client.get_bucket') as get_bucket:
            with pytest.raises(ValueError, match='Issues when reaching dataset url. Please check dataset name'):
                ImportToulouseDataset('factice_dataset', 'meteo-tls').upload()

    def test_error_with_invalid_project(self):
        with patch('google.cloud.storage.client.Client.get_bucket') as get_bucket:
            get_bucket.side_effect = NotFound('Bucket not found')
            with pytest.raises(ValueError, match='Issues when reaching project bucket. Please check project name'):
                ImportToulouseDataset('stations-meteo-en-place', 'factice_project').upload()

    def test_call_upload_from_string(self):
        with patch('google.cloud.storage.blob.Blob.upload_from_string') as upload:
            ImportToulouseDataset('stations-meteo-en-place', 'meteo-tls').upload()
            assert upload.called

    def test_call_upload_return_blob(self):
        with patch('google.cloud.storage.blob.Blob.upload_from_string'):
            result = ImportToulouseDataset('stations-meteo-en-place', 'meteo-tls').upload()

        assert isinstance(result, Blob)


if __name__ == '__main__':
    pytest.main()
