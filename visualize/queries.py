import pandas
from google.cloud import bigquery


def table_to_df(table_name: str) -> pandas.DataFrame:
    client = bigquery.Client()
    query_job = client.query(
        f"""
        SELECT *
        FROM `{client.project}.dataset.{table_name}` 
        LIMIT 1000
        """
    )

    results = query_job.result()  # Waits for job to complete.

    return results.to_dataframe()
