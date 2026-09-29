from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import IncidentEvent
from app.models.incident import IncidentCreate, IncidentOut
from app.services.incident_service import IncidentService

router = APIRouter(prefix="/api/incidents", tags=["incidents"])


class IncidentAction(BaseModel):
    action: Literal["investigate", "start_response", "assign", "contain", "resolve", "add_note", "escalate"]
    detail: str = Field(default="", max_length=4000)
    assigned_to: str = Field(default="", max_length=120)


@router.post("", response_model=IncidentOut)
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db)):
    service = IncidentService(db)
    incident = service.create_incident(payload)
    return IncidentOut(
        incident_id=incident.incident_id,
        title=incident.title,
        service=incident.service,
        severity=incident.severity,
        status=incident.status,
        symptoms=incident.symptoms,
        error_logs=incident.error_logs,
        affected_components=incident.affected_components,
        deployment_version=incident.deployment_version,
        environment=incident.environment,
        root_cause=incident.root_cause,
        investigation_steps=incident.investigation_steps,
        actions_taken=incident.actions_taken,
        runbook_used=incident.runbook_used,
        resolution=incident.resolution,
        resolution_time=incident.resolution_time,
        successful=incident.successful,
        postmortem=incident.postmortem,
        lessons_learned=incident.lessons_learned,
        created_at=incident.created_at,
        resolved_at=incident.resolved_at,
        confidence=incident.confidence or 0.0,
    )


@router.get("")
def list_incidents(db: Session = Depends(get_db)):
    service = IncidentService(db)
    incidents = service.get_all()
    return [{
        "incident_id": incident.incident_id,
        "title": incident.title,
        "service": incident.service,
        "severity": incident.severity,
        "status": incident.status,
        "symptoms": incident.symptoms,
        "error_logs": incident.error_logs,
        "resolution_time": incident.resolution_time,
        "successful": incident.successful,
        "created_at": incident.created_at.isoformat() if incident.created_at else None,
    } for incident in incidents]


@router.get("/{incident_id}")
def get_incident(incident_id: str, db: Session = Depends(get_db)):
    service = IncidentService(db)
    incident = service.get_by_id(incident_id)
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return {
        "incident_id": incident.incident_id,
        "title": incident.title,
        "service": incident.service,
        "severity": incident.severity,
        "status": incident.status,
        "symptoms": incident.symptoms,
        "error_logs": incident.error_logs,
        "affected_components": incident.affected_components,
        "deployment_version": incident.deployment_version,
        "environment": incident.environment,
        "root_cause": incident.root_cause,
        "investigation_steps": incident.investigation_steps,
        "actions_taken": incident.actions_taken,
        "runbook_used": incident.runbook_used,
        "resolution": incident.resolution,
        "resolution_time": incident.resolution_time,
        "successful": incident.successful,
        "postmortem": incident.postmortem,
        "lessons_learned": incident.lessons_learned,
        "created_at": incident.created_at.isoformat() if incident.created_at else None,
    }


@router.get("/{incident_id}/events")
def get_incident_events(incident_id: str, db: Session = Depends(get_db)):
    incident = IncidentService(db).get_by_id(incident_id)
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    events = db.query(IncidentEvent).filter(
        IncidentEvent.incident_id == incident_id
    ).order_by(IncidentEvent.created_at.asc(), IncidentEvent.id.asc()).all()
    return [{
        "id": event.id,
        "event_type": event.event_type,
        "detail": event.detail,
        "actor": event.actor,
        "created_at": event.created_at.isoformat() if event.created_at else None,
    } for event in events]


@router.post("/{incident_id}/actions")
def perform_incident_action(incident_id: str, payload: IncidentAction, db: Session = Depends(get_db)):
    incident = IncidentService(db).get_by_id(incident_id)
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")

    detail = payload.detail.strip()
    assigned_to = payload.assigned_to.strip()
    if payload.action == "assign" and not assigned_to:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="A responder is required")
    if payload.action in {"add_note", "resolve"} and not detail:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="A note or resolution is required")

    if payload.action in {"investigate", "start_response"}:
        incident.status = "INVESTIGATING"
    elif payload.action == "contain":
        incident.status = "CONTAINED"
    elif payload.action == "resolve":
        incident.status = "RESOLVED"
        incident.resolution = detail
        incident.resolved_at = datetime.utcnow()

    event_detail = assigned_to if payload.action == "assign" else detail
    db.add(IncidentEvent(
        incident_id=incident_id,
        event_type=payload.action,
        detail=event_detail,
    ))
    db.commit()
    db.refresh(incident)
    return {
        "incident_id": incident_id,
        "action": payload.action,
        "status": incident.status,
        "detail": event_detail,
        "created_at": datetime.utcnow().isoformat(),
    }
