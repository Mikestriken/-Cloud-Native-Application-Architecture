"""
Backend API initialization
"""

from app.models import User, Resume, Job, Match
from app.db import get_db, init_db, seed_initial_data
from app.llm import match_resume_with_jobs 