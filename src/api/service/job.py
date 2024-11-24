import re

from fastapi import HTTPException
from pydantic import HttpUrl

from src.crawler.sites import get_site_content


class JobService:
    @staticmethod
    async def get_site_content(site_url: HttpUrl):
        response = await get_site_content(url=str(site_url))
        if not response.success:
            raise HTTPException(status_code=response.status_code, detail=response.content)

        return response
