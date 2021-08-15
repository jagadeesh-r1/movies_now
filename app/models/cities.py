from app.models.db_base import MySqlBase
from sqlalchemy import Column, String, TIMESTAMP,Integer

class Cities(MySqlBase):

    __tablename__ = 'cities'
    city_id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    name = Column(String,nullable=False)