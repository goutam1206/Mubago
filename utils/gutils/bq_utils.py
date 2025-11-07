from google.cloud import bigquery
import os

def insert_user_to_bigquery(user_info: dict):
    client = bigquery.Client(project=os.getenv("BQ_PROJECT_ID"))

    dataset_id = os.getenv("BQ_DATASET")
    table_id = os.getenv("BQ_TABLE")
    table_ref = f"{client.project}.{dataset_id}.{table_id}"

    rows_to_insert = [user_info]

    errors = client.insert_rows_json(table_ref, rows_to_insert)
    if errors:
        print("❌ BigQuery insert errors:", errors)
    else:
        print("✅ User inserted successfully into BigQuery.")