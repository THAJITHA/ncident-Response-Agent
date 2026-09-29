from __future__ import annotations

import json
from typing import Any

import httpx

from app.config import get_settings


class LLMService:
    def __init__(self):
        self.settings = get_settings()

    def _fallback_response(self, incident_data: dict[str, Any]) -> dict[str, Any]:
        service = incident_data.get("service", "service")
        symptoms = incident_data.get("symptoms", "")
        return {
            "summary": f"{service} incident reported with symptoms including: {symptoms}",
            "possible_root_causes": [
                "Resource saturation or dependency exhaustion",
                "Deployment-related regression",
                "Configuration drift or unhealthy dependency",
            ],
            "confidence": 0.72,
            "recommended_runbook": "CHECK_RESOURCE_HEALTH",
            "recommendation": "Check dependency health, saturation metrics, and recent deployment impacts before applying a production change.",
        }

    async def analyze_incident(self, incident_data: dict[str, Any]) -> dict[str, Any]:
        if not self.settings.groq_api_key:
            return self._fallback_response(incident_data)

        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a senior SRE investigating production incidents. Respond with concise JSON: summary, possible_root_causes (list), confidence (0-1), recommended_runbook, recommendation.",
                },
                {
                    "role": "user",
                    "content": json.dumps(incident_data, default=str),
                },
            ],
            "temperature": 0.2,
        }

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.settings.groq_api_key}",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                )
                response.raise_for_status()
                content = response.json()
                text = content["choices"][0]["message"]["content"]
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    return self._fallback_response(incident_data)
        except Exception:
            return self._fallback_response(incident_data)
