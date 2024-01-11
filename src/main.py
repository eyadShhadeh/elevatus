from typing import Dict

from fastapi import FastAPI
from src.controllers import candidate, health, user
app = FastAPI(
    title='Elevatus Service'
)


app.include_router(user.user_router, prefix='/user')
app.include_router(candidate.candidate_router, prefix='/candidate')

app.include_router(health.health_router, prefix='/health_check')


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Welcome to Elevatus-service"}
