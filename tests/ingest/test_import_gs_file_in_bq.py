from collections import namedtuple
from unittest.mock import patch

import pytest

from ingest.convert_schema import ConvertSchema
from ingest.import_gs_file_in_bq import ImportGsFileInBq


class TestImportGsFileInBq:
    @pytest.fixture(autouse=True)
    def setup(self, patch_available_tables):
        self.dataset = 'fake_dataset'
        self.table = 'fake_table'
        self.my_schema = ConvertSchema('stations-meteo-en-place').bq_schema

    @pytest.fixture
    def patch_available_tables(self):
        TableWithId = namedtuple('TableWithId', 'table_id')
        fake_table = TableWithId('fake_table')
        with patch('google.cloud.bigquery.client.Client.list_tables') as list_tables:
            list_tables.return_value = [fake_table]
            yield list_tables

    def test_instantiate_with_dataset_table_and_schema(self, fake_instance):
        assert isinstance(fake_instance, ImportGsFileInBq)

    @pytest.fixture
    def fake_instance(self):
        yield ImportGsFileInBq(self.dataset, self.table, self.my_schema)

    def test_create_table_if_needed(self, patch_load):
        new_table_instance, _, _ = patch_load
        new_table_instance.table_name = 'new_table'
        with patch('google.cloud.bigquery.client.Client.create_table') as create_table:
            with patch('google.cloud.bigquery.client.Client.load_table_from_uri'):
                new_table_instance.load('fake_uri')
        assert create_table.called

    def test_call_load_table_from_uri(self, patch_load):
        fake_uri = 'gs://fake_bucket/fake.csv'
        fake_instance, load_table_from_uri, table = patch_load

        fake_instance.load(fake_uri)
        assert load_table_from_uri.called

    @pytest.fixture
    def patch_load(self, fake_instance):
        with patch('google.cloud.bigquery.client.Client.load_table_from_uri') as load_table_from_uri:
            with patch('google.cloud.bigquery.client.Client.get_table') as table:
                TableWithNumRows = namedtuple('TableWithId', 'num_rows')
                fake_table = TableWithNumRows(0)
                table.return_value = fake_table

                yield fake_instance, load_table_from_uri, table


if __name__ == '__main__':
    pytest.main()
