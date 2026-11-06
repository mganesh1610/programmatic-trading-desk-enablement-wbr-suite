-- ============================================================================
-- Programmatic Trading Desk Enablement, SLA Governance & WBR Analytics Suite
-- Dialect: Standard SQL / Google BigQuery / PostgreSQL Compatible
-- ============================================================================

CREATE TABLE IF NOT EXISTS dim_trading_desk_accounts (
    account_id VARCHAR(32) PRIMARY KEY,
    agency_or_advertiser_name VARCHAR(128) NOT NULL,
    vertical_category VARCHAR(64) NOT NULL, -- E-Commerce, Retail, Automotive, Entertainment
    assigned_consultant_id VARCHAR(32) NOT NULL,
    onboarding_cohort_month DATE NOT NULL,
    annual_programmatic_budget_usd NUMERIC(14, 2) NOT NULL,
    dmp_cdp_integrated BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS fact_consultant_enablement_events (
    event_id VARCHAR(40) PRIMARY KEY,
    account_id VARCHAR(32) NOT NULL,
    consultant_id VARCHAR(32) NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    service_type VARCHAR(64) NOT NULL, -- Custom_Training, Strategy_Session, Tech_Troubleshooting, Workflow_Audit
    certification_module_completed BOOLEAN DEFAULT FALSE,
    self_service_campaign_launches INT DEFAULT 0,
    assisted_campaign_launches INT DEFAULT 0,
    csat_score NUMERIC(4, 2)
);

CREATE TABLE IF NOT EXISTS fact_technical_escalations_sla (
    ticket_id VARCHAR(40) PRIMARY KEY,
    account_id VARCHAR(32) NOT NULL,
    consultant_id VARCHAR(32) NOT NULL,
    issue_category VARCHAR(64) NOT NULL, -- RTB_Deal_Pacing, Bid_Shading_Config, DMP_CDP_Sync, VAST_Verification_QA, Attribution_Tracking
    severity_tier VARCHAR(16) NOT NULL, -- P1_Critical, P2_High, P3_Standard
    opened_at TIMESTAMP NOT NULL,
    resolved_at TIMESTAMP NOT NULL,
    sla_target_hours NUMERIC(6, 2) NOT NULL,
    actual_resolution_hours NUMERIC(6, 2) NOT NULL,
    feature_blocker_code VARCHAR(32)
);

-- ============================================================================
-- Analytical Query 1: Weekly Business Review (WBR) Category & Self-Sufficiency Rollup
-- Uses SQL Joins & CTEs for executive WBR scorecard generation
-- ============================================================================
WITH account_enablement_cte AS (
    SELECT
        a.vertical_category,
        a.account_id,
        a.dmp_cdp_integrated,
        COUNT(CASE WHEN e.certification_module_completed THEN 1 END) AS certified_modules,
        SUM(e.self_service_campaign_launches) AS self_service_launches,
        SUM(e.assisted_campaign_launches) AS assisted_launches,
        AVG(e.csat_score) AS avg_csat
    FROM dim_trading_desk_accounts a
    LEFT JOIN fact_consultant_enablement_events e
        ON a.account_id = e.account_id
    GROUP BY a.vertical_category, a.account_id, a.dmp_cdp_integrated
),
sla_performance_cte AS (
    SELECT
        a.vertical_category,
        COUNT(t.ticket_id) AS total_tickets,
        AVG(t.actual_resolution_hours) AS mean_mttr_hours,
        SUM(CASE WHEN t.actual_resolution_hours <= t.sla_target_hours THEN 1 ELSE 0 END) * 100.0
            / NULLIF(COUNT(t.ticket_id), 0) AS sla_attainment_pct
    FROM dim_trading_desk_accounts a
    JOIN fact_technical_escalations_sla t
        ON a.account_id = t.account_id
    GROUP BY a.vertical_category
)
SELECT
    e.vertical_category,
    COUNT(DISTINCT e.account_id) AS active_enterprise_accounts,
    ROUND(SUM(e.self_service_launches) * 100.0 / NULLIF(SUM(e.self_service_launches + e.assisted_launches), 0), 2) AS trading_desk_self_sufficiency_pct,
    ROUND(AVG(e.avg_csat), 2) AS category_csat_score,
    ROUND(s.mean_mttr_hours, 2) AS mean_resolution_hours,
    ROUND(s.sla_attainment_pct, 2) AS sla_compliance_pct
FROM account_enablement_cte e
JOIN sla_performance_cte s
    ON e.vertical_category = s.vertical_category
GROUP BY e.vertical_category, s.mean_mttr_hours, s.sla_attainment_pct
ORDER BY trading_desk_self_sufficiency_pct DESC;
