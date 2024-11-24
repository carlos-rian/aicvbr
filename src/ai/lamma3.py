from langchain_ollama import ChatOllama

model = ChatOllama(model="llama3.2")


async def ollama_message(site_content: str, linkedin_perfil: str) -> str:
    message = f"""
LinkedIn Profile: {linkedin_perfil}

Job Vacancy: {site_content}

Based on my linkedin profile and the job vacancy, generate a curriculum for me.
    """

    messages = [
        # you are a specialist in Create curriculum for ATS( Applicant Tracking System) and LMS (Learning Management System) platforms
        {
            "role": "system",
            "content": "You are a specialist in treate curriculum for ATS(Applicant Tracking System) and LMS (Learning Management System) platforms",
        },
        {"role": "user", "content": message},
    ]

    stream = await model.ainvoke(messages)
    async for content in stream:
        print(content, end="", flush=True)
