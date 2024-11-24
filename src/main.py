from fastapi import FastAPI

from .api.linkedin import router as linkedin_router


def create_app():
    app = FastAPI()

    app.include_router(linkedin_router, prefix="/api/linkedin")
    return app


app = create_app()
