from .db_base import MySqlBase
from app.models.cities import Cities
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, TIMESTAMP,Integer,ForeignKey

class Users(MySqlBase):

    __tablename__ = 'users'
    user_id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    username = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True)
    phone = Column(String,nullable=False)
    city_id = Column(Integer,ForeignKey('cities.city_id'))
    city = relationship(Cities)
