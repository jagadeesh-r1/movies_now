from .cities import Cities
from sqlalchemy.orm import relationship
from app.models.db_base import MySqlBase
from sqlalchemy import Column, String, TIMESTAMP,Integer,ForeignKey,Boolean

class MovieTheaters(MySqlBase):

    __tablename__ = 'movie_theaters'
    theater_id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    theater_name = Column(String,nullable=False)
    city_id = Column(Integer,ForeignKey('cities.city_id'))
    total_screens = Column(Integer,nullable=False)
    city = relationship(Cities)