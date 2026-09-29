import json
from pathlib import Path

from app.database.database import SessionLocal, engine
from app.database.models import Base, IncidentRecord


def seed_demo_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    existing = db.query(IncidentRecord).count()
    if existing:
        print("Demo data already loaded.")
        return

    data_path = Path(__file__).resolve().parent.parent / "sample-data" / "incidents.json"
    if not data_path.exists():
        print("Sample incident file not found.")
        return

    incidents = json.loads(data_path.read_text())
    for incident in incidents:
        record = IncidentRecord(
            incident_id=incident["incident_id"],
            title=incident["title"],
            service=incident["service"],
            severity=incident["severity"],
            status=incident["status"],
            symptoms=incident["symptoms"],
            error_logs=incident["error_logs"],
            affected_components=incident.get("affected_components", ""),
            deployment_version=incident.get("deployment_version", ""),
            environment=incident.get("environment", "production"),
            root_cause=incident.get("root_cause", ""),
            investigation_steps=incident.get("investigation_steps", ""),
            actions_taken=incident.get("actions_taken", ""),
            runbook_used=incident.get("runbook_used", ""),
            resolution=incident.get("resolution", ""),
            resolution_time=incident.get("resolution_time", 0),
            successful=incident.get("successful", False),
            postmortem=incident.get("postmortem", ""),
            lessons_learned=incident.get("lessons_learned", ""),
            confidence=incident.get("confidence", 0.0),
        )
        db.add(record)
    db.commit()
    print(f"Seeded {len(incidents)} synthetic incidents.")


if __name__ == "__main__":
    seed_demo_data()
