from dotenv import load_dotenv
import os

load_dotenv()

COUCHDB_URL = os.getenv("COUCHDB_URL")