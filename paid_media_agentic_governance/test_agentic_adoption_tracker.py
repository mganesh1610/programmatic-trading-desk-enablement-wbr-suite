import unittest
from paid_media_agentic_governance.agentic_adoption_and_cadence_tracker import (
    run_adoption_and_cadence_module,
)


class TestAgenticAdoptionTracker(unittest.TestCase):
    def test_cadence_and_log_coverage(self):
        summary = run_adoption_and_cadence_module()
        self.assertEqual(summary["total_evaluated_campaign_logs"], 120000)
        self.assertEqual(
            set(summary["cadences_covered"]),
            {"Daily", "Weekly", "Monthly", "Quarterly"},
        )
        self.assertAlmostEqual(
            summary["overall_velocity_improvement_pct"], 38.05, places=1
        )
        self.assertGreater(summary["weighted_sla_compliance_pct"], 95.0)


if __name__ == "__main__":
    unittest.main()
