from enum import Enum
from random import uniform

from langchain.docstore.document import Document
from langchain.output_parsers import PydanticOutputParser
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_text_splitters import CharacterTextSplitter
from langdetect import detect
from pydantic import Field

from src.logger import Logger
from src.schema import BaseModel


class MessageOutputParser(BaseModel):
    data: str = Field(..., description="An output message")


parser = PydanticOutputParser(pydantic_object=MessageOutputParser)
format_instructions = parser.get_format_instructions()

llm = ChatOpenAI(
    verbose=True,
    model="gpt-4o-mini",
    temperature=uniform(0.2, 0.8),
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

Logger.info(f"LLM configs: {llm.model_dump_json(indent=2)}")


class TextLanguage(Enum):
    PT = "PORTUGUESE"
    EN = "ENGLISH"


def check_language_of_the_message(content: str) -> TextLanguage:
    # create a document with the message
    lang = detect(content)
    if lang == "pt":
        return TextLanguage.PT
    elif lang == "en":
        return TextLanguage.EN

    raise ValueError(f"Language not supported: {lang}")


def format_message(kind: str, language: str, linkedin_perfil: str, site_content: str) -> str:
    return HumanMessage(
        content="""
                # LinkedIn Profile: 
                {linkedin_perfil}

                # Job Vacancy: 
                {site_content}

                Based on my LinkedIn Profile and the Job Vacancy, generate a {kind} for me that I can use to apply for the job.
                Respond in {language}.
                """.format(linkedin_perfil=linkedin_perfil, site_content=site_content, kind=kind, language=language)
    )


async def send_message(site_content: str, linkedin_perfil: str, language: str = None) -> str:
    language = language or check_language_of_the_message(site_content).value

    results = {"objective": None, "summary": None}

    system = SystemMessage(
        content="""
                - You are a specialist in create "Professional Objective" and "Professional Summary" curriculum for ATS(Applicant Tracking System) and LMS (Learning Management System) platforms!
                - You can use the best fit for the job vacancy and your LinkedIn profile to generate "Professional Objective" and "Professional Summary"!
                - You must respond in the same language as the job vacancy (in this case, {language}).
                - Don't be repetitive, be creative and professional!
                {format_instructions}                       
                """.format(format_instructions=format_instructions, language=language)
    )

    objective = format_message(
        kind="Professional Objective",
        language=language,
        linkedin_perfil=linkedin_perfil,
        site_content=site_content,
    )
    messages = [system, objective]
    response = await llm.ainvoke(input=messages)
    # add the AI response
    messages.append(AIMessage(content=response.content))

    # parse the response
    result = parser.parse(response.content)
    results["objective"] = result.data

    summary = format_message(
        kind="Professional Summary",
        language=language,
        linkedin_perfil=linkedin_perfil,
        site_content=site_content,
    )

    messages.append(summary)
    response = await llm.ainvoke(input=messages)
    messages.append(AIMessage(content=response.content))

    # parse the response
    result = parser.parse(response.content)
    results["summary"] = result.data

    print(results)
    return results
