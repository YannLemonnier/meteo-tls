from ingest.convert_schema import ConvertSchema
from ingest.import_gs_file_in_bq import ImportGsFileInBq
from ingest.import_toulouse_dataset import ImportToulouseDataset

from ingest.initiate_dataset import initiate_dataset


def ingest_station_description(dataset: str):
    table = 'stations-meteo-en-place'

    stations = ImportToulouseDataset(table).upload()
    uri = f'gs://{stations.bucket.name}/{stations.name}'

    my_schema = ConvertSchema(table).bq_schema
    import_session = ImportGsFileInBq(dataset, table, my_schema)

    import_session.load(uri)


if __name__ == '__main__':
    stage_dataset = initiate_dataset()
    ingest_station_description(stage_dataset)
