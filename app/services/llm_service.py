import json
import re
from typing import List, Dict, Any
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionMessageParam,
)
from app.core import settings
from app.prompts.expense_prompt import EXPENSE_EXTRACT_PROMPT
from app.prompts.rc_prompt import RC_EXTRACT_PROMPT


def clean_and_parse_json(text: str) -> Dict[str, Any]:
    """Remove code fences and parse JSON from LLM response"""
    # Remove code fences and language hint
    cleaned = re.sub(r"^```json\s*|\s*```$", "", text.strip(), flags=re.MULTILINE)
    # Parse and return JSON
    return json.loads(cleaned)


def extract_rc_data_by_llm(texts: List[str]) -> Dict[str, Any]:
    """Extract RC (Registration Certificate) data using LLM"""
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
        
        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from LLM")
            
        parsed_content = clean_and_parse_json(content)
        print("RC Data extracted:", parsed_content)
        return parsed_content

    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        raise ValueError(f"Failed to parse LLM response as JSON: {e}")
    except Exception as e:
        print(f"Error extracting RC data: {e}")
        raise Exception(f"Error extracting RC data: {e}")


def extract_expense_data_by_llm(texts: List[str]) -> Dict[str, Any]:
    """Extract expense data using LLM"""
    client = OpenAI(api_key=settings.openai_api_key)

    messages: List[ChatCompletionMessageParam] = [
        ChatCompletionSystemMessageParam(content=EXPENSE_EXTRACT_PROMPT, role='system'),
        ChatCompletionUserMessageParam(content="\n\n".join(texts), role='user'),
    ]

    try:
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            temperature=0.2,
        )
        
        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from LLM")
            
        parsed_content = clean_and_parse_json(content)
        print("Expense data extracted:", parsed_content)
        return parsed_content

    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        raise ValueError(f"Failed to parse LLM response as JSON: {e}")
    except Exception as e:
        print(f"Error extracting expense data: {e}")
        raise Exception(f"Error extracting expense data: {e}")