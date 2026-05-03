# AI Telecom Defect Copilot 🚀

An AI-powered Telecom Defect Intelligence System built using FastAPI and LLMs to automate defect analysis, root cause detection, and resolution recommendations across telecom platforms.

---

## 🔧 Features

- Multi-issue batch processing  
- AI-driven root cause analysis  
- Business impact identification  
- Suggested fixes generation  
- Owner team detection (UI / Backend / Platform)  
- Structured JSON output for API integration  
- Jira-ready comment generation  

---

## 🏗️ Tech Stack

- Python  
- FastAPI  
- Google Gemini (LLM)  
- REST APIs  
- JSON Parsing  
- Prompt Engineering  

---

## 📊 Sample Output

```json
{
  "issue": "Badge mismatch MPM vs Preview",
  "root_cause": "...",
  "business_impact": "...",
  "suggested_fix": ["step 1", "step 2"],
  "owner_team": "Backend/API Team"
}
