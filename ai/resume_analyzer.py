import json

from ai.groq_client import client
from ai.prompts import RESUME_EXTRACTION_PROMPT


def analyze_resume(resume_text):
    try:
        full_prompt = (
            RESUME_EXTRACTION_PROMPT
            + "\n\n"
            + resume_text
        )

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],
            temperature=0
        )

        raw_text = response.choices[0].message.content


        cleaned_response = (
            raw_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        parsed_data = json.loads(
            cleaned_response
        )

        return parsed_data

    except Exception as e:

        print("FULL ERROR:")
        print(type(e))
        print(e)

        return {
            "error": str(e)
        }