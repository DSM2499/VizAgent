import pandas as pd
import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_schema(df: pd.DataFrame) -> str:
    schema = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        example = df[col].dropna().astype(str).unique()[:3]
        schema.append(f"- {col} ({dtype}), e.g. {list(example)}")
    return "\n".join(schema)

def suggest_dashboard_plan(df: pd.DataFrame, max_charts: int = 4, model = "gpt-4o-mini") -> str:
    schema_text = extract_schema(df)
    client = openai.OpenAI(api_key = openai.api_key)

    system_prompt = "You are a dashboard planning assistant for web analytics."
    user_prompt = f"""
Given this data schema, suggest a Tableau dashboard plan with up to {max_charts} charts.

Schema:
{schema_text}

For each chart, describe:
- Chart type (bar, line, pie, map, etc.)
- Dimension(s)
- Measure(s)
- Optional filter
- What story it tells

Return the plan in structured Markdown or JSON.
"""
    
    try:
        response = client.chat.completions.create(
            model = model,
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format = {"type": "json_object"},
            temperature = 0.5,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
    