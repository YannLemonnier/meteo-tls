from flask import Flask

from ingest.ingest_station_description import ingest_station_description

from ingest.initiate_dataset import initiate_dataset

app = Flask(__name__)


@app.route('/')
def start_data_ingestion():
    stage_dataset = initiate_dataset()
    ingest_station_description(stage_dataset)
    return 'Start data ingestion'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
