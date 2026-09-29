from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.hindsight_service import HindsightService
from app.services.incident_service import IncidentService
from app.services.investigation_service import InvestigationService

router = APIRouter(prefix="/api", tags=["investigation"])


@router.post("/incidents/{incident_id}/investigate")
async def investigate_incident(incident_id: str, db: Session = Depends(get_db)):
    incident_service = IncidentService(db)
    incident = incident_service.get_by_id(incident_id)
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")

    payload = {
        "service": incident.service,
        "severity": incident.severity,
        "title": incident.title,
        "symptoms": incident.symptoms,
        "error_logs": incident.error_logs,
        "environment": incident.environment,
        "deployment_version": incident.deployment_version,
    }

    investigation = await InvestigationService().investigate(payload)
    return {
        "incident_id": incident_id,
        **investigation,
    }
