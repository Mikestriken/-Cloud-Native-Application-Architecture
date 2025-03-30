"""
Database connection and session management
"""
# Query DB Command: `docker-compose exec db psql -U postgres -d resumejobmatcher`
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
            Job(
                title="Machine Learning Engineer",
                company="AI Innovations",
                location="Boston, MA",
                description="""
                Join our team to build cutting-edge machine learning systems.
                
                Requirements:
                - MS or PhD in Computer Science, Machine Learning, or related field
                - Experience with deep learning frameworks (PyTorch, TensorFlow)
                - Strong Python programming skills
                - Knowledge of natural language processing and computer vision techniques
                
                Responsibilities:
                - Develop and deploy machine learning models
                - Research and implement state-of-the-art ML algorithms
                - Optimize model performance for production environments
                - Collaborate with data engineers and product teams
                """
            ),
            Job(
                title="Product Manager",
                company="ProductSphere",
                location="Chicago, IL",
                description="""
                Lead our product development initiatives from concept to launch.
                
                Requirements:
                - 4+ years of product management experience
                - Experience with agile methodologies
                - Strong analytical skills and data-driven decision making
                - Excellent communication and stakeholder management abilities
                
                Responsibilities:
                - Define product strategy and roadmap
                - Gather and prioritize requirements
                - Work with engineering, design, and marketing teams
                - Analyze market trends and competitive landscape
                """
            ),
            Job(
                title="Cybersecurity Analyst",
                company="SecureDefense",
                location="Washington, DC",
                description="""
                Protect our organization's systems and data from cyber threats.
                
                Requirements:
                - Bachelor's degree in Computer Science, Cybersecurity, or related field
                - Security certifications (CISSP, CEH, Security+) preferred
                - Experience with security tools and technologies
                - Knowledge of security frameworks (NIST, ISO 27001)
                
                Responsibilities:
                - Monitor systems for security breaches
                - Implement security measures and controls
                - Conduct vulnerability assessments and penetration testing
                - Develop security policies and procedures
                """
            ),
            Job(
                title="UX/UI Designer",
                company="DesignWorks",
                location="Remote",
                description="""
                Create intuitive and engaging user experiences for our digital products.
                
                Requirements:
                - 3+ years of experience in UX/UI design
                - Proficiency with design tools (Figma, Sketch, Adobe XD)
                - Understanding of user research methodologies
                - Portfolio demonstrating strong design skills
                
                Responsibilities:
                - Design user interfaces for web and mobile applications
                - Conduct user research and usability testing
                - Create wireframes, prototypes, and high-fidelity mockups
                - Collaborate with product managers and developers
                """
            ),
            Job(
                title="Data Engineer",
                company="DataFlow Systems",
                location="Seattle, WA",
                description="""
                Build and maintain our data infrastructure and pipelines.
                
                Requirements:
                - Strong experience with SQL and database systems
                - Knowledge of big data technologies (Hadoop, Spark)
                - Programming skills in Python or Scala
                - Experience with ETL processes and tools
                
                Responsibilities:
                - Design and implement data pipelines
                - Optimize database performance and architecture
                - Ensure data quality and reliability
                - Create data models and support analytics needs
                """
            ),
            Job(
                title="Embedded Systems Engineer",
                company="IoT Innovations",
                location="Austin, TX",
                description="""
                Design and develop embedded systems for IoT applications.
                
                Requirements:
                - BS/MS in Electrical Engineering or Computer Engineering
                - Experience with microcontrollers (ARM, AVR, PIC)
                - Proficiency in C/C++ programming for embedded systems
                - Knowledge of communication protocols (I2C, SPI, UART, CAN)
                - PCB design and schematic capture experience
                
                Responsibilities:
                - Develop firmware for embedded devices
                - Interface with hardware components and sensors
                - Optimize code for performance and power efficiency
                - Troubleshoot hardware and software issues
                """
            ),
            Job(
                title="FPGA Design Engineer",
                company="Xilinx Solutions",
                location="San Jose, CA",
                description="""
                Design and implement FPGA-based solutions for high-performance computing applications.
                
                Requirements:
                - MS in Electrical Engineering or Computer Engineering
                - Strong knowledge of VHDL or Verilog
                - Experience with FPGA design tools (Vivado, Quartus)
                - Understanding of digital signal processing concepts
                - Background in computer architecture
                
                Responsibilities:
                - Design and implement digital logic in VHDL/Verilog
                - Perform simulation and timing analysis
                - Develop test benches for verification
                - Optimize designs for area, power, and performance
                """
            ),
            Job(
                title="Power Electronics Engineer",
                company="EnergyTech",
                location="Raleigh, NC",
                description="""
                Design power conversion systems for renewable energy applications.
                
                Requirements:
                - MS/PhD in Electrical Engineering with focus on power electronics
                - Experience with power converter topologies (DC-DC, DC-AC)
                - Knowledge of control systems and feedback control
                - Familiarity with circuit simulation tools (SPICE, PSIM)
                - Understanding of thermal management and EMC requirements
                
                Responsibilities:
                - Design power conversion circuits
                - Develop control algorithms for power converters
                - Perform simulation and analysis of power systems
                - Prototype and test hardware designs
                """
            ),
            Job(
                title="RF/Microwave Engineer",
                company="Wireless Technologies Inc.",
                location="Boulder, CO",
                description="""
                Design and develop RF circuits and systems for wireless communication applications.
                
                Requirements:
                - BS/MS in Electrical Engineering with focus on RF/microwave
                - Experience with RF design tools (ADS, CST)
                - Knowledge of wireless communication standards (5G, WiFi, Bluetooth)
                - Understanding of antenna design principles
                - Familiarity with RF test equipment
                
                Responsibilities:
                - Design RF circuits (amplifiers, filters, mixers)
                - Perform electromagnetic simulations
                - Characterize RF components and systems
                - Troubleshoot and optimize RF performance
                """
            ),
            Job(
                title="Computer Architecture Engineer",
                company="Processor Technologies",
                location="Portland, OR",
                description="""
                Design and optimize processor architectures for high-performance computing applications.
                
                Requirements:
                - MS/PhD in Computer Engineering or Electrical Engineering
                - Strong understanding of computer architecture principles
                - Experience with hardware description languages (VHDL/Verilog)
                - Knowledge of instruction set architectures (x86, ARM, RISC-V)
                - Background in performance analysis and optimization
                
                Responsibilities:
                - Design processor microarchitecture components
                - Optimize pipeline and memory hierarchy
                - Implement and verify instruction execution units
                - Analyze and improve processor performance
                """
            ),
        ]
        
        for job in sample_jobs:
            db.add(job)
        
        db.commit()
    
    db.close() 