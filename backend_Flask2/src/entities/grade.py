
from sqlalchemy import Column, String, ForeignKey, Integer , Float
from marshmallow import Schema, fields
from .entity import Entity, Base
from sqlalchemy.orm import relationship
from . import question
from . import student






class Grade(Entity, Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    answer_id = Column(Integer, ForeignKey('answers.id'))
    student_id = Column(Integer, ForeignKey('students.id'))
    score = Column(Float)

    def __init__(self, score, answer_id, student_id):
        Entity.__init__(self)
        self.score = score
        self.answer_id = answer_id
        self.student_id= student_id

class GradeSchema(Schema):
    id = fields.Integer()
    student_id= fields.Integer()
    score=fields.Float()
    answer_id=fields.Integer()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
