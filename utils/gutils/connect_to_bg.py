from google.cloud import bigquery
from google.oauth2 import service_account
import os

def connect_bigquery(service_account_path: str, project_id: str):
    """
    Safely connects to Google BigQuery using a service account key file.
    Verifies connectivity by listing datasets (no public data access).
    """
    if not os.path.exists(service_account_path):
        raise FileNotFoundError(f"❌ Service account file not found: {service_account_path}")

    try:
        credentials = service_account.Credentials.from_service_account_file(service_account_path)
        client = bigquery.Client(credentials=credentials, project=project_id)
        # Lightweight internal API call — no data fetched.
        _ = list(client.list_datasets(max_results=1))
        print(f"✅ Connection to BigQuery project '{project_id}' successful!")
        return client
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        raise


if __name__ == "__main__":
    # ---- Configuration ----
    SERVICE_ACCOUNT_PATH = "../../config/credentials/bg-connector.json"
    PROJECT_ID = "x-entropy-477503-f8"

    connect_bigquery(SERVICE_ACCOUNT_PATH, PROJECT_ID)