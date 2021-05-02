from unittest.mock import patch

import pandas
import numpy
import pytest

from ingest.import_clean_stations_data import ImportCleanStationsData


class TestImportCleanStationsData:
    @pytest.fixture
    def small_dataset_import(self):
        yield ImportCleanStationsData('13-station-meteo-toulouse-pech-david')

    def test_check_header_raise_error(self):
        with patch('ingest.import_clean_stations_data.ImportCleanStationsData.get_url_as_dataframe') as get_df:
            df = pandas.DataFrame(columns=[range(40)])
            get_df.return_value = df
            with pytest.raises(ValueError, match='Header has wrong length!'):
                ImportCleanStationsData('fake').check_header()

    def test_get_dtypes_return_dict_with_types(self):
        with patch('ingest.import_clean_stations_data.ImportCleanStationsData.get_url_as_dataframe') as get_df:
            df = pandas.DataFrame([[1, 'test']], columns=['id', 'name'])
            get_df.return_value = df
            data_types = ImportCleanStationsData('fake').get_dtypes()

        assert all(isinstance(dtype, numpy.dtype) for dtype in data_types.values())

    def test_get_url_as_dataframe_return_dataframe(self, small_dataset_import):
        result = small_dataset_import.get_url_as_dataframe(nb_rows=3)
        assert isinstance(result, pandas.DataFrame)

    @pytest.fixture
    def bad_dataset(self, small_dataset_import):
        tmp_df = small_dataset_import.get_url_as_dataframe(nb_rows=700)
        tmp_df.loc[-3, 'id'] = numpy.NaN
        tmp_df.loc[-4, 'temperature'] = -50.0
        tmp_df.loc[-5, 'type_de_station'] = 'sous-station'
        yield tmp_df

    @pytest.fixture
    def setup_clean_bad_dataset(self, small_dataset_import, bad_dataset):
        data_types = small_dataset_import.get_dtypes()
        with patch('ingest.import_clean_stations_data.ImportCleanStationsData.get_dtypes') as get_dtypes:
            get_dtypes.return_value = data_types

            with patch('ingest.import_clean_stations_data.ImportCleanStationsData.get_url_as_dataframe') as get_df:
                get_df.return_value = bad_dataset
                result = ImportCleanStationsData('13-fake').clean_url_stream()
        yield data_types, len(bad_dataset), result

    def test_correct_bad_values(self, setup_clean_bad_dataset):
        _, original_len, result = setup_clean_bad_dataset
        assert len(result) != original_len

    def test_correct_bad_dtypes(self, setup_clean_bad_dataset):
        expected_dtypes, _, result = setup_clean_bad_dataset
        assert result.dtypes.to_dict() == expected_dtypes


if __name__ == '__main__':
    pytest.main()
