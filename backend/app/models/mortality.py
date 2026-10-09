from sqlalchemy import Column, Integer, String, Numeric, DateTime, Index
from sqlalchemy.sql import func
from app.database import Base

class Mortality(Base):
    __tablename__ = "mortality"

    id = Column(Integer, primary_key=True, index=True)
    country_code = Column(String, index=True)
    country_name = Column(String, index=True)
    year = Column(Integer, index=True)
    age_group = Column(String, index=True)
    sex = Column(String, index=True)
    number_of_deaths = Column(Integer)
    death_rate_per_100000 = Column(Numeric(15, 4))
    source_file = Column(String)
    ingested_at = Column(DateTime(timezone=True), server_default=func.now())

Index('idx_mortality_natkey', Mortality.country_code, Mortality.year, Mortality.age_group, Mortality.sex)
