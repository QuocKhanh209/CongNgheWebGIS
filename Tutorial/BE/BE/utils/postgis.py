import os

def get_parmas():
    return dict(
        db = os.environ.get('POSTGRES_DB'),
        host = os.environ.get('PG_HOST'),
        port = os.environ.get('PG_PORT'),
        pg_user = os.environ.get('POSTGRES_USER'),
        pg_password = os.environ.get('POSTGRES_PASSWORD'),
    )