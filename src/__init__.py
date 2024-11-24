from fastapi import FastAPI

from .api.job import router as job_router
from .api.linkedin import router as linkedin_router


def create_app():
    app = FastAPI()

    app.include_router(linkedin_router, prefix="/api/linkedin")
    app.include_router(job_router, prefix="/api/jobs")
    return app


app = create_app()
