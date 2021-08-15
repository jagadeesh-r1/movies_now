# third-party imports
import os
import logging.config
from flask import Flask
from boto3.session import Session

from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# local imports
from app.models.db_base import Base
# from app.models.cities import Cities
# from app.models.users import Users
# from app.models.city_movie_map import CityMovieMap
# from app.models.movie_theaters import MovieTheaters
# from app.models.movies import Movies
# from app.models.screens import Screens
# from app.models.show_seats import ShowSeats
# from app.models.shows import Shows
# from app.models.booking import Booking
# from app.models.city_movie_map import Booking

from config import Config

redis = FlaskRedis()
db = SQLAlchemy()


def get_session(url):
    engine = create_engine(url, pool_pre_ping=True)
    Session = sessionmaker(bind = engine)
    session = Session()
    return session

def create_tables(url, table_name="products"):
    engine = create_engine(url, pool_pre_ping=True)
    Base.metadata.create_all(engine, [Base.metadata.tables[table_name]],checkfirst=True)

    
DEBUG_LEVELV_NUM = 35

logging.addLevelName(DEBUG_LEVELV_NUM, "REQUEST_DEBUG")


def custom_debug(self, message, *args, **kws):
    if self.isEnabledFor(DEBUG_LEVELV_NUM):
        # Yes, logger takes its '*args' as 'args'.
        self._log(DEBUG_LEVELV_NUM, message, args, **kws)
     

logging.Logger.request_debug = custom_debug

# create_tables(Config.SQLALCHEMY_DATABASE_URI,Cities.__tablename__)
# create_tables(Config.SQLALCHEMY_DATABASE_URI,Users.__tablename__)
# create_tables(Config.SQLALCHEMY_DATABASE_URI,Movies.__tablename__)
# create_tables(Config.SQLALCHEMY_DATABASE_URI,CityMovieMap.__tablename__)
# create_tables(Config.SQLALCHEMY_DATABASE_URI,MovieTheaters.__tablename__)
# create_tables(Config.SQLALCHEMY_DATABASE_URI,Screens.__tablename__)
# create_tables(Config.SQLALCHEMY_DATABASE_URI,Shows.__tablename__)
# create_tables(Config.SQLALCHEMY_DATABASE_URI,ShowSeats.__tablename__)
# create_tables(Config.SQLALCHEMY_DATABASE_URI,Booking.__tablename__)


def create_app():
    app = Flask(__name__, instance_relative_config=True, root_path=os.path.join(os.getcwd(), 'app'))
    app.config.from_object(Config)
    
    redis.init_app(app)
    db.init_app(app)
    
    boto3_session = Session(
            aws_access_key_id = Config.BOTO3_ACCESS_KEY, 
            aws_secret_access_key = Config.BOTO3_SECRET_KEY,
            region_name = Config.BOTO3_REGION
        )

    if Config.DEPLOY_ENV != 'dev':    
        for handler_type in [ "custom_handler", "info_file_handler", "debug_file_handler", "error_file_handler" ]:
            Config.LOGGING_CONFIG["handlers"][handler_type]["boto3_session"] = boto3_session
        
    logging.config.dictConfig(Config.LOGGING_CONFIG)
    logger = logging.getLogger(__name__)
    logger.request_debug("Logs Setuped in Region us-east-2")

    from app.routes import blueprints

    for route_blueprint in blueprints:
        app.register_blueprint(route_blueprint, url_prefix='/api/movies-now') 
        
    return app
