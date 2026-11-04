# Alignment — Customer Churn and Revenue Analytics

Main README (original LinkedIn description) vs files in this repo.
Sample data is synthetic (1,000 customers); original production
figures are NOT claimed as results of this starter code.
See CODE_AND_DATA_README.md.

| README claim | Representation in this repo | Status |
|---|---|---|
| SQL cohort retention + RFM segmentation | `sql/cohort_retention.sql`, `sql/rfm_segmentation.sql`, `src/analysis.py` | SQL + pandas, with documented proxies (no signup/transaction dates in sample) |
| 7,000+ telecom records | Sample is 1,000 synthetic customers | Demo only, NOT 7,000 |
| $1.5M at-risk revenue, 4 segments | Sample at-risk revenue is $292,202.16 (sample-only, in analysis output); sample segments are Early / Mid Standard / Mid Premium / Long Tenure | Sample figure only, NOT $1.5M |
| Power BI star schema + DAX + RLS by region | `sql/star_schema.sql`, `dax_measures.txt` (measures + RLS role example) | Example only; no .pbix file |
| Tableau executive dashboard | `tableau_notes.md` (rebuild steps) + `dashboard/app.py` (Streamlit) + charts in `outputs/charts/` | Notes + Streamlit, no .twbx file |
| Excel | `src/export_to_excel.py` + `outputs/customer_churn_sample.xlsx` | Sample workbook, 4 sheets (Customers + 3 summaries, with at-risk revenue column) |
| One-page executive memo, 3 retention actions, +8% projection | `docs/executive_memo.md` (3 actions, sample findings only) | Memo is sample-based; +8% is NOT claimed for the sample |

What was fixed in the 2026-11-04 review: added star-schema SQL,
Excel export + workbook, RLS example in DAX file, and the executive
memo — all four were previously missing or only mentioned. No main
README content was changed.
