import os
from openai import AzureOpenAI
from ..templates.summarize_paper import summarize_system_message, summarize_user_message
from ..models import Paper

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-07-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)


def summarize_paper_with_oai(paper: Paper):

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": summarize_system_message},
            {
                "role": "user",
                "content": summarize_user_message.format(title=paper.title, authors=paper.authors, text=paper.text),
            }
        ]
    )

    return  completion.choices[0].message.content