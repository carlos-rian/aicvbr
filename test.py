import re

# URL without a trailing slash
url = "https://www.linkedin.com/in/carlos-rian/"
pattern = r"https:\/\/www\.linkedin\.com\/in\/([a-zA-Z0-9\-]+)\/?"
match = re.search(pattern, url)

if match:
    public_id = match.group(1)
    print(f"Public ID: {public_id}")
else:
    print("No match found.")


import json
import logging
import os

from src.const import LINKEDIN_PASSWORD, LINKEDIN_USERNAME
from src.crawler.linkedin import LinkedinCrawler

logging.basicConfig(level=logging.DEBUG)

PUBLIC_ID = os.environ["LINKEDIN_PUBLIC_ID"]

crawler = LinkedinCrawler(username=LINKEDIN_USERNAME, password=LINKEDIN_PASSWORD)
profile = crawler.get_profile(public_id=PUBLIC_ID)
connections = crawler.get_profile_connections(urn_id=profile.urn_id)

print(profile.model_dump_json(indent=2))
