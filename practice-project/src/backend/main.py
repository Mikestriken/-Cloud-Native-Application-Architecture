"""
Main FastAPI application entry point
"""
import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from app.models import User, Resume, Job, Match
from app.db import get_db
from app.llm import match_resume_with_jobs
from app.schemas import (
    UserCreate, 
    UserResponse, 
    ResumeCreate, 
    JobResponse, 
    MatchResponse,
    Token,
)

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(title="Resume Job Matcher API")

# Add CORS middleware to allow frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

# User Authentication Endpoints
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, name=user.name, password=hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Resume Endpoints
@app.post("/upload_resume")
async def upload_resume(resume: ResumeCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check if the user already has a resume
    existing_resume = db.query(Resume).filter(Resume.user_id == current_user.id).first()
    
    if existing_resume:
        # Update existing resume
        existing_resume.content = resume.content
        db_resume = existing_resume
        db.commit()
        db.refresh(db_resume)
        
        # Log the update
        logger.info(f"Updated existing resume for user ID {current_user.id}, resume ID {db_resume.id}")
    else:
        # Create new resume
        db_resume = Resume(
            user_id=current_user.id,
            content=resume.content
        )
        db.add(db_resume)
        db.commit()
        db.refresh(db_resume)
        
        # Log the creation
        logger.info(f"Created new resume for user ID {current_user.id}, resume ID {db_resume.id}")
    
    # Match with jobs and store matches
    matches = await match_resume_with_jobs(db_resume.content, db_resume.id, db)
    return {"resume_id": db_resume.id, "matches": matches}

@app.get("/match_jobs/{resume_id}", response_model=list[MatchResponse])
async def get_job_matches(resume_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Verify the resume belongs to the current user
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Get the top 5 matches for this resume
    matches = db.query(Match).filter(Match.resume_id == resume_id).order_by(Match.score.desc()).limit(5).all()
    
    return matches

# Job Endpoints
@app.get("/jobs", response_model=list[JobResponse])
async def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    return jobs

@app.get("/job/{job_id}", response_model=JobResponse)
async def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

# Health check endpoint
@app.get("/")
async def root():
    return {"status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 