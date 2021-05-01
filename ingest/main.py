from ingest.ingest_to_bigquery import ingest_station_description, ingest_station_data

from ingest.initiate_dataset import initiate_dataset


def start_ingest():
    stage_dataset = initiate_dataset()
    ingest_station_description(stage_dataset)

    raw_table = 'stations'
    ingest_station_data(stage_dataset, raw_table)


if __name__ == "__main__":
    start_ingest()
