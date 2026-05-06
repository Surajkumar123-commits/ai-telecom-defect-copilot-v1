def build_prompt(issue_data):
    return f"""
You are an AI telecom defect analysis expert.

Analyze this issue:
{issue_data}

STRICT RULES:
- Return ONLY valid JSON
- Do NOT add explanations
- Do NOT use markdown
- Do NOT add ```json

FORMAT:

{{
  "root_cause": "one clear sentence",
  "business_impact": "one clear sentence",
  "severity": "High/Medium/Low",
  "suggested_fix": ["step 1", "step 2"],
  "owner_team": "UI/Frontend Team or Backend/API Team or Platform/MPM Team"
}}
"""