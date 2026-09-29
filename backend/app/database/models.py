from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.sql import func

from app.database.database import Base


class IncidentRecord(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    service = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    status = Column(String, nullable=False, default="OPEN")
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    symptoms = Column(Text, nullable=True)
    error_logs = Column(Text, nullable=True)
    affected_components = Column(Text, nullable=True)
    deployment_version = Column(String, nullable=True)
    environment = Column(String, nullable=True)
    root_cause = Column(Text, nullable=True)
    investigation_steps = Column(Text, nullable=True)
    actions_taken = Column(Text, nullable=True)
    runbook_used = Column(String, nullable=True)
    resolution = Column(Text, nullable=True)
    resolution_time = Column(Integer, nullable=True, default=0)
    successful = Column(Boolean, default=False)
    postmortem = Column(Text, nullable=True)
    lessons_learned = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    similarity_summary = Column(Text, nullable=True)
    memory_context = Column(Text, nullable=True)
    confidence = Column(Float, nullable=True)


class IncidentEvent(Base):
    __tablename__ = "incident_events"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(String, index=True, nullable=False)
    event_type = Column(String, nullable=False)
    detail = Column(Text, nullable=False, default="")
    actor = Column(String, nullable=False, default="SOC operator")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
