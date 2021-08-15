from os import getenv, path
from dotenv import load_dotenv

APP_ROOT = path.join(path.dirname(__file__), '.')   # refers to application_top
dotenv_path = path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)



logging_config = {
    "dev":{
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "simple": {
                "format": "%(message)s"
            },
            "extended": {
                'format': '[{asctime}] : [{levelname}] : [PATH: {name}.{module}.{funcName}] : [lineno: {lineno}] : {message}',
                'style': '{',
            },
            "json": {
                "format": "name: {name}.{module}.{funcName} lineno: {lineno}, level: {levelname}, time: {asctime}, message: {message}",
                'style': '{'
                }
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "REQUEST_DEBUG",
                "formatter": "extended",
                "stream": "ext://sys.stdout"
            },
        },
        'loggers': {
            'gunicorn.error': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            }
        },

        "root": {
            "level": "DEBUG",
            "handlers": ["console"]
        }
    },
    "prod":{
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(message)s"
            },
            "extended": {
                'format': '[{asctime}] : [{levelname}] : [PATH: {name}.{module}.{funcName}] : [lineno: {lineno}] : {message}',
                'style': '{',
            },
            "json": {
                "format": "name: {name}.{module}.{funcName} lineno: {lineno}, level: {levelname}, time: {asctime}, message: {message}",
                'style': '{'
                }
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "REQUEST_DEBUG",
                "formatter": "extended",
                "stream": "ext://sys.stdout"
            },
            "custom_handler": {
                "level": "REQUEST_DEBUG",
                "class": "watchtower.CloudWatchLogHandler",
                "boto3_session": "",
                "log_group": "service_name_logs",
                "stream_name": "REQUEST_DEBUG",
                "formatter": "extended"
            },

            "info_file_handler": {
                "level": "INFO",
                "class": "watchtower.CloudWatchLogHandler",
                "boto3_session": "",
                "log_group": "service_name_logs",
                "stream_name": "info",
                "formatter": "extended"
            },
            "debug_file_handler": {
                "level": "DEBUG",
                "class": "watchtower.CloudWatchLogHandler",
                "boto3_session": "",
                "log_group": "service_name_logs",
                "stream_name": "debug",
                "formatter": "extended"
            },
            

            "error_file_handler": {
                "level": "ERROR",
                "class": "watchtower.CloudWatchLogHandler",
                "boto3_session": "",
                "log_group": "service_name_logs",
                "stream_name": "error",
                "formatter": "extended"
            }
            
        },
        'loggers': {
            'gunicorn.error': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            }
        },

        "root": {
            "level": "DEBUG",
            "handlers": ["error_file_handler", "custom_handler","console"]
        }
    }
}


class Config(object):

    DEPLOY_ENV = getenv('RUN_ENV','dev')

    SERVER_PORT = getenv('SERVER_PORT','9001')

    BOTO3_ACCESS_KEY = getenv('AWS_ACCESS_KEY')
    
    BOTO3_SECRET_KEY = getenv('AWS_SECRET_KEY')

    BOTO3_REGION = getenv('AWS_REGION')
    
    REDIS_HOST = getenv('REDIS_HOST')

    REDIS_PASSWORD = getenv('REDIS_PASSWORD')

    REDIS_PORT = getenv('REDIS_PORT')

    REDIS_DB = getenv('REDIS_DATABASE')

    REDIS_URL = getenv('REDIS_URL')

    RABBITMQ_URI = getenv('RABBITMQ_URI')
    
    SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI')
    
    LOGGING_CONFIG = logging_config[getenv('RUN_ENV','dev')]

    


