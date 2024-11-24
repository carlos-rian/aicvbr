import os

LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
LINKEDIN_PROFILE_URL_REGEX = "https://www.linkedin.com/in/.*"
LINKEDIN_EXTRACT_PUBLIC_PROFILE = r"https:\/\/www\.linkedin\.com\/in\/([a-zA-Z0-9\-]+)\/?"
