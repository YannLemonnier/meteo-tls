from typing import Union, Iterable

from google.cloud import bigquery
import google.api_core.exceptions


class ImportGsFileInBq:
    """
    This class enable to load data in csv from google storage into a bigquery table.
    :param dataset_name: An existing dataset name in the current project
    :param table_name: A name for a table to load data into (created if needed)
    :param schema: A google schema representing fields to load in database
    """

    def __init__(self, dataset_name: str, table_name: str, schema: list):
        self.dataset_name = dataset_name
        self.table_name = table_name
        self.schema = schema

        self.client = bigquery.Client()

    @property
    def table(self):
        return f"{self.client.project}.{self.dataset_name}.{self.table_name}"

    def load(self, uris: Union[str, Iterable[str]]):
        """
        The load method will load google storage csv file into the table.
        :param uris: Could be a single URI or a list of URIs and even use wildcard after bucket separator like
        gs://meteo-tls/data-station/*.csv
        :return: Nothing
        """

        self.__check_table()

        load_job = self.client.load_table_from_uri(
            uris, self.table, job_config=self.job_config
        )  # Make an API request.
        load_job.result()  # Waits for the job to complete.
        destination_table = self.client.get_table(self.table)  # Make an API request.
        print("Loaded {} rows.".format(destination_table.num_rows))

    def __check_table(self):
        available_tables = self.client.list_tables(self.dataset_name)
        if self.table_name not in [table.table_id for table in available_tables]:
            self.create_table_with_schema()

    def create_table_with_schema(self):
        table_ref = bigquery.Table(self.table, schema=self.schema)

        try:
            table = self.client.create_table(table_ref)  # Make an API request.
            print(
                f"Created table {table.project}.{table.dataset_id}.{table.table_id}"
            )
        except google.api_core.exceptions.Conflict:
            pass

    @property
    def job_config(self):
        return bigquery.LoadJobConfig(
            schema=self.schema,
            skip_leading_rows=1,
            # The source format defaults to CSV, so the line below is optional.
            source_format=bigquery.SourceFormat.CSV
        )
