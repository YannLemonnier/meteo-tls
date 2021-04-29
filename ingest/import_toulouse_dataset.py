from urllib.error import HTTPError

from google.api_core.exceptions import NotFound
from google.cloud import storage
import urllib.request

from google.cloud.storage import Blob


class ImportToulouseDataset:
    """
    This class is responsible to import toulouse métropole dataset into google cloud storage
    :param toulouse_dataset: name of a dataset available in https://data.toulouse-metropole.fr/
    :param project: a project in google cloud platform
    """

    def __init__(self, toulouse_dataset: str, project: str = None):
        self.toulouse_dataset = toulouse_dataset
        if project is None:
            self.storage_client = storage.Client()
        else:
            self.storage_client = storage.Client(project=project)
        self.project = self.storage_client.project

    def upload(self) -> Blob:
        blob = self.__bucket.blob(self.destination_name)
        blob.upload_from_string(self.dataset_stream.read())
        return blob

    @property
    def __bucket(self):
        try:
            bucket = self.storage_client.get_bucket(self.bucket_name)
        except NotFound:
            raise ValueError('Issues when reaching project bucket. Please check project name')
        return bucket

    @property
    def bucket_name(self):
        return f'{self.project}.appspot.com'

    @property
    def destination_name(self):
        return f'{self.toulouse_dataset}.csv'

    @property
    def dataset_stream(self):
        link = None
        try:
            link = urllib.request.urlopen(self.dataset_url)
        except HTTPError as http_error:
            if http_error.code == 404:
                raise ValueError('Issues when reaching dataset url. Please check dataset name')
        return link

    @property
    def dataset_url(self):
        prefix = 'https://data.toulouse-metropole.fr/explore/dataset/'
        suffix = '/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%2C'
        return f'{prefix}{self.toulouse_dataset}{suffix}'
