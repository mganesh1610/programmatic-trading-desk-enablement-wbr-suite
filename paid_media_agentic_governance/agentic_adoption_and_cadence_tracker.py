#!/usr/bin/env python3
"""
Paid Media Agentic Adoption, Change Management & Cadence Governance Module (P1 Extension)
=========================================================================================
Tracks Concept -> Pilot -> Production agent rollouts across Paid Search (SA360 / Google Ads),
Programmatic (DV360), Paid Social (Meta Ads), and Media Campaign Planning across daily,
weekly, monthly, and quarterly review cadences, SME adoption feedback loops, and RICE
enhancement prioritization across 120,000+ campaign & enablement logs.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List

MODULE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = MODULE_DIR / "outputs"


def run_adoption_and_cadence_module() -> Dict[str, Any]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    db_path = OUTPUT_DIR / "paid_media_agentic_cadence.db"
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    cur.executescript(
        """
        CREATE TABLE paid_media_agent_cadence_logs (
            cohort_id TEXT PRIMARY KEY,
            media_workstream TEXT NOT NULL,
            platform_stack TEXT NOT NULL,
            review_cadence TEXT NOT NULL,
            deployment_stage TEXT NOT NULL,
            evaluated_campaign_logs INTEGER NOT NULL,
            sme_trained_specialists INTEGER NOT NULL,
            pre_adoption_cycle_hours REAL NOT NULL,
            post_adoption_cycle_hours REAL NOT NULL,
            sla_compliance_pct REAL NOT NULL,
            feedback_loop_enhancements_logged INTEGER NOT NULL,
            rice_priority_score REAL NOT NULL
        );
        """
    )

    cohorts = [
        (
            "CAD-SRCH-D1",
            "Paid Search",
            "SA360, Google Ads",
            "Daily",
            "Production",
            34200,
            18,
            14.5,
            8.8,
            96.4,
            14,
            248.0,
        ),
        (
            "CAD-PROG-W1",
            "Programmatic",
            "DV360, CM360, The Trade Desk",
            "Weekly",
            "Production",
            38400,
            22,
            18.0,
            11.0,
            95.9,
            19,
            312.5,
        ),
        (
            "CAD-SOCL-M1",
            "Paid Social",
            "Meta Ads, GA4",
            "Monthly",
            "Production",
            27600,
            16,
            12.0,
            7.5,
            95.4,
            11,
            195.0,
        ),
        (
            "CAD-PLAN-Q1",
            "Media Campaign Planning",
            "Advanced Excel, SQL Joins & CTEs, Power BI, Tableau",
            "Quarterly",
            "Production",
            19800,
            14,
            22.0,
            13.9,
            95.7,
            16,
            284.0,
        ),
    ]

    cur.executemany(
        "INSERT INTO paid_media_agent_cadence_logs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        cohorts,
    )
    conn.commit()

    query = """
    WITH workstream_rollup AS (
        SELECT
            cohort_id,
            media_workstream,
            platform_stack,
            review_cadence,
            deployment_stage,
            evaluated_campaign_logs,
            sme_trained_specialists,
            pre_adoption_cycle_hours,
            post_adoption_cycle_hours,
            ROUND((1.0 - (post_adoption_cycle_hours / pre_adoption_cycle_hours)) * 100.0, 2) AS velocity_improvement_pct,
            sla_compliance_pct,
            feedback_loop_enhancements_logged,
            rice_priority_score
        FROM paid_media_agent_cadence_logs
    )
    SELECT * FROM workstream_rollup ORDER BY rice_priority_score DESC;
    """
    cur.execute(query)
    cols = [d[0] for d in cur.description]
    rows = [dict(zip(cols, r)) for r in cur.fetchall()]
    conn.close()

    total_logs = sum(r["evaluated_campaign_logs"] for r in rows)
    total_pre_hours = sum(r["pre_adoption_cycle_hours"] for r in rows)
    total_post_hours = sum(r["post_adoption_cycle_hours"] for r in rows)
    overall_velocity_gain_pct = round(
        (1.0 - (total_post_hours / total_pre_hours)) * 100.0, 2
    )
    mean_sla_pct = round(
        sum(r["sla_compliance_pct"] * r["evaluated_campaign_logs"] for r in rows)
        / total_logs,
        2,
    )

    summary = {
        "total_evaluated_campaign_logs": total_logs,
        "overall_velocity_improvement_pct": overall_velocity_gain_pct,
        "weighted_sla_compliance_pct": mean_sla_pct,
        "total_sme_specialists_trained": sum(r["sme_trained_specialists"] for r in rows),
        "total_feedback_enhancements_prioritized": sum(
            r["feedback_loop_enhancements_logged"] for r in rows
        ),
        "cadences_covered": ["Daily", "Weekly", "Monthly", "Quarterly"],
        "workstream_summary": rows,
    }
    (OUTPUT_DIR / "paid_media_agentic_cadence_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    return summary


if __name__ == "__main__":
    res = run_adoption_and_cadence_module()
    print(json.dumps(res, indent=2))
