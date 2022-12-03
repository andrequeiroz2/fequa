from dotenv import find_dotenv, load_dotenv
from pydantic import BaseSettings
import os
from functools import lru_cache


class Settings(BaseSettings):

    load_dotenv(find_dotenv(".env"), override=True)

    HOST = os.environ.get("HOST")
    PORT = int(os.environ.get("PORT"))
    LOGLEVEL = os.environ.get("LOGLEVEL")
    APITITLE = os.environ.get("APITITLE")
    DEBUG = os.environ.get("DEBUG")

    DBDIALECT = os.environ.get("DBDIALECT")
    DBHOST = os.environ.get("DBHOST")
    DBUSER = os.environ.get("DBUSER")
    DBPASSWORD = os.environ.get("DBPASSWORD")
    DBPORT = int(os.environ.get("DBPORT"))
    DBBASE = os.environ.get("DBBASE")

    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALGORITHM = os.environ.get("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))


@lru_cache
def settings_get() -> Settings:
    return Settings()


settings = settings_get()