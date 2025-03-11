from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Groups(Base):
    __tablename__ = 'groups'
    name = Column(String(), primary_key=True)


class Students(Base):
    __tablename__ = 'students'
    student_id = Column(Integer(), primary_key=True)
    group_id = Column(String())
    first_name = Column(String())
    last_name = Column(String())


class Courses(Base):
    __tablename__ = 'courses'
    course_id = Column(Integer(), primary_key=True)
    name = Column(String())
    description = Column(String)
