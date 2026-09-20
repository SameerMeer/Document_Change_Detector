from groq import Groq


client = Groq()


def explain_change(old_text, new_text):

    prompt = f"""
You are a document change analysis assistant.

Compare the OLD text and NEW text below.

OLD TEXT:
{old_text}

NEW TEXT:
{new_text}

Explain exactly what changed in 1-2 clear sentences.

Rules:
- Mention changed values or requirements.
- Mention newly added requirements.
- Do not invent information.
- Do not make assumptions.
- If there is no meaningful change, say "No meaningful change."
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content