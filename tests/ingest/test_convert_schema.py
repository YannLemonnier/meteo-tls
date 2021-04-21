import pytest

from ingest.convert_schema import ConvertSchema


class TestConvertSchema:
    @pytest.fixture
    def schema_stations(self):
        yield ConvertSchema('stations-meteo-en-place').bq_schema

    def test_error_with_invalid_filename(self):
        match_msg = 'Invalid schema filename provided. See schema sub folder for available schema'
        with pytest.raises(FileNotFoundError, match=match_msg):
            _ = ConvertSchema('invalid_name').original_schema

    def test_output_a_list(self, schema_stations):
        assert isinstance(schema_stations, list)

    def test_output_contains_name_field(self, schema_stations):
        assert all('name' in fields.keys() for fields in schema_stations)

    def test_output_contains_type_field(self, schema_stations):
        assert all('type' in fields.keys() for fields in schema_stations)


if __name__ == '__main__':
    pytest.main()
