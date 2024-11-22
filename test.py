import os

from src.const import LINKEDIN_PASSWORD, LINKEDIN_USERNAME
from src.crawler.linkedin import LinkedinCrawler

PUBLIC_ID = os.environ["LINKEDIN_PUBLIC_ID"]

crawler = LinkedinCrawler(username=LINKEDIN_USERNAME, password=LINKEDIN_PASSWORD)
profile = crawler.get_profile(public_id=PUBLIC_ID)
print(profile.model_dump_json(indent=2))
