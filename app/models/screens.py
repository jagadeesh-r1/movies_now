from app.models.db_base import MySqlBase
from sqlalchemy.orm import relationship
from app.models.movie_theaters import MovieTheaters
from sqlalchemy import Column, String, TIMESTAMP,Integer,ForeignKey,Boolean

class Screens(MySqlBase):

    __tablename__ = 'screens'
    screen_id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    screen_name = Column(String,nullable=False)
    theater_id = Column(Integer,ForeignKey('movie_theaters.theater_id'))
    total_seats = Column(Integer,nullable=False)
    city = relationship(MovieTheaters)