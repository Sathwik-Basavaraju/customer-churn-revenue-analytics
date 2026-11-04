-- Power BI star-schema model (EXAMPLE ONLY, for the synthetic sample).
-- The DAX measures in dax_measures.txt assume a single 'Customers'
-- table for simplicity. This file shows how that table can be
-- decomposed into a star schema for a fuller Power BI model.
-- These are example DDL statements, not a live deployment, and all
-- figures derived from them are sample-only.

-- Dimensions (distinct values from the sample Customers table)
CREATE TABLE dim_region (
    region_key INT PRIMARY KEY,
    region VARCHAR(50) NOT NULL
);

CREATE TABLE dim_segment (
    segment_key INT PRIMARY KEY,
    segment VARCHAR(100) NOT NULL
);

CREATE TABLE dim_contract (
    contract_key INT PRIMARY KEY,
    contract_type VARCHAR(50) NOT NULL
);

CREATE TABLE dim_payment (
    payment_key INT PRIMARY KEY,
    payment_method VARCHAR(100) NOT NULL
);

-- Fact table: one row per customer, with foreign keys to dimensions.
CREATE TABLE fact_customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    region_key INT REFERENCES dim_region (region_key),
    segment_key INT REFERENCES dim_segment (segment_key),
    contract_key INT REFERENCES dim_contract (contract_key),
    payment_key INT REFERENCES dim_payment (payment_key),
    tenure_months INT,
    monthly_charges DECIMAL(10, 2),
    total_charges DECIMAL(12, 2),
    churn INT -- 1 = churned, 0 = retained
);

-- Example population (adapt to your SQL dialect):
-- INSERT INTO dim_region SELECT DISTINCT ... FROM Customers;
-- INSERT INTO fact_customers SELECT ... JOIN dim_* ON ... FROM Customers;
