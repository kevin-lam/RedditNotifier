import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

HOST = os.getenv("EMAILER_HOST")
PORT = os.getenv("EMAILER_PORT")
EMAIL = os.getenv("EMAILER_EMAIL")
PASSWORD = os.getenv("EMAILER_PASSWORD")
ID = os.getenv("PRAW_ID")
AGENT = os.getenv("PRAW_AGENT")
