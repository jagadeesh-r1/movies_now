from os import name
from app.models.users import Users
from app.models.shows import Shows
from sqlalchemy.orm import relationship
from app.models.db_base import MySqlBase
from sqlalchemy import Column, Integer,ForeignKey,Boolean,DateTime,Enum,TIMESTAMP


class Booking(MySqlBase):

    __tablename__ = 'booking'
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    user_id = Column(Integer,ForeignKey('users.user_id'))
    show_id = Column(Integer,ForeignKey('shows.show_id'))
    no_of_seats = Column(Integer,nullable=False)
    timestamp = Column(TIMESTAMP,nullable=False)
    status = Column(Enum("Confirmed","Not Confirmed",name="status"),nullable=False)
    user = relationship(Users)
    show = relationship(Shows)