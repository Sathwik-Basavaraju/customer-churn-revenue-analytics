"""Streamlit dashboard for the synthetic Customer Churn sample data.

Reads data/sample_customers.csv relative to the project root.
Uses only Streamlit charts/tables -- no matplotlib dependency in the app.

At-risk revenue shown here is SAMPLE ONLY:
    sum(monthly_charges * 12) for churned customers.
It does NOT reproduce the original project's $1.5M figure.

Run from the project root:
    streamlit run dashboard/app.py
"""

from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "sample_customers.csv"


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    """Load the sample CSV."""
    return pd.read_csv(path)


def main() -> None:
    st.title("Customer Churn and Revenue Analytics (Sample Data)")
    st.caption(
        "Synthetic sample data for demonstration only. "
        "At-risk revenue below is sample-only and does not reproduce "
        "the original project's figures."
    )

    df = load_data(DATA_PATH)

    total = len(df)
    churned = int(df["churn"].sum())
    churn_rate = df["churn"].mean() if total else 0.0
    at_risk = float((df.loc[df["churn"] == 1, "monthly_charges"] * 12).sum())
    avg_monthly = float(df["monthly_charges"].mean()) if total else 0.0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total customers", f"{total:,}")
    col2.metric("Churn rate", f"{churn_rate:.1%}")
    col3.metric("Churned customers", f"{churned:,}")
    col4.metric("At-risk revenue (sample)", f"${at_risk:,.0f}")
    st.metric("Avg monthly charges", f"${avg_monthly:.2f}")

    st.subheader("Churn rate by segment")
    by_segment = df.groupby("segment")["churn"].mean().sort_values(ascending=False)
    st.bar_chart(by_segment)
    st.dataframe(by_segment.reset_index().rename(columns={"churn": "churn_rate"}))

    st.subheader("Churn rate by region")
    by_region = df.groupby("region")["churn"].mean().sort_values(ascending=False)
    st.bar_chart(by_region)
    st.dataframe(by_region.reset_index().rename(columns={"churn": "churn_rate"}))

    st.subheader("Churn rate by contract type")
    by_contract = df.groupby("contract_type")["churn"].mean().sort_values(ascending=False)
    st.bar_chart(by_contract)

    st.subheader("Customers by segment")
    st.dataframe(df["segment"].value_counts().reset_index())

    st.subheader("Sample data (first 100 rows)")
    st.dataframe(df.head(100))


if __name__ == "__main__":
    main()
