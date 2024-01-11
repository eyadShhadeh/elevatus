from fastapi import APIRouter, Response, status, Path, Query
from src.models.candidate import Candidate, CandidateBase
from src.models.generic import APIResponse
from src.services import candidate_service, user_service
from uuid import UUID
from typing import List


candidate_router = APIRouter()
# OAuth would be better but due to time constrains it will be done using simpler methods for authentication


@candidate_router.get("/{candidate_id}",
                      tags=["Candidate"],
                      summary="Candidate Get by ID",
                      response_model=APIResponse[Candidate],
                      response_model_exclude_none=True,
                      responses={
                                 200: {},
                                 404: {}
                             })
def get_candidate(response: Response, user_id: UUID = Query(...),
                  candidate_id: UUID = Path(..., description="Id for candidate want their data",
                                            example="bf46601e-9bd2-479b-8c14-6f4582fe4e23")):

    user = user_service.get(user_id=user_id)
    if not user:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return APIResponse(success=False, errors=("unauthorized user",))

    result = candidate_service.get(candidate_id)
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
        return APIResponse(success=False, errors=("candidate not found",))
    return APIResponse(results=result)


@candidate_router.get("/",
                      tags=["Candidate"],
                      summary="Candidate Get by ID",
                      response_model=APIResponse[List[Candidate]],
                      response_model_exclude_none=True,
                      responses={
                                 200: {},
                                 404: {}
                             })
def get_all_candidate(response: Response, keyword: str, user_id: UUID = Query(...)):
    user = user_service.get(user_id=user_id)
    if not user:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return APIResponse(success=False, errors=("unauthorized user",))

    result = candidate_service.get_all(keyword=keyword)
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
        return APIResponse(success=False, errors=("candidate not found",))
    return APIResponse(results=result)


@candidate_router.delete("/{candidate_id}",
                         tags=["Candidate"],
                         summary="Candidate Get by ID",
                         response_model=APIResponse[Candidate],
                         response_model_exclude_none=True,
                         responses={
                                 200: {},
                                 404: {}
                         })
def delete_candidate(response: Response, user_id: UUID = Query(...),
                     candidate_id: UUID = Path(..., description="Id for candidate want to delete their data",
                                               example="bf46601e-9bd2-479b-8c14-6f4582fe4e23")):
    user = user_service.get(user_id=user_id)
    if not user:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return APIResponse(success=False, errors=("unauthorized user",))

    candidate_service.delete(candidate_id)
    return status.HTTP_202_ACCEPTED


@candidate_router.post("/",
                       tags=["Candidate"],
                       summary="Candidate Get by ID",
                       response_model=APIResponse[Candidate],

                       response_model_exclude_none=True,
                       responses={
                                 200: {},
                                 404: {}
                       })
def add_candidate(response: Response,
                  candidate: CandidateBase,
                  user_id: UUID = Query(...),):
    user = user_service.get(user_id=user_id)
    if not user:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return APIResponse(success=False, errors=("unauthorized user",))

    result = candidate_service.add(candidate=candidate)
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
        return APIResponse(success=False, errors=("something wrong happened",))
    return APIResponse(results=result)
