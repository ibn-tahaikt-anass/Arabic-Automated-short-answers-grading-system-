from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from marshmallow import Schema, fields

db_url = 'localhost:3306'
db_name = 'online_exam'
db_user = 'root'
db_password = ''
engine = create_engine(f'mysql://{db_user}:{db_password}@{db_url}/{db_name}')
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Entity():
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __init__(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
