from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse
import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI()


class Issue(BaseModel):
    issue: str
    owner: str = "AI to decide"


class IssueBatch(BaseModel):
    issues: list[Issue]


def clean_and_parse_json(text):
    cleaned_text = text.strip()
    cleaned_text = re.sub(r"```json|```", "", cleaned_text).strip()

    json_match = re.search(r"\[.*\]", cleaned_text, re.DOTALL)

    if not json_match:
        raise ValueError("No JSON array found")

    return json.loads(json_match.group(0))


@app.post("/ai-analysis")
def ai_analysis(data: IssueBatch):
    issues_text = "\n".join(
        [f"- {item.issue}" for item in data.issues]
    )

    prompt = f"""
You are an AI telecom defect analysis expert.

Analyze the following telecom defect issues:

{issues_text}

Return ONLY valid JSON array.
Do NOT use markdown.
Do NOT add explanations.
Do NOT add ```json.

Each object must follow this exact format:

[
  {{
    "issue": "same issue text",
    "root_cause": "one clear sentence",
    "business_impact": "one clear sentence",
    "severity": "High/Medium/Low",
    "suggested_fix": ["step 1", "step 2"],
    "owner_team": "UI/Frontend Team or Backend/API Team or Platform/MPM Team"
  }}
]
"""

    try:
        response = model.generate_content(prompt)
        parsed = clean_and_parse_json(response.text)

        return {
            "results": parsed
        }

    except Exception as e:
        return {
            "error": str(e),
            "results": []
        }


@app.post("/ai-jira-comment", response_class=PlainTextResponse)
def ai_jira_comment(data: Issue):
    prompt = f"""
You are an AI telecom defect analysis expert.

Create a Jira-ready comment for this issue:

Issue: {data.issue}

Include:
- Root Cause
- Business Impact
- Severity
- Suggested Fix
- Owner Team

Keep it concise and professional.
"""

    response = model.generate_content(prompt)
    return response.text


@app.get("/health")
def health():
    return {"status": "ok"}