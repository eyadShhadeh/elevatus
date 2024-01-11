from fastapi import APIRouter, Response, status, Path
from src.models.user import User, UserBase
from src.models.generic import APIResponse
from src.services import user_service
from uuid import UUID
from typing import List


user_router = APIRouter()


@user_router.get("/{user_id}",
                 tags=["user"],
                 summary="user Get by ID",
                 response_model=APIResponse[User],
                 response_model_exclude_none=True,
                 responses={
                                 200: {},
                                 404: {}
                             })
def get_user(response: Response,
             user_id: UUID = Path(..., description="Id for user want their data",
                                  example="bf46601e-9bd2-479b-8c14-6f4582fe4e23")):
    result = user_service.get(user_id)
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
        return APIResponse(success=False, errors=("user not found",))
    return APIResponse(results=result)


@user_router.get("/",
                 tags=["user"],
                 summary="user Get by ID",
                 response_model=APIResponse[List[User]],
                 response_model_exclude_none=True,
                 responses={
                                 200: {},
                                 404: {}
                             })
def get_all_user(response: Response):
    result = user_service.get_all()
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
        return APIResponse(success=False, errors=("user not found",))
    return APIResponse(results=result)


@user_router.delete("/{user_id}",
                    tags=["user"],
                    summary="user Get by ID",
                    response_model=APIResponse[User],
                    response_model_exclude_none=True,
                    responses={
                                 200: {},
                                 404: {}
                         })
def delete_user(response: Response,
                user_id: UUID = Path(..., description="Id for subscriber want to delete their data",
                                     example="bf46601e-9bd2-479b-8c14-6f4582fe4e23")):
    user_service.delete(user_id)
    return status.HTTP_202_ACCEPTED


@user_router.post("/",
                  tags=["user"],
                  summary="user Get by ID",
                  response_model=APIResponse[User],

                  response_model_exclude_none=True,
                  responses={
                                 200: {},
                                 404: {}
                       })
def add_user(response: Response,
             user: UserBase):
    result = user_service.add(user=user)
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
        return APIResponse(success=False, errors=("something wrong happened",))
    return APIResponse(results=result)
