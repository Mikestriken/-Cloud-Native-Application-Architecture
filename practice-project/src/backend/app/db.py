"""
Database connection and session management
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get database URL from environment or use default for local development
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/resumejobmatcher")

# Create engine and SessionLocal
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    from app.models import Base
    Base.metadata.create_all(bind=engine)

def seed_initial_data():
    """Seed initial job data for demonstration purposes"""
    from app.models import Job
    from sqlalchemy.orm import Session
    
    db = SessionLocal()
    
    # Check if jobs table is empty
    job_count = db.query(Job).count()
    if job_count == 0:
        # Add some sample job listings
        sample_jobs = [
            Job(
                title="Software Engineer",
                company="TechCorp",
                location="Remote",
                description="""
                We're looking for a talented Software Engineer to join our team.
                
                Requirements:
                - 3+ years of software development experience
                - Strong knowledge of Python, FastAPI, and SQLAlchemy
                - Experience with cloud infrastructure (AWS, GCP, or Azure)
                - Familiarity with Docker and containerization
                
                Responsibilities:
                - Develop and maintain backend services
                - Collaborate with cross-functional teams
                - Participate in code reviews and technical discussions
                """
            ),
            Job(
                title="Data Scientist",
                company="DataInsights",
                location="New York, NY",
                description="""
                Join our data science team to solve complex problems using ML and data analysis.
                
                Requirements:
                - Advanced degree in Computer Science, Statistics, or related field
                - Experience with Python, pandas, scikit-learn, and TensorFlow
                - Strong background in statistical analysis and machine learning
                - Excellent communication skills
                
                Responsibilities:
                - Develop and implement machine learning models
                - Analyze large datasets to extract insights
                - Present findings to stakeholders
                """
            ),
            Job(
                title="Cloud Solutions Architect",
                company="CloudTech Solutions",
                location="San Francisco, CA",
                description="""
                Design and implement scalable cloud infrastructure solutions.
                
                Requirements:
                - 5+ years of experience in cloud architecture (AWS, Azure, GCP)
                - Strong knowledge of infrastructure as code (Terraform, CloudFormation)
                - Experience with containerization and orchestration (Docker, Kubernetes)
                - Understanding of security best practices
                
                Responsibilities:
                - Design and implement cloud infrastructure
                - Optimize for performance, cost, and security
                - Collaborate with development teams to implement CI/CD pipelines
                """
            ),
            Job(
                title="Frontend Developer",
                company="WebDesign Co",
                location="Remote",
                description="""
                Build beautiful and responsive user interfaces for our web applications.
                
                Requirements:
                - 2+ years of experience with React, Vue, or Angular
                - Strong HTML, CSS, and JavaScript skills
                - Experience with responsive design and CSS frameworks
                - Knowledge of modern frontend build tools
                
                Responsibilities:
                - Implement user interfaces based on design specifications
                - Optimize applications for performance and accessibility
                - Write clean, maintainable code
                """
            ),
            Job(
                title="DevOps Engineer",
                company="InfraOps",
                location="Austin, TX",
                description="""
                Implement and maintain CI/CD pipelines and infrastructure.
                
                Requirements:
                - 3+ years of experience in DevOps or SRE roles
                - Experience with infrastructure as code (Terraform, Ansible)
                - Knowledge of container orchestration (Kubernetes, ECS)
                - Familiarity with monitoring and observability tools
                
                Responsibilities:
                - Design and implement CI/CD pipelines
                - Manage and optimize cloud infrastructure
                - Implement monitoring and alerting systems
                """
            ),
        ]
        
        for job in sample_jobs:
            db.add(job)
        
        db.commit()
    
    db.close() 