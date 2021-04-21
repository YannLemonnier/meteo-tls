import google.api_core
from google.cloud import bigquery


def initiate_dataset():
    # Construct a BigQuery client object.
    client = bigquery.Client()

    dataset_id = "{}.dataset".format(client.project)

    # Construct a full Dataset object to send to the API.
    dataset = bigquery.Dataset(dataset_id)

    dataset.location = "EU"

    # Send the dataset to the API for creation, with an explicit timeout.
    # Raises google.api_core.exceptions.Conflict if the Dataset already
    # exists within the project.
    try:
        dataset = client.create_dataset(dataset, timeout=30)  # Make an API request.
        print("Created dataset {}.{}".format(client.project, dataset.dataset_id))
    except google.api_core.exceptions.Conflict:
        pass

    return dataset.dataset_id
