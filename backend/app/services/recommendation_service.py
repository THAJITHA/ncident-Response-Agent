from __future__ import annotations

from app.models.recommendation import RecommendationResponse


class RecommendationService:
    def build_recommendation(self, incident, similar_incidents: list[dict]) -> RecommendationResponse:
        if not similar_incidents:
            return RecommendationResponse(
                recommendation="Investigate recent deployment and service health metrics.",
                why="No direct historical memory matches were found for this incident.",
                historical_evidence="No similar incidents found.",
                related_incident_ids=[],
                previous_root_cause="",
                recommended_runbook="CHECK_DEPLOYMENT_HEALTH",
                expected_benefit="Reduce time to isolate deployment-related regression.",
                warning="Validate evidence before production action.",
                confidence=0.45,
            )

        best_match = similar_incidents[0]
        return RecommendationResponse(
            recommendation=f"Check {best_match.get('service', 'service')} resource saturation and recent deployment changes.",
            why=f"Previous incidents with similar symptoms were caused by {best_match.get('root_cause', 'unknown dependency degradation') }.",
            historical_evidence=", ".join(item["incident_id"] for item in similar_incidents[:3]),
            related_incident_ids=[item["incident_id"] for item in similar_incidents[:3]],
            previous_root_cause=best_match.get("root_cause", ""),
            recommended_runbook=best_match.get("runbook_used", "CHECK_DEPLOYMENT_HEALTH"),
            expected_benefit="Faster diagnosis and lower mean time to recovery.",
            warning="Verify current pool or saturation metrics before making a production change.",
            confidence=best_match.get("confidence", 0.7),
        )
