import json
import sys
import unittest
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_DIR / "src"))

import sla_gtm_governance_pipeline as pipeline


class TestSlaGtmGovernance(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.summary = pipeline.main()

    def test_record_counts_and_consolidation(self) -> None:
        self.assertEqual(self.summary["combined_records_processed"], 154042)
        self.assertEqual(self.summary["incident_event_snapshots"], 141712)
        self.assertEqual(self.summary["unique_consolidated_tickets"], 24918)
        self.assertEqual(self.summary["distinct_assignment_queues"], 71)
        self.assertAlmostEqual(self.summary["event_row_consolidation_pct"], 82.42, places=2)

    def test_sla_lift_and_cycle_time_reduction(self) -> None:
        m = self.summary["sla_and_cycle_time_metrics"]
        self.assertGreater(m["sla_compliance_lift_pp"], 25.0)
        self.assertGreater(m["median_cycle_time_reduction_pct"], 40.0)

    def test_ai_escalation_classifier_auc(self) -> None:
        ml = self.summary["ai_escalation_risk_classifier"]
        self.assertGreaterEqual(ml["holdout_roc_auc"], 0.75)
        self.assertGreater(ml["top_20pct_breach_capture_pct"], 35.0)

    def test_gtm_ga4_adobe_audit(self) -> None:
        gtm = self.summary["gtm_ga4_adobe_tag_audit"]
        self.assertEqual(gtm["sessions_audited"], 12330)
        self.assertGreater(gtm["gtm_fire_rate_pct"], 90.0)
        self.assertGreater(gtm["ga4_adobe_parity_mismatches_isolated"], 0)

    def test_all_ten_qa_gates_passed(self) -> None:
        self.assertEqual(self.summary["governance_qa_gates_total"], 10)
        self.assertEqual(self.summary["governance_qa_gates_passed"], 10)
        out_json = pipeline.OUTPUTS_DIR / "sla_gtm_validation_summary.json"
        out_csv = pipeline.OUTPUTS_DIR / "queue_sla_performance.csv"
        self.assertTrue(out_json.is_file())
        self.assertTrue(out_csv.is_file())
        loaded = json.loads(out_json.read_text(encoding="utf-8"))
        self.assertEqual(loaded["governance_qa_gates_passed"], 10)


if __name__ == "__main__":
    unittest.main()
