import logging
from typing import Dict

from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi_utils.tasks import repeat_every
from pydantic import BaseModel
app = FastAPI(
    title='Subscription Domain Service'
)

app.include_router(admin_router, prefix='/admin')
app.include_router(security_router, prefix='/security')

logger = logging.getLogger(__name__)

ONE_MINUTE = 60


class SubscriptionHealth(BaseModel):
    name: str = 'subscription-domain-service'
    postgres: str = 'Available'
    status: int = status.HTTP_200_OK

    def mark_healthy(self) -> None:
        self.postgres = 'Available'
        self.status = status.HTTP_200_OK

    def mark_unavailable(self, err: str) -> None:
        self.postgres = err
        self.status = status.HTTP_503_SERVICE_UNAVAILABLE


health = SubscriptionHealth()


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Welcome to subscription-domain-service"}


