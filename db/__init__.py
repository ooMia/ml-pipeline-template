import os
import sys

from dotenv import load_dotenv

sys.path.append(os.path.dirname(__file__))

load_dotenv()

MYSQL_ROOT_PASSWORD: str = os.getenv('MYSQL_ROOT_PASSWORD')
MYSQL_DATA_DIR: str = os.getenv('MYSQL_DATA_DIR')

MYSQL_HOST: str = os.getenv('MYSQL_HOST')
MYSQL_PORT: int = int(os.getenv('MYSQL_PORT'))
MYSQL_DATABASE: str = os.getenv('MYSQL_DATABASE')

MYSQL_USER: str = os.getenv('MYSQL_USER')
MYSQL_PASSWORD: str = os.getenv('MYSQL_PASSWORD')
