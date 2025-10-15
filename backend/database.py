from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()

# 1️⃣ Resume Table
class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    skills = Column(JSON)
    education = Column(JSON)
    projects = Column(JSON)
    parsed_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    matches = relationship("Match", back_populates="resume")


# 2️⃣ Job Description Table
class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    company = Column(String)
    required_skills = Column(JSON)
    jd_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    matches = relationship("Match", back_populates="job")


# 3️⃣ Match Table
class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_id = Column(Integer, ForeignKey("job_descriptions.id"))
    match_score = Column(Integer)
    summary_of_fit = Column(String)
    matched_skills = Column(JSON)
    missing_skills = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    resume = relationship("Resume", back_populates="matches")
    job = relationship("JobDescription", back_populates="matches")


# ────────────────────────────────────────────────
# DB setup
def get_engine():
    DB_URL = os.getenv("DATABASE_URL", "sqlite:///smart_screener.db")
    return create_engine(DB_URL, echo=False)


engine = get_engine()
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(engine)
