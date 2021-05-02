import pandas
from google.cloud import bigquery


def table_to_df(table_name: str) -> pandas.DataFrame:
    client = bigquery.Client()
    query = f"""
        SELECT *
        FROM `{client.project}.dataset.{table_name}`
        WHERE emission = 'V'
        LIMIT 1000
        """

    return query_to_df(query, client)


def get_avg_temp_to_df(station_table: str, data_table: str) -> pandas.DataFrame:
    client = bigquery.Client()
    query = f"""
        WITH temp_data AS (
            SELECT id, ROUND(AVG(temperature_en_degre_c),1) as temperature, COUNT(*) as cnt
            FROM `{client.project}.dataset.{data_table}`
            group by id) 
        
        select id_nom, temperature, longitude, latitude
        FROM `{client.project}.dataset.{station_table}` as stations
        join temp_data on stations.id_numero = temp_data.id
        WHERE cnt > 40000
        """

    return query_to_df(query, client)


def get_all_temp_to_df(station_table: str, data_table: str) -> pandas.DataFrame:
    client = bigquery.Client()
    query = f"""
        WITH temp_data AS (SELECT id,
                ROUND(AVG(temperature_en_degre_c),1) as temperature, 
                COUNT(*) as cnt, 
                extract(hour FROM heure_de_paris) as hour,
                extract(date FROM heure_de_paris) as date,
            FROM `{client.project}.dataset.{data_table}`
            group by hour, date, id
            order by date desc, hour desc) 

        SELECT id_nom, temperature, longitude, latitude, altitude, DATETIME(date, TIME(hour, 0,0)) as datetime
            FROM `{client.project}.dataset.{station_table}` as stations
            join temp_data on stations.id_numero = temp_data.id
        """

    return query_to_df(query, client)


def get_temp_from_date_to_df(station_table: str, data_table: str, date: str) -> pandas.DataFrame:
    client = bigquery.Client()
    query = f"""
        WITH temp_data AS (SELECT id,
                ROUND(AVG(temperature_en_degre_c),1) as temperature, 
                COUNT(*) as cnt, 
                extract(hour FROM heure_de_paris) as hour,
                extract(date FROM heure_de_paris) as date,
            FROM `{client.project}.dataset.{data_table}`
            group by hour, date, id
            order by date desc, hour desc) 

        SELECT id_nom, temperature, longitude, latitude, altitude, DATETIME(date, TIME(hour, 0,0)) as datetime
            FROM `{client.project}.dataset.{station_table}` as stations
            join temp_data on stations.id_numero = temp_data.id
            WHERE DATETIME(date, TIME(hour, 0,0)) = \'{date}\'
        """

    return query_to_df(query, client)


def get_std_by_date_hour(data_table: str):
    client = bigquery.Client()
    query = f"""
        WITH temp_data AS (SELECT ROUND(AVG(temperature_en_degre_c),1) as temperature, 
                ROUND(STDDEV(temperature_en_degre_c),2) as std, 
                COUNT(*) as cnt, 
                extract(hour FROM heure_de_paris) as hour,
                extract(date FROM heure_de_paris) as date,
            FROM `{client.project}.dataset.{data_table}`
            GROUP BY hour, date)
        SELECT DATETIME(date, TIME(hour, 0,0)) as datetime, std, temperature
        FROM temp_data
        WHERE cnt > 50
        ORDER BY datetime
        """

    return query_to_df(query, client)


def query_to_df(query: str, client: bigquery.Client) -> pandas.DataFrame:
    query_job = client.query(query)
    results = query_job.result()  # Waits for job to complete.

    return results.to_dataframe()
