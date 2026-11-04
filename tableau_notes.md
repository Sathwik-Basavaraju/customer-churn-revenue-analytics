# Rebuilding the executive dashboard in Tableau

Use `data/sample_customers.csv` as the data source (Text File connection).
All figures below are sample-only and do not reproduce the original
project's figures.

## Fields to use

- Dimensions: `region`, `segment`, `contract_type`, `payment_method`
- Measures: `churn` (average = churn rate, sum = churned count),
  `monthly_charges` (average and sum), `total_charges` (sum)
- Calculated field — At-Risk Revenue (sample only):
  `IF [churn] = 1 THEN [monthly_charges] * 12 ELSE 0 END`
  Then sum that field for the at-risk total.

## Sheets to build

1. **Churn by segment**
   - Rows: `segment`
   - Columns: `AVG(churn)` formatted as a percentage
   - Bar chart, sorted descending by churn rate. Add customer count
     (`COUNT(customer_id)`) to the tooltip.

2. **Churn by region**
   - Rows: `region`
   - Columns: `AVG(churn)` formatted as a percentage
   - Bar chart, sorted descending. Colour by churn rate if desired.

3. **Revenue at risk**
   - Rows: `segment`
   - Columns: `SUM(At-Risk Revenue)` (the calculated field above)
   - Bar chart. Title it clearly as "Sample only" so the sample total
     is not mistaken for the original project's revenue figure.

## Dashboard assembly

- Put the three sheets on one dashboard with a title such as
  "Customer Churn and Revenue Analytics — Sample Data".
- Add filters for `region` and `contract_type` so viewers can slice
  churn and at-risk revenue.
- Add a KPI text box / BANs: total customers, churn rate,
  and at-risk revenue (sample only).
