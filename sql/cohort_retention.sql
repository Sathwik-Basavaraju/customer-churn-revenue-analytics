-- Cohort retention (starter / sample-data version)
-- ------------------------------------------------------------------
-- The sample file has no signup date, so the cohort is a TENURE BUCKET
-- used as a proxy for cohort. Replace tenure_bucket with a real signup
-- cohort (e.g. DATE_TRUNC('month', signup_date)) when real data is used.
--
-- Retention in this proxy = share of customers in the bucket who did
-- NOT churn (1 - churn rate). Tenure buckets:
--   0-11 months, 12-24 months, 25-36 months, 37+ months
--
-- Dialect note: standard SQL; CASE / GROUP BY work in most warehouses
-- (Snowflake, BigQuery, Postgres, DuckDB). Adjust quoting as needed.

SELECT
    CASE
        WHEN tenure_months < 12 THEN '0-11 months'
        WHEN tenure_months <= 24 THEN '12-24 months'
        WHEN tenure_months <= 36 THEN '25-36 months'
        ELSE '37+ months'
    END AS tenure_cohort,
    COUNT(*) AS customers,
    SUM(churn) AS churned_customers,
    COUNT(*) - SUM(churn) AS retained_customers,
    1.0 - AVG(churn) AS retention_rate,
    AVG(churn) AS churn_rate
FROM sample_customers
GROUP BY 1
ORDER BY tenure_cohort;
