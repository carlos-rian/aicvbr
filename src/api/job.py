from fastapi import APIRouter, Query
from pydantic import HttpUrl

from .service.job import JobService

router = APIRouter()


@router.get("/job")
async def get_linkedin_profile(site_url: HttpUrl):
    return await JobService.get_site_content(site_url=site_url)
