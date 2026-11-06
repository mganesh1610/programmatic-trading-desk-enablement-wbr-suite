import unittest
from src.enablement_wbr_engine import (
    compute_self_sufficiency_index,
    compute_rice_priority_score,
    run_pipeline,
)

class TestEnablementWBREngine(unittest.TestCase):
    def test_self_sufficiency_index_bounds(self):
        score = compute_self_sufficiency_index(750, 1000, 0.90, True)
        self.assertGreaterEqual(score, 80.0)
        self.assertLessEqual(score, 100.0)
        self.assertEqual(compute_self_sufficiency_index(0, 0, 0.5, False), 0.0)

    def test_rice_priority_score(self):
        rice = compute_rice_priority_score(60, 2.5, 90.0, 4.5)
        self.assertAlmostEqual(rice, 30.0, places=2)
        with self.assertRaises(ValueError):
            compute_rice_priority_score(50, 2.0, 80.0, 0.0)

    def test_end_to_end_pipeline_outputs(self):
        summary = run_pipeline(seed=42, total_events=120000)
        self.assertEqual(summary["total_campaign_support_logs_processed"], 120000)
        self.assertAlmostEqual(summary["overall_certification_velocity_lift_pct"], 38.0, delta=0.5)
        self.assertEqual(len(summary["vertical_breakdown"]), 4)
        self.assertEqual(len(summary["product_roadmap_proposals"]), 5)

if __name__ == "__main__":
    unittest.main()
