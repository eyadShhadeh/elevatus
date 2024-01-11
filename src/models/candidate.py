from uuid import UUID
from src.models.user import UserBase
from enum import Enum
from typing import List, Optional
from datetime import datetime


class Gender(str, Enum):
    Male = "Male"
    Female = "Female"
    Not_Specified = "Not_Specified"


class CandidateBase(UserBase):
    career_level: str
    job_major: str
    years_of_experience: int
    skills: List[str]
    nationality: str
    city: str
    salary: int
    gender: Gender


class Candidate(CandidateBase):
    id: UUID
    created_at: Optional[datetime] = datetime.utcnow()
    updated_at: Optional[datetime] = datetime.utcnow()
