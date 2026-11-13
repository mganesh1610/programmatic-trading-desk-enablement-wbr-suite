-- AI-Assisted AdOps SLA Governance & GTM/GA4/Adobe Tag Parity SQL Mart
-- Compatible with SQLite, BigQuery, Snowflake, and PostgreSQL.

WITH ticket_summary AS (
    SELECT
        routing_tier,
        CASE WHEN reassignment_count = 0 THEN 'First-Touch Resolved' ELSE 'Reassigned Escalation' END AS resolution_path,
        COUNT(*) AS ticket_count,
        SUM(made_sla) AS sla_met_tickets,
        ROUND(100.0 * SUM(made_sla) / NULLIF(COUNT(*), 0), 2) AS sla_compliance_pct,
        ROUND(AVG(resolution_hours), 2) AS mean_resolution_hours
    FROM fct_consolidated_tickets
    GROUP BY
        routing_tier,
        CASE WHEN reassignment_count = 0 THEN 'First-Touch Resolved' ELSE 'Reassigned Escalation' END
)
SELECT * FROM ticket_summary
ORDER BY routing_tier, resolution_path;

WITH tag_parity AS (
    SELECT
        traffic_type,
        COUNT(*) AS total_sessions,
        SUM(gtm_fired) AS gtm_tags_fired,
        SUM(revenue_converted) AS conversions,
        SUM(ga4_adobe_mismatch) AS parity_mismatches
    FROM fct_gtm_tag_telemetry
    GROUP BY traffic_type
)
SELECT
    traffic_type,
    total_sessions,
    gtm_tags_fired,
    ROUND(100.0 * gtm_tags_fired / NULLIF(total_sessions, 0), 2) AS gtm_fire_rate_pct,
    conversions,
    parity_mismatches
FROM tag_parity
ORDER BY total_sessions DESC;
