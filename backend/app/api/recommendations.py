from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.hindsight_service import HindsightService
from app.services.incident_service import IncidentService
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/api", tags=["recommendations"])


@router.post("/incidents/{incident_id}/recommend")
def generate_recommendation(incident_id: str, db: Session = Depends(get_db)):
    incident_service = IncidentService(db)
    incident = incident_service.get_by_id(incident_id)
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")

    memory = HindsightService(db)
    similar = memory.recall_relevant_incidents(f"{incident.service} {incident.symptoms} {incident.error_logs}")
    recommendation = RecommendationService().build_recommendation(incident, similar)
    return recommendation.model_dump()
