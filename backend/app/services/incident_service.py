from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.database.models import IncidentRecord
from app.models.incident import IncidentCreate, IncidentOut, IncidentStatus


class IncidentService:
    def __init__(self, db: Session):
        self.db = db

    def create_incident(self, payload: IncidentCreate) -> IncidentRecord:
        incident_id = f"INC-{uuid.uuid4().hex[:8].upper()}"
        incident = IncidentRecord(
            incident_id=incident_id,
            title=payload.title,
            service=payload.service,
            severity=payload.severity.value,
            status=payload.status.value,
            symptoms=payload.symptoms,
            error_logs=payload.error_logs,
            affected_components=payload.affected_components,
            deployment_version=payload.deployment_version,
            environment=payload.environment,
            root_cause=payload.root_cause,
            investigation_steps=payload.investigation_steps,
            actions_taken=payload.actions_taken,
            runbook_used=payload.runbook_used,
            resolution=payload.resolution,
            resolution_time=payload.resolution_time,
            successful=payload.successful,
            postmortem=payload.postmortem,
            lessons_learned=payload.lessons_learned,
            created_at=datetime.utcnow(),
        )
        self.db.add(incident)
        self.db.commit()
        self.db.refresh(incident)
        return incident

    def get_all(self):
        return self.db.query(IncidentRecord).order_by(IncidentRecord.created_at.desc()).all()

    def get_by_id(self, incident_id: str):
        return self.db.query(IncidentRecord).filter(IncidentRecord.incident_id == incident_id).first()

    def resolve(self, incident_id: str, root_cause: str, resolution: str, successful: bool = True, runbook_used: str = "") -> IncidentRecord:
        incident = self.get_by_id(incident_id)
        if not incident:
            raise ValueError("Incident not found")
        incident.root_cause = root_cause or incident.root_cause
        incident.resolution = resolution or incident.resolution
        incident.successful = successful
        incident.status = IncidentStatus.RESOLVED.value
        incident.runbook_used = runbook_used or incident.runbook_used
        incident.resolved_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(incident)
        return incident

    def update_incident(self, incident_id: str, **kwargs) -> IncidentRecord:
        incident = self.get_by_id(incident_id)
        if not incident:
            raise ValueError("Incident not found")
        for key, value in kwargs.items():
            if hasattr(incident, key):
                setattr(incident, key, value)
        self.db.commit()
        self.db.refresh(incident)
        return incident
