from collections import namedtuple
from unittest.mock import patch

import pytest

from ingest.initiate_dataset import initiate_dataset


class TestInitiateDataset:
    def test_create_new_dataset(self, patch_list_datasets):
        with patch('google.cloud.bigquery.client.Client.create_dataset') as create_dataset:
            initiate_dataset('new_dataset')
            assert create_dataset.called

    def test_not_create_existing_dataset(self, patch_list_datasets):
        with patch('google.cloud.bigquery.client.Client.create_dataset') as create_dataset:
            initiate_dataset('existing_dataset')
            create_dataset.assert_not_called()

    @pytest.fixture
    def patch_list_datasets(self):
        with patch('google.cloud.bigquery.client.Client.list_datasets') as list_datasets:
            DatasetWithId = namedtuple('DatasetWithId', 'dataset_id')
            fake_dataset = DatasetWithId('existing_dataset')
            list_datasets.return_value = [fake_dataset]
            yield list_datasets


if __name__ == '__main__':
    pytest.main()
