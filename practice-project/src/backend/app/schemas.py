"""
Pydantic schemas for data validation and response models
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List


class Token(BaseModel):
    """Token schema for authentication"""
    access_token: str
    token_type: str


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    name: str


class UserCreate(UserBase):
    """User creation schema with password"""
    password: str


class UserResponse(UserBase):
    """User response schema with ID"""
    id: int

    class Config:
        from_attributes = True


class ResumeBase(BaseModel):
    """Base resume schema"""
    content: str


class ResumeCreate(ResumeBase):
    """Resume creation schema"""
    pass


class ResumeResponse(ResumeBase):
    """Resume response schema with ID and user ID"""
    id: int
    user_id: int

    class Config:
        from_attributes = True


class JobBase(BaseModel):
    """Base job schema"""
    title: str
    company: str
    location: str
    description: str


class JobCreate(JobBase):
    """Job creation schema"""
    pass


class JobResponse(JobBase):
    """Job response schema with ID"""
    id: int

    class Config:
        from_attributes = True


class MatchBase(BaseModel):
    """Base match schema"""
    resume_id: int
    job_id: int
    score: float = Field(..., ge=0.0, le=1.0)


class MatchCreate(MatchBase):
    """Match creation schema"""
    pass


class MatchResponse(MatchBase):
    """Match response schema with ID and related job"""
    id: int
    job: JobResponse

    class Config:
        from_attributes = True


class MatchDetail(BaseModel):
    """Match detail with resume and job info"""
    id: int
    score: float
    resume: ResumeResponse
    job: JobResponse

    class Config:
        from_attributes = True 