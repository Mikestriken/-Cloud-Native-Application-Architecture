from orm_lab.config import engine
from orm_lab.models import Base
def init_db():
    Base.metadata.create_all(bind=engine)
    
if __name__ == "__main__":
    init_db()