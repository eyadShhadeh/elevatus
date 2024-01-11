from uuid import UUID, uuid4
from src.models.candidate import Candidate, CandidateBase
from typing import Optional, Tuple
from src.infra.db import candidates
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import or_


def get(candidate_id: UUID) -> Optional[Candidate]:
    result = candidates.select().where(
        candidates.c.id == candidate_id).execute().first()
    return Candidate(**result) if result else None


def get_all(keyword: str) -> Optional[Tuple[Candidate]]:
    # there should be a better way, but due to time constrains we will go with this
    results = candidates.select().where(or_(
                candidates.c.first_name.ilike('%' + keyword + '%'),
                candidates.c.last_name.ilike('%' + keyword + '%'),
                candidates.c.email.ilike('%' + keyword + '%'),
                candidates.c.career_level.ilike('%' + keyword + '%'),
                candidates.c.job_major.ilike('%' + keyword + '%'),
                candidates.c.city.ilike('%' + keyword + '%'),
                candidates.c.gender.ilike('%' + keyword + '%'),
                )).execute().fetchall()

    # results = candidates.select().execute().fetchall()
    return tuple(map(lambda x: Candidate(**x), results)) if results else None


def delete(candidate_id: UUID) -> None:
    candidates.delete().where(
        candidates.c.id == candidate_id).execute()


def add(candidate: CandidateBase):
    candidate = Candidate(id=uuid4(), **candidate.dict())
    insert(candidates).values(**candidate.dict()).execute()
    return candidate
