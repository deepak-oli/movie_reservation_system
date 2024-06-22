import os

from dotenv import load_dotenv
load_dotenv()

class Envs:
    # Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    # Database
    DB_URL = os.getenv("DB_URL")
    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB: int = int(os.getenv("REDIS_DB", 0))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    # Email
    MAIL_USERNAME:str = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD:str = os.getenv("MAIL_PASSWORD", "")
    MAIL_FROM:str = os.getenv("MAIL_FROM","")
    MAIL_PORT:int = int(os.getenv("MAIL_PORT", 0))
    MAIL_SERVER:str = os.getenv("MAIL_SERVER", "")
    SECURITY_PASSWORD_SALT:str = os.getenv("SECURITY_PASSWORD_SALT","")

    FRONTEND_URL:str = os.getenv("FRONTEND_URL","")

envs = Envs()