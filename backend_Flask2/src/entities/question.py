# coding=utf-8

from sqlalchemy import Column, String, ForeignKey, Integer

from .entity import Entity, Base
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields
from . import answer
from . import grade


class Question(Entity, Base):
    __tablename__ = 'questions'
    text_question = Column(String(255))

    answers = relationship("Answer", backref="questions")

    def __init__(self, text_question):
        Entity.__init__(self)
        self.text_question = text_question


class QuestionSchema(Schema):
    id = fields.Number()
    text_question = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
