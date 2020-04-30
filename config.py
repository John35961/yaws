import os


class Config(object):
    DEBUG = False

    OPWM_API_KEY = os.environ["OPWM_API_KEY"]
    TIMEZONEDB_API_KEY = os.environ["TIMEZONEDB_API_KEY"]
    AIRQUALITY_API_KEY = os.environ["AIRQUALITY_API_KEY"]


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True