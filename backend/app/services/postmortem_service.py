from __future__ import annotations


class PostmortemService:
    def generate_postmortem(self, incident: dict) -> dict:
        return {
            "incident_summary": incident.get("title", "Incident"),
            "impact": f"Affected {incident.get('service', 'service')} in {incident.get('environment', 'production')}.",
            "timeline": "Incident detected -> investigation -> mitigation -> validation -> resolution.",
            "symptoms": incident.get("symptoms", ""),
            "root_cause": incident.get("root_cause", "Under investigation"),
            "investigation": incident.get("investigation_steps", "Investigation completed."),
            "actions_taken": incident.get("actions_taken", "No actions recorded."),
            "resolution": incident.get("resolution", "Resolution completed."),
            "what_worked": "Use of historical memory and runbook guidance.",
            "what_did_not_work": "Initial assumption without enough evidence.",
            "preventive_actions": [
                "Add alerting for dependency capacity thresholds.",
                "Improve deployment validation checks.",
                "Store lessons learned in Hindsight memory.",
            ],
            "lessons_learned": incident.get("lessons_learned", "No lesson recorded."),
        }
