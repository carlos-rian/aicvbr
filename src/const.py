import os

LINKEDIN_USERNAME = os.environ["LINKEDIN_USERNAME"]
LINKEDIN_PASSWORD = os.environ["LINKEDIN_PASSWORD"]
LINKEDIN_PROFILE_URL_REGEX = "https://www.linkedin.com/in/.*"
LINKEDIN_EXTRACT_PUBLIC_PROFILE = r"https:\/\/www\.linkedin\.com\/in\/([a-zA-Z0-9\-]+)\/?"
