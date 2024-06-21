import os

from dotenv import load_dotenv
load_dotenv()

class Envs:
    DB_URL = os.getenv("DB_URL")

envs = Envs()