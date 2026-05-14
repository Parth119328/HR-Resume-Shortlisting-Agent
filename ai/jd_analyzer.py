import json

from ai.groq_client import client
from ai.prompts import JD_EXTRACTION_PROMPT


def analyzeJobDescription(jd_text):
    try:
        full_prompt = (
            JD_EXTRACTION_PROMPT
            + "\n\n"
            + jd_text
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

        raw_text = (
            response.choices[0]
            .message
            .content
        )

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
        return {
            "error": str(e)
        }