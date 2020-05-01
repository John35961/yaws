import os
from dotenv import load_dotenv

load_dotenv(override=True)


class Config(object):
    DEBUG = False

    OPWM_API_KEY = os.getenv("OPWM_API_KEY")
    TIMEZONEDB_API_KEY = os.getenv("TIMEZONEDB_API_KEY")
    AIRQUALITY_API_KEY = os.getenv("AIRQUALITY_API_KEY")


class ProductionConfig(Config):
    DEBUG = False
    ENV = "production"


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"