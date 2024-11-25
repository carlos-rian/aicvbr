import logging
import os

from src.ai.chat import ollama_message
from src.const import LINKEDIN_PASSWORD, LINKEDIN_USERNAME
from src.crawler.linkedin import LinkedinCrawler
from src.crawler.sites import get_site_content

logging.basicConfig(level=logging.DEBUG)

PUBLIC_ID = os.environ["LINKEDIN_PUBLIC_ID"]

crawler = LinkedinCrawler(username=LINKEDIN_USERNAME, password=LINKEDIN_PASSWORD)
profile = crawler.get_profile(public_id=PUBLIC_ID)


async def main():
    profile_content = crawler.format_as_text()
    site_content = await get_site_content(
        url="https://gruponexxees.gupy.io/job/eyJqb2JJZCI6ODEzODA1Mywic291cmNlIjoiZ3VweV9wb3J0YWwifQ==?jobBoardSource=gupy_portal"
    )

    await ollama_message(site_content=site_content.content, linkedin_perfil=profile_content)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
