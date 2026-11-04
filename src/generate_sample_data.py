"""Generate synthetic sample data for the Customer Churn starter project.

Deterministic: seed 42. Writes 1000 rows to data/sample_customers.csv
relative to the project root (the parent of this src/ directory).

Segment logic (documented, generator-derived -- NOT the original
project's 4 customer segments):
  - tenure_months < 12: "Early Tenure"
  - 12 <= tenure_months <= 36 and monthly_charges < 70: "Mid Tenure - Standard"
  - 12 <= tenure_months <= 36 and monthly_charges >= 70: "Mid Tenure - Premium"
  - tenure_months > 36: "Long Tenure"

Churn is assigned probabilistically: month-to-month contracts, short
tenure, and higher monthly charges raise churn probability. This is
synthetic demonstration data only and does NOT reproduce any original
project figure (including the original $1.5M at-risk revenue figure
from the LinkedIn project description).

Usage:
    python3 src/generate_sample_data.py
    python3 src/generate_sample_data.py --rows 1000 --seed 42
"""

import argparse
import csv
import random
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "sample_customers.csv"

REGIONS = ["North", "South", "East", "West"]
CONTRACTS = ["Month-to-month", "One year", "Two year"]
PAYMENTS = [
    "Electronic check",
    "Mailed check",
    "Bank transfer (automatic)",
    "Credit card (automatic)",
]


def segment_for(tenure_months: int, monthly_charges: float) -> str:
    """Derive segment from tenure and charges (see module docstring)."""
    if tenure_months < 12:
        return "Early Tenure"
    if tenure_months <= 36:
        return "Mid Tenure - Premium" if monthly_charges >= 70 else "Mid Tenure - Standard"
    return "Long Tenure"


def churn_probability(tenure_months: int, monthly_charges: float, contract: str) -> float:
    """Base churn probability, adjusted by contract, tenure and charges."""
    p = 0.18
    if contract == "Month-to-month":
        p += 0.22
    elif contract == "One year":
        p += 0.05
    # Two year: no addition.
    if tenure_months < 12:
        p += 0.12
    elif tenure_months > 36:
        p -= 0.08
    if monthly_charges >= 90:
        p += 0.08
    elif monthly_charges < 40:
        p -= 0.05
    return max(0.02, min(0.85, p))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    rows = []
    for i in range(1, args.rows + 1):
        region = rng.choice(REGIONS)
        contract = rng.choices(CONTRACTS, weights=[0.55, 0.25, 0.20])[0]
        payment = rng.choice(PAYMENTS)
        tenure_months = max(0, int(rng.gauss(28, 20)))
        monthly_charges = round(rng.uniform(20.0, 115.0), 2)
        # Total charges: tenure * monthly, with small noise, floored at 0.
        total_charges = round(
            max(0.0, tenure_months * monthly_charges + rng.gauss(0, 25)), 2
        )
        churn = 1 if rng.random() < churn_probability(
            tenure_months, monthly_charges, contract
        ) else 0
        segment = segment_for(tenure_months, monthly_charges)
        rows.append(
            {
                "customer_id": f"CUST-{i:05d}",
                "region": region,
                "segment": segment,
                "tenure_months": tenure_months,
                "monthly_charges": monthly_charges,
                "total_charges": total_charges,
                "contract_type": contract,
                "payment_method": payment,
                "churn": churn,
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "customer_id",
        "region",
        "segment",
        "tenure_months",
        "monthly_charges",
        "total_charges",
        "contract_type",
        "payment_method",
        "churn",
    ]
    with args.output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
