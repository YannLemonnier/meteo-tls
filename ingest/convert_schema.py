import json
from pathlib import Path

from gbqschema_converter.jsonschema_to_gbqschema import json_representation as converter


class ConvertSchema:
    """
        The purpose of this class is to convert a json schema gathered from https://data.toulouse-metropole.fr/ into a
        json representation that will be used in bigquery.
        See schema sub folder for available schema.
        :param schema_name: filename radical between 'schema-' and '.json'
    """
    schema_folder = Path(__file__).parent.parent / 'schema'

    def __init__(self, schema_name: str):
        self.schema_name = schema_name

    @property
    def bq_schema(self) -> list:
        schema_in = self.original_schema['definitions'][f'{self.schema_name}_records']['properties']['fields']
        return converter(schema_in)

    @property
    def original_schema(self):
        try:
            with open(self.schema_file, encoding='utf-8') as schema_file_reader:
                return json.load(schema_file_reader)

        except FileNotFoundError:
            raise FileNotFoundError('Invalid schema filename provided. See schema sub folder for available schema')

    @property
    def schema_file(self):
        return self.schema_folder / f'schema-{self.schema_name}.json'
