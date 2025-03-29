from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = (
"postgresql://lab_user:lab_pass@localhost:5432/lab_database"
# Adjust if you’re using a different host or port
)
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)