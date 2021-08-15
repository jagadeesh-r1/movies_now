from app.models.movies import Movies
from app.models.screens import Screens
from sqlalchemy.orm import relationship
from app.models.db_base import MySqlBase
from sqlalchemy import Column, String, TIMESTAMP,Integer,ForeignKey,Boolean,DateTime

class Shows(MySqlBase):

    __tablename__ = 'shows'
    show_id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    screen_id = Column(Integer,ForeignKey('screens.screen_id'))
    movie_id = Column(Integer,ForeignKey('movies.movie_id'))
    start_time = Column(TIMESTAMP,nullable=False)
    end_time = Column(TIMESTAMP,nullable=False)
    date = Column(DateTime,nullable=False)
    booked_seat_counts = Column(Integer,default=0,nullable=False)
    screen = relationship(Screens)
    movie = relationship(Movies)