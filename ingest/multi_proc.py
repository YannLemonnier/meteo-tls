import multiprocessing
from multiprocessing import Pool

from ingest.ingest_to_bigquery import load_in_gcs, load_in_bigquery
from ingest.queries import table_to_df


def ingest_station_data_mp(dataset: str, table: str):
    stations_info = table_to_df('stations-meteo-en-place')
    list_of_datasets = stations_info['id_nom'].to_list()

    schema = '14-station-meteo-toulouse-centre-pierre-potier'
    with Pool(multiprocessing.cpu_count() - 2) as p:
        uris = p.map(load_in_gcs, list_of_datasets)
    uris = [uri[0] for uri in uris if len(uri) > 0]

    load_in_bigquery(uris, dataset, table, schema)


if __name__ == '__main__':
    ingest_station_data_mp('dataset', 'raw_stations')
