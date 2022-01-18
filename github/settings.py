import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

URL = os.environ.get("URL")

APPLICATION_NAME = os.environ.get("APPLICATION_NAME")

SERVER = {
    'host': os.environ.get("SERVER_HOST"),
    'port': int(os.environ.get("SERVER_PORT"))
}

RABBITMQ = os.environ.get("RABBITMQ_HOST")

DB = {
    'name': os.environ.get("DATABASE_NAME"),
    'host': os.environ.get("DATABASE_HOST"),
    'port': int(os.environ.get("DATABASE_PORT"))
}

APPLICATION_TOKEN = os.environ.get("APPLICATION_TOKEN")

USERS_COLLECTION_NAME = os.environ.get("USERS_COLLECTION_NAME")

HAWK_CATCHER_SETTINGS = None
