from sqlalchemy import Column, Integer, String, Float
from database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String)
    status = Column(String)  # On Track, At Risk, Delayed
    
    budget = Column(Float)
    actual_cost = Column(Float)
    
    progress = Column(Float)  # percentage
    
    deadline = Column(String)
    owner = Column(String)
    priority = Column(String)