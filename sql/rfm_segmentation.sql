-- RFM-style segmentation (starter / sample-data version)
-- ------------------------------------------------------------------
-- The sample file has no transaction dates or transaction counts, so
-- proxies are used and must be replaced with real fields when available:
--   Recency proxy   = tenure_months (longer tenure = more established)
--   Frequency proxy = tenure_months (months active, as activity proxy)
--   Monetary        = total_charges
--
-- Scores are quartiles (NTILE(4)) within the sample. In a real model,
-- Recency would normally be days since last purchase (lower = better),
-- so reverse the R score direction for real transaction data.
--
-- Dialect note: NTILE window functions work in Snowflake, BigQuery,
-- Postgres and DuckDB. Adjust table/column quoting as needed.

WITH scored AS (
    SELECT
        customer_id,
        region,
        tenure_months,
        monthly_charges,
        total_charges,
        churn,
        NTILE(4) OVER (ORDER BY tenure_months) AS r_score,
        NTILE(4) OVER (ORDER BY tenure_months) AS f_score,
        NTILE(4) OVER (ORDER BY total_charges) AS m_score
    FROM sample_customers
),
segmented AS (
    SELECT
        *,
        CAST(r_score AS VARCHAR) || CAST(f_score AS VARCHAR)
            || CAST(m_score AS VARCHAR) AS rfm_segment
    FROM scored
)
SELECT
    rfm_segment,
    COUNT(*) AS customers,
    AVG(churn) AS churn_rate,
    AVG(monthly_charges) AS avg_monthly_charges,
    SUM(total_charges) AS total_charges_sum
FROM segmented
GROUP BY rfm_segment
ORDER BY customers DESC;
