from google.cloud import bigquery


def initiate_dataset(dataset_name: str = 'dataset', location: str = 'EU'):
    client = bigquery.Client()

    dataset_id = f'{client.project}.{dataset_name}'

    dataset = bigquery.Dataset(dataset_id)
    dataset.location = location

    available_datasets = [dataset_obj.dataset_id for dataset_obj in client.list_datasets()]
    if dataset_name not in available_datasets:
        dataset = client.create_dataset(dataset, timeout=30)  # Make an API request.
        print("Created dataset {}.{}".format(client.project, dataset.dataset_id))

    return dataset.dataset_id
