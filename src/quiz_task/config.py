import os

import sqlalchemy
import sqlalchemy.ext.asyncio


def get_postgres_connection_url() -> str:
    """Returns postgresql database connection url"""
    # Using environ[...] instead of environ.get(...) to raise exception
    # in case of missing some of the crucial variables
    db_name = os.environ['POSTGRES_DB']
    username = os.environ['POSTGRES_USER']
    password = os.environ['POSTGRES_PASSWORD']
    host = os.environ.get('POSTGRES_HOST', '127.0.0.1')
    port = os.environ.get('POSTGRES_PORT', '5432')
    connection_url = f'postgresql+asyncpg://{username}:{password}@{host}:{port}/{db_name}'
    return connection_url
