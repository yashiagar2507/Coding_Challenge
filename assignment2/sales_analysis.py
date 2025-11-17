"""
Assignment 2 – CSV Data Analysis using Functional Programming + Visualization

This program reads sales data from a CSV file and performs a series of analyses
using a functional programming approach. It calculates totals, groupings, and
trends, and plots a monthly revenue chart using Matplotlib.
"""

import csv
from dataclasses import dataclass
from typing import List, Dict, Tuple
from collections import defaultdict
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt


# Data model
@dataclass
class Sale:
    """Represents a single sale record."""
    order_id: str
    date: datetime
    region: str
    category: str
    product: str
    customer: str
    quantity: int
    unit_price: float
    discount: float

    @property
    def revenue(self) -> float:
        """Return the revenue for this sale after applying discount."""
        return self.quantity * self.unit_price * (1 - self.discount)


# Reading the CSV file
def read_sales(csv_path: str) -> List[Sale]:
    """Load sales data from a CSV file into a list of Sale objects."""
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        return [
            Sale(
                order_id=row["order_id"],
                date=datetime.strptime(row["date"], "%Y-%m-%d"),
                region=row["region"],
                category=row["category"],
                product=row["product"],
                customer=row["customer"],
                quantity=int(row["quantity"]),
                unit_price=float(row["unit_price"]),
                discount=float(row["discount"]),
            )
            for row in reader
        ]


# Analysis functions
def total_revenue(data: List[Sale]) -> float:
    """Return total revenue across all sales."""
    return round(sum(map(lambda s: s.revenue, data)), 2)


def revenue_by_region(data: List[Sale]) -> Dict[str, float]:
    """Return total revenue grouped by region."""
    result = defaultdict(float)
    for s in data:
        result[s.region] += s.revenue
    return dict(result)


def revenue_by_category(data: List[Sale]) -> Dict[str, float]:
    """Return total revenue grouped by product category."""
    result = defaultdict(float)
    for s in data:
        result[s.category] += s.revenue
    return dict(result)


def top_n_products_by_revenue(data: List[Sale], n: int = 5) -> List[Tuple[str, float]]:
    """Return the top N products ranked by total revenue."""
    product_revenue = defaultdict(float)
    for s in data:
        product_revenue[s.product] += s.revenue
    sorted_products = sorted(product_revenue.items(), key=lambda x: x[1], reverse=True)
    return sorted_products[:n]


def monthly_revenue_trend(data: List[Sale]) -> Dict[str, float]:
    """Return total revenue for each month (formatted as YYYY-MM)."""
    monthly = defaultdict(float)
    for s in data:
        key = s.date.strftime("%Y-%m")
        monthly[key] += s.revenue
    return dict(sorted(monthly.items()))


def average_discount_by_category(data: List[Sale]) -> Dict[str, float]:
    """Return the average discount value for each category."""
    sums = defaultdict(float)
    counts = defaultdict(int)
    for s in data:
        sums[s.category] += s.discount
        counts[s.category] += 1
    return {c: round(sums[c] / counts[c], 3) for c in sums}


def highest_order_value(data: List[Sale]) -> Tuple[str, float]:
    """Return the order ID and value of the highest-value order."""
    order_values = defaultdict(float)
    for s in data:
        order_values[s.order_id] += s.revenue
    order_id, value = max(order_values.items(), key=lambda x: x[1])
    return order_id, round(value, 2)


# Visualization
def plot_monthly_trend(data: List[Sale]):
    """Plot monthly revenue trend using Matplotlib."""
    trend = monthly_revenue_trend(data)
    months = list(trend.keys())
    revenues = list(trend.values())

    plt.figure(figsize=(10, 5))
    plt.plot(months, revenues, marker='o', color='blue', linewidth=2)
    plt.title("Monthly Revenue Trend - 2024")
    plt.xlabel("Month")
    plt.ylabel("Revenue ($)")
    plt.xticks(rotation=45)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()


# Report printer
def print_report(csv_path: str):
    """Read the CSV and print a formatted summary of all analyses."""
    data = read_sales(csv_path)
    print("\n=== SALES ANALYTICS REPORT ===")
    print(f"Total Records: {len(data)}")
    print(f"Total Revenue: ${total_revenue(data):,.2f}\n")

    print("Revenue by Region:")
    for region, rev in revenue_by_region(data).items():
        print(f"  {region:<10} ${rev:,.2f}")

    print("\nRevenue by Category:")
    for category, rev in revenue_by_category(data).items():
        print(f"  {category:<15} ${rev:,.2f}")

    print("\nTop 5 Products by Revenue:")
    for product, rev in top_n_products_by_revenue(data, 5):
        print(f"  {product:<15} ${rev:,.2f}")

    print("\nMonthly Revenue Trend:")
    for month, rev in monthly_revenue_trend(data).items():
        print(f"  {month}: ${rev:,.2f}")

    print("\nAverage Discount by Category:")
    for cat, avg in average_discount_by_category(data).items():
        print(f"  {cat:<15} {avg:.2%}")

    oid, value = highest_order_value(data)
    print(f"\nHighest Order Value: Order {oid} → ${value:,.2f}")


# Helper for file path
def default_csv_path() -> str:
    """Return the default path to sales.csv regardless of where the script runs."""
    here = Path(__file__).resolve()
    return str(here.with_name("data") / "sales.csv")


# Entry point
if __name__ == "__main__":
    csv_path = default_csv_path()
    data = read_sales(csv_path)
    print_report(csv_path)
    plot_monthly_trend(data)
