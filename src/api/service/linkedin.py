import re

from fastapi import HTTPException

from src.const import LINKEDIN_EXTRACT_PUBLIC_PROFILE, LINKEDIN_PASSWORD, LINKEDIN_USERNAME
from src.crawler.linkedin import LinkedinCrawler, Profile


class LinkedinService:
    linkedin = LinkedinCrawler(username=LINKEDIN_USERNAME, password=LINKEDIN_PASSWORD)

    @staticmethod
    def extract_public_id(profile_url):
        match = re.search(pattern=LINKEDIN_EXTRACT_PUBLIC_PROFILE, string=profile_url)
        return match.group(1) if match else None

    @classmethod
    def get_linkedin_profile(self, profile_url: str) -> Profile:
        public_id = self.extract_public_id(profile_url)
        if not public_id:
            raise HTTPException(status_code=400, detail="Sorry, this LinkedIn profile URL is not valid.")

        if profile := self.linkedin.get_profile(public_id=public_id):
            return profile

        raise HTTPException(status_code=404, detail="Sorry, profile not found.")
