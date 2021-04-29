from typing import Union, List

from convert_schema import ConvertSchema
from import_gs_file_in_bq import ImportGsFileInBq
from import_toulouse_dataset import ImportToulouseDataset
from queries import table_to_df


def ingest_station_description(dataset: str):
    table = 'stations-meteo-en-place'
    ingest_open_data_in_dataset_table_given_schema(open_dataset=table, dataset=dataset, table=table, schema=table)


def ingest_station_data(dataset: str):
    stations_info = table_to_df('stations-meteo-en-place')
    list_of_datasets = stations_info['id_nom'].to_list()

    table = 'stations'
    schema = '58-station-meteo-toulouse-fondeyre'

    ingest_open_data_in_dataset_table_given_schema(list_of_datasets, dataset, table, schema)


def ingest_open_data_in_dataset_table_given_schema(open_dataset: Union[str, List[str]], dataset: str, table: str,
                                                   schema: str):
    if isinstance(open_dataset, str):
        open_dataset = [open_dataset]

    uris = []
    for open_data in open_dataset:
        file_blob = ImportToulouseDataset(open_data).upload()
        uri = f'gs://{file_blob.bucket.name}/{file_blob.name}'
        uris.append(uri)

    my_schema = ConvertSchema(schema).bq_schema
    import_session = ImportGsFileInBq(dataset, table, my_schema)

    import_session.load(uris)


if __name__ == '__main__':
    ingest_station_data('dataset')
