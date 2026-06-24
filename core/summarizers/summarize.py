import os

from litellm import acompletion

from ..models import Paper
from ..templates.summarize_paper import summarize_system_message, summarize_user_message

MODEL = os.getenv("MODEL", "openai/gpt-4o-mini")


async def summarize_paper_with_oai(paper: Paper):
    completion = await acompletion(
        model=MODEL,
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
