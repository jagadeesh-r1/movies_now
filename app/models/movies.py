from app.models.db_base import MySqlBase
from sqlalchemy import Column, String, TIMESTAMP,Integer,DateTime


class Movies(MySqlBase):

    __tablename__ = 'movies'
    movie_id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    movie_title = Column(String,nullable=False)
    description = Column(String,nullable=False)
    duration = Column(Integer,nullable=False)
    language = Column(String,nullable=False)
    release_date = Column(DateTime,nullable=False)
    genre = Column(String,nullable=False)