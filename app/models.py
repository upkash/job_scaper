from sqlalchemy import Column, Integer, String
from .database import Base

class Job(Base):
    __tablename__ = "jobs"
    job_id = Column(String(50), primary_key = True)
    title = Column(String(50))
    location = Column(String(50))
    company = Column(String(50))
    url = Column(String(200))
    source = Column(String(20))