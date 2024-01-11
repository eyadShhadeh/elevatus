from fastapi import APIRouter, Response, status
health_router = APIRouter()


@health_router.head("/health_check",
                    tags=["health"],
                    summary="Enable auto-renew",
                    responses={
                        200: {},
                        404: {}
                    })
def health_check():
    return status.HTTP_200_OK
