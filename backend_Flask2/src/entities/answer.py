
from sqlalchemy import Column, String, ForeignKey, Integer
from marshmallow import Schema, fields
from .entity import Entity, Base
from sqlalchemy.orm import relationship
from . import question
from . import student



    
class Answer(Entity, Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    text_answer = Column(String(255))
    # les relations
    question_id = Column(Integer, ForeignKey('questions.id'))
    student_id = Column(Integer, ForeignKey('students.id'))
    grades = relationship("Grade", backref="answers")

   

    def __init__(self, text_answer, question_id ,student_id):
        Entity.__init__(self)
        self.text_answer = text_answer
        self.question_id = question_id
        self.student_id = student_id

class AnswerSchema(Schema):
    id = fields.Integer(dump_only=True)
    text_answer = fields.Str()
    question_id= fields.Integer()
    student_id=fields.Integer()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
