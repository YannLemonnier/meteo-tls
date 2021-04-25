from .convert_schema import ConvertSchema
from .import_gs_file_in_bq import ImportGsFileInBq
from .import_toulouse_dataset import ImportToulouseDataset


def ingest_station_description(dataset: str):
    table = 'stations-meteo-en-place'

    stations = ImportToulouseDataset(table).upload()
    uri = f'gs://{stations.bucket.name}/{stations.name}'

    my_schema = ConvertSchema(table).bq_schema
    import_session = ImportGsFileInBq(dataset, table, my_schema)

    import_session.load(uri)
