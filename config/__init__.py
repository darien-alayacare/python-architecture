import os


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 5000 if host == "localhost" else 80
    return f"http://{host}:{port}"

def get_postgres_uri():
    host = os.environ.get("DB_HOST", "127.0.0.1")
    port = 54321 if host == "localhost" else 5432
    password = os.environ.get("DB_PASSWORD", "2Password!")
    user, db_name = "darien", "allocations"
    uri = f"postgresql://{user}:{password}@{host}/{db_name}"
    return uri