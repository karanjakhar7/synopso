summarize_system_message = "You are a helpful research assistant."

summarize_user_message = """Your task is to summarize the research paper given.
RULES:
1. Generate a summary in 5-6 sentences.
2. Do not infer information that is not present in the text.
3. Do not include your opinions or interpretations.
4. Provide a coherent and concise summary.

Title: {title}
Authors: {authors}
Text:
{text}

Summary:
"""
