from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse
import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai
from prompt import build_prompt

load_dotenv()

print("Loaded Key:", os.getenv("GEMINI_API_KEY"))

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI()


class Issue(BaseModel):
    issue: str
    owner: str


class IssueBatch(BaseModel):
    issues: list[Issue]


@app.post("/ai-analysis")
def ai_analysis(data: IssueBatch):
    results = []

    for item in data.issues:
        prompt = build_prompt(item.dict())
        response = model.generate_content(prompt)

        try:
            raw_text = response.text.strip()
            cleaned_text = re.sub(r"```json|```", "", raw_text).strip()
            json_match = re.search(r"\{.*\}", cleaned_text, re.DOTALL)

            if json_match:
                json_string = json_match.group(0)
                parsed = json.loads(json_string)
            else:
                raise ValueError("No JSON found")

        except Exception:
            parsed = {
                "root_cause": "Parsing failed",
                "business_impact": "",
                "suggested_fix": [],
                "owner_team": "Unknown"
            }

        results.append({
            "issue": item.issue,
            "root_cause": parsed.get("root_cause"),
            "business_impact": parsed.get("business_impact"),
            "suggested_fix": parsed.get("suggested_fix"),
            "owner_team": parsed.get("owner_team")
        })

    return {
        "results": results
    }


@app.post("/ai-jira-comment", response_class=PlainTextResponse)
def ai_jira_comment(data: Issue):
    prompt = build_prompt(data.dict())
    response = model.generate_content(prompt)

    return response.text


@app.get("/health")
def health():
    return {"status": "ok"}