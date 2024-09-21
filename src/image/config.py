import os


def get_postgres_uri():
    host = os.environ.get("DB_HOST", "db")
    port = 5433 if host == "localhost" else 5432
    password = os.environ.get("DB_PASSWORD", "password")
    user = os.environ.get("DB_USER", "postgres")
    db_name = os.environ.get("DB_NAME", "image")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 8000 if host == "localhost" else 8000
    return f"http://{host}:{port}"


def get_redis_host_and_port():
    host = os.environ.get("REDIS_HOST", "redis")
    port = 6379 if host == "localhost" else 6379
    return dict(host=host, port=port)


REDIS_CHANNEL = "image_saved"

IMAGE_FILES_PATH = "image_files"
