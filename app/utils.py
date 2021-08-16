
import logging
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def catch_exceptions(func):
    '''
    This decoretor wraps fuction to catch any exceptions and log them. 
    '''
    def wrapped_function(*args, **kargs):
        try:
            return func(*args, **kargs)
        except Exception as e:
            l = logging.getLogger(func.__name__)
            l.error(e, exc_info=True)
            return None                
    return wrapped_function

def get_session(url : str):
    '''
    Creates a session with the DataBase.
    '''
    engine = create_engine(url, pool_pre_ping=True)
    Session = sessionmaker(bind = engine)
    session = Session()
    return session