"""
SQLAlchemy models for the database
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    """User model for authentication"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    
    # Relationships
    resumes = relationship("Resume", back_populates="user")


class Resume(Base):
    """Resume model to store user resumes"""
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)  # Store the plain text content of the resume
    
    # Relationships
    user = relationship("User", back_populates="resumes")
    matches = relationship("Match", back_populates="resume")


class Job(Base):
    """Job description model"""
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String, index=True)
    location = Column(String)
    description = Column(Text)
    
    # Relationships
    matches = relationship("Match", back_populates="job")


class Match(Base):
    """Match model to store resume-job matches with relevance scores"""
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    score = Column(Float)  # Relevance score from LLM
    
    # Relationships
    resume = relationship("Resume", back_populates="matches")
    job = relationship("Job", back_populates="matches") 