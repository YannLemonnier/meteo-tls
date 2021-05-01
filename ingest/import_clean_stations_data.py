import io
from typing import Any, Mapping

import pandas

from ingest.import_toulouse_dataset import ImportToulouseDataset


class ImportCleanStationsData(ImportToulouseDataset):
    @property
    def dataset_stream(self):
        tmp_df = self.clean_url_stream()

        data_stream = io.StringIO()
        tmp_df.to_csv(data_stream, index=False)

        data_stream.seek(0)

        return data_stream

    def clean_url_stream(self) -> pandas.DataFrame:
        self.check_header()

        data_types = self.get_dtypes()

        tmp_df = self.get_url_as_dataframe(nb_rows=None)

        id_number = int(self.destination_name[:2])

        check_id = tmp_df.id == id_number
        try:
            check_temperature = tmp_df.temperature > -20
        except AttributeError:
            check_temperature = tmp_df.temperature_en_degre_c > -20
        check_station_type = tmp_df.type_de_station != 'sous-station'
        clean_check = check_id & check_temperature & check_station_type

        tmp_df = tmp_df.where(clean_check).dropna()
        tmp_df = tmp_df.astype(data_types)
        return tmp_df

    def check_header(self):
        header = self.get_url_as_dataframe(nb_rows=0).columns.to_list()
        if len(header) != 15:
            raise ValueError('Header has wrong length!')

    def get_dtypes(self) -> Mapping:
        tmp_df = self.get_url_as_dataframe(nb_rows=1)
        data_types = tmp_df.dtypes.to_dict()
        return data_types

    def get_url_as_dataframe(self, nb_rows: Any = None) -> pandas.DataFrame:
        url_stream = super().dataset_stream
        tmp_df = pandas.read_csv(url_stream, nrows=nb_rows)
        url_stream.close()
        return tmp_df
