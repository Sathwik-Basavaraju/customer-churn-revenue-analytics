"""Starter analysis for the synthetic Customer Churn sample data.

Reads data/sample_customers.csv (project root), computes:
  - churn rate overall and by segment / region / contract_type
  - at-risk revenue on the SAMPLE ONLY:
        sum(monthly_charges * 12) for churned customers
    This is a sample-only figure. It does NOT reproduce the original
    project's $1.5M at-risk revenue figure.
  - an RFM-style summary. The sample has no transaction dates, so
    proxies are used and documented here:
        Recency proxy    = tenure_months (longer tenure = more established)
        Frequency proxy  = tenure_months (months active, as an activity proxy)
        Monetary         = total_charges
    Scores are quartile ranks (1-4) within the sample.

Creates charts (pandas + matplotlib only) in outputs/charts/:
  churn_by_segment.png, churn_by_contract.png,
  monthly_charges_distribution.png, at_risk_revenue_by_segment.png

Usage:
    python3 src/analysis.py
    python3 src/analysis.py --input data/sample_customers.csv
"""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = PROJECT_ROOT / "data" / "sample_customers.csv"
DEFAULT_CHART_DIR = PROJECT_ROOT / "outputs" / "charts"


def churn_rate(df: pd.DataFrame, by: str) -> pd.DataFrame:
    """Churn rate and customer count grouped by `by`."""
    grouped = df.groupby(by)["churn"].agg(["mean", "count", "sum"])
    grouped.columns = ["churn_rate", "customers", "churned"]
    return grouped.reset_index().sort_values("churn_rate", ascending=False)


def rfm_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Quartile RFM scores using the documented proxies."""
    out = df.copy()
    # qcut can fail on many ties; fall back to rank-based bins.
    for col, score_col in [
        ("tenure_months", "r_score"),
        ("tenure_months", "f_score"),
        ("total_charges", "m_score"),
    ]:
        try:
            out[score_col] = pd.qcut(out[col], 4, labels=[1, 2, 3, 4]).astype(int)
        except ValueError:
            out[score_col] = pd.cut(
                out[col].rank(method="first"), 4, labels=[1, 2, 3, 4]
            ).astype(int)
    out["rfm_segment"] = (
        out["r_score"].astype(str)
        + out["f_score"].astype(str)
        + out["m_score"].astype(str)
    )
    summary = (
        out.groupby("rfm_segment")
        .agg(customers=("customer_id", "count"), churn_rate=("churn", "mean"))
        .reset_index()
        .sort_values("customers", ascending=False)
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--chart-dir", type=Path, default=DEFAULT_CHART_DIR)
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    args.chart_dir.mkdir(parents=True, exist_ok=True)

    overall = df["churn"].mean()
    print(f"Customers: {len(df)}")
    print(f"Overall churn rate: {overall:.2%}")

    by_segment = churn_rate(df, "segment")
    by_region = churn_rate(df, "region")
    by_contract = churn_rate(df, "contract_type")
    print("\nChurn by segment:\n", by_segment.to_string(index=False))
    print("\nChurn by region:\n", by_region.to_string(index=False))
    print("\nChurn by contract:\n", by_contract.to_string(index=False))

    # Sample-only at-risk revenue: 12 months of monthly charges for churned.
    churned = df[df["churn"] == 1].copy()
    churned["at_risk_annual"] = churned["monthly_charges"] * 12
    at_risk_total = churned["at_risk_annual"].sum()
    print(
        f"\nAt-risk revenue (SAMPLE ONLY, churned x monthly x 12): "
        f"${at_risk_total:,.2f}"
    )
    at_risk_by_segment = (
        churned.groupby("segment")["at_risk_annual"].sum().sort_values(ascending=False)
    )
    print("\nAt-risk revenue by segment (sample only):\n", at_risk_by_segment)

    rfm = rfm_summary(df)
    print("\nRFM summary (top 10 segments):\n", rfm.head(10).to_string(index=False))

    # --- Charts (matplotlib only) ---
    plt.figure()
    by_segment.plot.bar(x="segment", y="churn_rate", legend=False)
    plt.ylabel("Churn rate")
    plt.title("Churn rate by segment")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(args.chart_dir / "churn_by_segment.png", dpi=150)
    plt.close()

    plt.figure()
    by_contract.plot.bar(x="contract_type", y="churn_rate", legend=False)
    plt.ylabel("Churn rate")
    plt.title("Churn rate by contract type")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(args.chart_dir / "churn_by_contract.png", dpi=150)
    plt.close()

    plt.figure()
    df["monthly_charges"].plot.hist(bins=20)
    plt.xlabel("Monthly charges ($)")
    plt.ylabel("Customers")
    plt.title("Monthly charges distribution")
    plt.tight_layout()
    plt.savefig(args.chart_dir / "monthly_charges_distribution.png", dpi=150)
    plt.close()

    plt.figure()
    at_risk_by_segment.plot.bar()
    plt.ylabel("At-risk annual revenue ($) - sample only")
    plt.title("At-risk revenue by segment (sample only)")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(args.chart_dir / "at_risk_revenue_by_segment.png", dpi=150)
    plt.close()

    print(f"\nCharts written to {args.chart_dir}")


if __name__ == "__main__":
    main()
