from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.incident_service import IncidentService
from app.services.postmortem_service import PostmortemService

router = APIRouter(prefix="/api", tags=["postmortem"])


@router.post("/incidents/{incident_id}/postmortem")
def generate_postmortem(incident_id: str, db: Session = Depends(get_db)):
    incident_service = IncidentService(db)
    incident = incident_service.get_by_id(incident_id)
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")

    postmortem = PostmortemService().generate_postmortem({
        "title": incident.title,
        "service": incident.service,
        "environment": incident.environment,
        "symptoms": incident.symptoms,
        "root_cause": incident.root_cause,
        "investigation_steps": incident.investigation_steps,
        "actions_taken": incident.actions_taken,
        "resolution": incident.resolution,
        "lessons_learned": incident.lessons_learned,
    })
    incident.postmortem = str(postmortem)
    db.commit()
    return postmortem
