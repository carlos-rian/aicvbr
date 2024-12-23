from src.ai.chat import send_message


async def main():
    with open("src/ai/tmp/profile.md", "r") as f:
        profile_content = f.read()

    with open("src/ai/tmp/job.md", "r") as f:
        site_content = f.read()

    await send_message(site_content=site_content, linkedin_perfil=profile_content)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())


import logging
import os

from src.const import LINKEDIN_PASSWORD, LINKEDIN_USERNAME
from src.crawler.linkedin import LinkedinCrawler
from src.crawler.sites import get_site_content

logging.basicConfig(level=logging.DEBUG)

PUBLIC_ID = os.environ["LINKEDIN_PUBLIC_ID"]

crawler = LinkedinCrawler(username=LINKEDIN_USERNAME, password=LINKEDIN_PASSWORD)
profile = crawler.get_profile(public_id=PUBLIC_ID)
profile_content = crawler._format_as_text()

with open("profile.md", "w") as f:
    f.write(profile_content)


async def main():
    site_content = await get_site_content(
        url="https://gruponexxees.gupy.io/job/eyJqb2JJZCI6ODEzODA1Mywic291cmNlIjoiZ3VweV9wb3J0YWwifQ==?jobBoardSource=gupy_portal"
    )

    await send_message(site_content=site_content.content, linkedin_perfil=profile_content)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
