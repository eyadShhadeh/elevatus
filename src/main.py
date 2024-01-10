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


@app.on_event("startup")
async def startup_event() -> None:
    configure_sentry()
    configure_logging()
    configure_event_bus()
    instantiate_parasite(app=app)


@app.on_event("startup")
@repeat_every(seconds=ONE_MINUTE, logger=logger, wait_first=False)
def periodic() -> None:
    with engine.connect() as conn:
        try:
            conn.execute('SELECT 1')
            health.mark_healthy()
        except Exception as e:
            health.mark_unavailable(str(e))


