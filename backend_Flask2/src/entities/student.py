from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, Integer
from marshmallow import Schema, fields
from .entity import Entity, Base
from . import answer
from . import grade


class Student(Entity, Base):
    __tablename__ = 'students'
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255))
    
    answers = relationship("Answer", backref="students")
    grades = relationship("Grade", backref="students")

    def __init__(self, first_name,last_name,email):
        Entity.__init__(self)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

class StudentSchema(Schema):
    id = fields.Integer()
    first_name = fields.Str()
    last_name=fields.Str()
    email=fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
