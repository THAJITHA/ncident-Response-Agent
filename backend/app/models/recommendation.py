from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    incident_id: str = Field(...)


class RecommendationResponse(BaseModel):
    recommendation: str
    why: str
    historical_evidence: str
    related_incident_ids: list[str] = []
    previous_root_cause: str = ""
    recommended_runbook: str = ""
    expected_benefit: str = ""
    warning: str = ""
    confidence: float = 0.0
