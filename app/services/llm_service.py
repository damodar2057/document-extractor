import json
from typing import List
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionMessageParam,
)
from app.core import settings
from app.prompts.rc_prompt import RC_EXTRACT_PROMPT
import re
def clean_and_parse_json(text: str):
    # Remove code fences and language hint
    cleaned = re.sub(r"^```json\s*|\s*```$", "", text.strip(), flags=re.MULTILINE)
    # Now parse JSON
    return json.loads(cleaned)


def extract_rc_data(texts: List[str]) -> str:
    client = OpenAI(api_key=settings.openai_api_key)

    messages: List[ChatCompletionMessageParam] = [
        ChatCompletionSystemMessageParam(content=RC_EXTRACT_PROMPT, role='system'),
        ChatCompletionUserMessageParam(content="\n\n".join(texts), role='user'),
    ]

    try:
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            temperature=0.2,
        )
        content =  clean_and_parse_json(response.choices[0].message.content)
        print(content)
        # json_data = json.loads(content)
        return content

    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"
