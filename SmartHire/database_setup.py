import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Candidates(Base):
    __tablename__ = 'candidates'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    gender = Column(String(64), nullable=True)
    school = Column(String(128), nullable=True)
    degree = Column(String(128), nullable=True)
    resume = Column(Text, nullable=False)

class ResumeData(Base):
    __tablename__ = 'resume_data'
    id = Column(Integer, ForeignKey('candidates.id'), primary_key=True)
    keywords = Column(ARRAY(String), nullable=False)
    concepts = Column(ARRAY(String), nullable=False)

class DescriptionData(Base):
    __tablename__ = 'job_description_data'
    id = Column(Integer, primary_key=True)
    keywords = Column(ARRAY(String), nullable=False)
    concepts = Column(ARRAY(String), nullable=False)


engine = create_engine('sqlite:///matching.db')
Base.metadata.create_all(engine)

