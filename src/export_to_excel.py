"""Export the synthetic churn sample to Excel (sample only).

Writes outputs/customer_churn_sample.xlsx with sheets:
  Customers, Churn by Segment, Churn by Region, Churn by Contract,
  At-Risk Revenue (sample only).

Requires pandas + openpyxl. Run from the project root:
    python3 src/export_to_excel.py
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "data" / "sample_customers.csv"
OUTPUT = ROOT / "outputs" / "customer_churn_sample.xlsx"


def main() -> None:
    df = pd.read_csv(INPUT)
    df["at_risk_revenue_sample"] = df.apply(
        lambda r: r["monthly_charges"] * 12 if r["churn"] == 1 else 0, axis=1
    )

    def summary(col):
        g = df.groupby(col).agg(
            customers=("customer_id", "count"),
            churned=("churn", "sum"),
            churn_rate=("churn", "mean"),
            at_risk_revenue_sample=("at_risk_revenue_sample", "sum"),
        ).reset_index()
        return g

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(OUTPUT, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Customers", index=False)
        summary("segment").to_excel(writer, sheet_name="Churn by Segment", index=False)
        summary("region").to_excel(writer, sheet_name="Churn by Region", index=False)
        summary("contract_type").to_excel(writer, sheet_name="Churn by Contract", index=False)
    print(f"Wrote {OUTPUT} ({len(df)} customers, sample only)")


if __name__ == "__main__":
    main()
