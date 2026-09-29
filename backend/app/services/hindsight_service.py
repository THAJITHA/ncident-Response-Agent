from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.config import get_settings
from app.database.database import Base, engine
from app.database.models import IncidentRecord


class HindsightService:
    """Local Hindsight adapter.

    This keeps the Hindsight integration isolated and intentionally avoids claiming a
    remote official SDK/API contract where that was not verified in this environment.
    The service exposes the conceptual Hindsight operations requested by the project,
    while using the local SQLite database as the persistent memory layer.
    """

    def __init__(self, db: Session | None = None):
        self.db = db
        self.settings = get_settings()

    def is_available(self) -> bool:
        return bool(self.settings.hindsight_url or self.settings.hindsight_api_key)

    def _ensure_db(self):
        Base.metadata.create_all(bind=engine)
        if self.db is None:
            from app.database.database import SessionLocal

            self.db = SessionLocal()

    def store_incident_memory(self, incident_data: dict[str, Any]) -> dict[str, Any]:
        self._ensure_db()
        incident = IncidentRecord(
            incident_id=incident_data["incident_id"],
            title=incident_data["title"],
            service=incident_data["service"],
            severity=incident_data["severity"],
            status=incident_data.get("status", "OPEN"),
            symptoms=incident_data.get("symptoms", ""),
            error_logs=incident_data.get("error_logs", ""),
            affected_components=incident_data.get("affected_components", ""),
            deployment_version=incident_data.get("deployment_version", ""),
            environment=incident_data.get("environment", "production"),
            root_cause=incident_data.get("root_cause", ""),
            investigation_steps=incident_data.get("investigation_steps", ""),
            actions_taken=incident_data.get("actions_taken", ""),
            runbook_used=incident_data.get("runbook_used", ""),
            resolution=incident_data.get("resolution", ""),
            resolution_time=incident_data.get("resolution_time", 0),
            successful=incident_data.get("successful", False),
            postmortem=incident_data.get("postmortem", ""),
            lessons_learned=incident_data.get("lessons_learned", ""),
            similarity_summary=incident_data.get("similarity_summary", ""),
            memory_context=json.dumps(incident_data.get("memory_context", {}), default=str),
            confidence=incident_data.get("confidence", 0.0),
        )
        self.db.add(incident)
        self.db.commit()
        self.db.refresh(incident)
        return {"status": "stored", "incident_id": incident.incident_id}

    def recall_relevant_incidents(self, query: str, limit: int = 5):
        self._ensure_db()
        incidents = self.db.query(IncidentRecord).all()
        ordered = []
        query_lower = (query or "").lower()
        for incident in incidents:
            text = " ".join(
                [
                    incident.title or "",
                    incident.service or "",
                    incident.symptoms or "",
                    incident.error_logs or "",
                    incident.root_cause or "",
                    incident.actions_taken or "",
                    incident.runbook_used or "",
                    incident.lessons_learned or "",
                ]
            ).lower()
            score = 0
            if incident.service.lower() in query_lower:
                score += 3
            if incident.runbook_used and incident.runbook_used.lower() in query_lower:
                score += 2
            for term in query_lower.split():
                if term and term in text:
                    score += 1
            if score > 0 or not query_lower:
                ordered.append({
                    "incident_id": incident.incident_id,
                    "service": incident.service,
                    "title": incident.title,
                    "symptoms": incident.symptoms,
                    "root_cause": incident.root_cause,
                    "runbook_used": incident.runbook_used,
                    "resolution": incident.resolution,
                    "resolution_time": incident.resolution_time,
                    "lessons_learned": incident.lessons_learned,
                    "status": incident.status,
                    "confidence": min(0.98, round(score / max(1, len(query_lower.split()) + 1), 2)),
                    "date": incident.created_at,
                })
        ordered.sort(key=lambda x: x["confidence"], reverse=True)
        return ordered[:limit]

    def list_incidents(self):
        self._ensure_db()
        return self.db.query(IncidentRecord).order_by(IncidentRecord.created_at.desc()).all()

    def get_incident_by_id(self, incident_id: str):
        self._ensure_db()
        return self.db.query(IncidentRecord).filter(IncidentRecord.incident_id == incident_id).first()

    def get_memories(self):
        self._ensure_db()
        incidents = self.db.query(IncidentRecord).all()
        memories = []
        for incident in incidents:
            memories.append({
                "incident_id": incident.incident_id,
                "title": incident.title,
                "service": incident.service,
                "symptoms": incident.symptoms,
                "root_cause": incident.root_cause,
                "runbook_used": incident.runbook_used,
                "resolution": incident.resolution,
                "resolution_time": incident.resolution_time,
                "lessons_learned": incident.lessons_learned,
                "similarity": 0.86,
            })
        return memories
