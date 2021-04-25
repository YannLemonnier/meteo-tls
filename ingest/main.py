from ingest.ingest_station_description import ingest_station_description

from ingest.initiate_dataset import initiate_dataset


def main(data, context):
    stage_dataset = initiate_dataset()
    ingest_station_description(stage_dataset)


if __name__ == "__main__":
    main('data', 'context')
