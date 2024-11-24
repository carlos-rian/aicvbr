from fastapi import APIRouter, Query

from ..const import LINKEDIN_PROFILE_URL_REGEX
from ..logger import Logger
from .service.linkedin import LinkedinService

router = APIRouter()


@router.get("/profile")
async def get_linkedin_profile(profile_url: str = Query(..., pattern=LINKEDIN_PROFILE_URL_REGEX)):
    Logger.info(f"Received request for profile URL: {profile_url}")
    return LinkedinService.get_linkedin_profile(profile_url=profile_url)
