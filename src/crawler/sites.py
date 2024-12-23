import textwrap

import html2text
from bs4 import BeautifulSoup
from bs4.element import Comment
from fastapi import status
from httpx import AsyncClient, RequestError

from ..logger import Logger
from ..schema import BaseModel

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
}
default_client = AsyncClient(timeout=60, headers=headers)


class CheckURL(BaseModel):
    success: bool
    content: str
    status_code: int


def check_captchas(content: str) -> bool:
    soup = BeautifulSoup(content, "html.parser")

    captchas = ["g-recaptcha", "h-captcha"]
    for captcha in captchas:
        if soup.find_all("div", {"class": captcha}):
            return True
    return False


async def check_url_is_valid(url: str, client: AsyncClient = default_client) -> CheckURL:
    try:
        response = await client.get(url, follow_redirects=True)
        status_code = response.status_code
        if response.is_error:
            return CheckURL(
                success=False,
                content="The URL is invalid, or we don't have access to it.",
                status_code=status_code,
            )

        elif check_captchas(content=response.text):
            return CheckURL(
                success=False,
                content="The URL could actually have a captcha. Please try again with a different URL.",
                status_code=status_code,
            )

        return CheckURL(success=True, content=response.text, status_code=status_code)
    except RequestError as err:
        Logger.error(f"Error to check URL: {err}")
        return CheckURL(
            success=False,
            content="The URL is taking too long to respond. Please try again later.",
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
        )


def filter_visible_html(body):
    soup = BeautifulSoup(body, "html.parser")

    # Remove unwanted tags (like <style>, <script>, etc.)
    for tag in soup(["style", "script", "head", "title", "meta", "[document]"]):
        tag.decompose()

    # Remove comments
    for comment in soup.findAll(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Return the cleaned-up HTML
    return str(soup)


def html_to_markdown(body):
    clean_html = filter_visible_html(body)
    return html2text.html2text(clean_html)


async def get_site_content(url: str) -> CheckURL:
    response = await check_url_is_valid(url=url)

    if not response.success:
        Logger.error(f"Error to get site content: {url} - {response.status_code}\n{response.content}")
        return response

    text = html_to_markdown(response.content)
    content = textwrap.dedent(text)
    response.content = content

    return response
