from app.models.cities import Cities
from app.models.movies import Movies
from sqlalchemy.orm import relationship
from app.models.db_base import MySqlBase
from sqlalchemy import Column, String, TIMESTAMP,Integer,ForeignKey,Boolean

# from app.models import movies


class CityMovieMap(MySqlBase):

    __tablename__ = 'city_movie_map'
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    city_id = Column(Integer,ForeignKey('cities.city_id'))
    movie_id = Column(Integer,ForeignKey('movies.movie_id'))
    is_active = Column(Boolean,nullable=False)
    city = relationship(Cities)
    movie = relationship(Movies)