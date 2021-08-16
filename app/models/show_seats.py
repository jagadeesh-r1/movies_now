from os import name
from app.models.shows import Shows
from app.models.movies import Movies
from app.models.screens import Screens
from sqlalchemy.orm import relationship
from app.models.db_base import MySqlBase
from sqlalchemy import Column, Integer,ForeignKey,Boolean,DateTime,Enum

'''
Currently commenting out this model due to complexity it adds to complete the assignment.
'''


# class ShowSeats(MySqlBase):

    # __tablename__ = 'show_seats'

    # seat_id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    # screen_id = Column(Integer,ForeignKey('screens.screen_id'))
    # movie_id = Column(Integer,ForeignKey('movies.movie_id'))
    # show_id = Column(Integer,ForeignKey('shows.show_id'))
    # price = Column(Integer,nullable=False)
    # status = Column(Enum("Available","Not Available",name="availability"),nullable=False)
    # screen = relationship(Screens)
    # movie = relationship(Movies)
    # show = relationship(Shows)