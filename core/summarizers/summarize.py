import os

from openai import AsyncAzureOpenAI

from ..models import Paper
from ..templates.summarize_paper import summarize_system_message, summarize_user_message

client = AsyncAzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)


async def summarize_paper_with_oai(paper: Paper):
    completion = await client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": summarize_system_message},
            {
                "role": "user",
                "content": summarize_user_message.format(
                    title=paper.title, authors=paper.authors, text=paper.text
                ),
            },
        ],
    )

    return completion.choices[0].message.content

    return completion.choices[0].message.content
