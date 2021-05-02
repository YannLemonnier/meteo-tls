import pandas
from google.cloud import bigquery


def table_to_df(table_name: str) -> pandas.DataFrame:
    client = bigquery.Client()
    query_job = client.query(
        f"""
        SELECT *
        FROM `{client.project}.dataset.{table_name}`
        WHERE emission = 'V'
        LIMIT 1000
        """
    )

    results = query_job.result()  # Waits for job to complete.

    return results.to_dataframe()


def get_temp_to_df(station_table: str, data_table: str) -> pandas.DataFrame:
    client = bigquery.Client()
    query_job = client.query(
        f"""
        with temp_data as (
            SELECT id, ROUND(AVG(temperature_en_degre_c),1) as temp, COUNT(*) as cnt
            FROM `{client.project}.dataset.{data_table}`
            group by id) 
        
        select id_nom, temp_data.temp, stations.longitude, stations.latitude
        FROM `{client.project}.dataset.{station_table}` as stations
        join temp_data on stations.id_numero = temp_data.id
        WHERE cnt > 40000
        """
    )

    results = query_job.result()  # Waits for job to complete.

    return results.to_dataframe()
