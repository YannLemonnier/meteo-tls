from typing import Union, List

from ingest.import_clean_stations_data import ImportCleanStationsData
from ingest.convert_schema import ConvertSchema
from ingest.import_gs_file_in_bq import ImportGsFileInBq
from ingest.import_toulouse_dataset import ImportToulouseDataset
from ingest.queries import table_to_df


def ingest_station_description(dataset: str):
    table = 'stations-meteo-en-place'
    file_blob = ImportToulouseDataset(table).upload()
    uri = f'gs://{file_blob.bucket.name}/{file_blob.name}'

    load_in_bigquery(uris=uri, dataset=dataset, table=table, schema=table)


def ingest_station_data(dataset: str, table: str):
    stations_info = table_to_df('stations-meteo-en-place')
    list_of_datasets = stations_info['id_nom'].to_list()

    schema = '14-station-meteo-toulouse-centre-pierre-potier'
    uris = load_in_gcs(list_of_datasets)

    load_in_bigquery(uris, dataset, table, schema)


def load_in_bigquery(uris: Union[str, List[str]], dataset: str, table: str,
                     schema: str):
    my_schema = ConvertSchema(schema).bq_schema
    import_session = ImportGsFileInBq(dataset, table, my_schema)

    print('Import in BigQuery')
    import_session.load(uris)


def load_in_gcs(open_dataset):
    if isinstance(open_dataset, str):
        open_dataset = [open_dataset]
    uris = []
    for open_data in open_dataset:
        try:
            print(f'Loading: {open_data}')
            file_blob = ImportCleanStationsData(open_data).upload()
            uri = f'gs://{file_blob.bucket.name}/{file_blob.name}'
            uris.append(uri)
        except ValueError:
            print(f'failed')
    return uris


if __name__ == '__main__':
    ingest_station_data('dataset', 'raw_stations')
