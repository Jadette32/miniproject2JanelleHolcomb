# Name: Janelle Holcomb
# Class: INF 601 – Programming with Python
# Project: Mini Project 2 – Pandas Data Exploration

import os
import random
from datetime import datetime, timedelta


import pandas as pd
import matplotlib.pyplot as plt
from faker import Faker

# ------------------ CONFIG ------------------
# TODO[1]: Change this to False when you switch to a CSV or API
USE_FAKER = True

# TODO[2]: If using a CSV later, put its path here (and set USE_FAKER=False)
CSV_PATH = "your_data.csv"  # e.g., "netflix_titles.csv"

# Charts output folder (rubric requires saving PNGs into charts/)
CHART_DIR = "charts"

# Random seed for reproducibility
SEED = 42
random.seed(SEED)


# ------------------ UTILITIES ------------------
def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def save_chart(fig, filename: str):
    """Save a matplotlib fig as a PNG into CHART_DIR and close it."""
    ensure_dir(CHART_DIR)
    fig.tight_layout()
    out_path = os.path.join(CHART_DIR, filename)
    fig.savefig(out_path, dpi=120)
    plt.close(fig)


# ------------------ DATA LOADING ------------------
def random_date(start: datetime, end: datetime) -> datetime:
    """Helper for Faker dates."""
    delta = end - start
    days = random.randint(0, delta.days)
    seconds = random.randint(0, 86399)
    return start + timedelta(days=days, seconds=seconds)


def load_data() -> pd.DataFrame:
    """
    Returns a DataFrame. Starts with Faker so it's runnable now.
    Later you can replace with CSV/API and keep the rest of the code unchanged.
    """
    if not USE_FAKER:
        # -------- CSV / API BRANCH --------
        # TODO[3]: Replace with your CSV/API code. Example for CSV:
        # df = pd.read_csv(CSV_PATH)
        # return df
        raise ValueError("Set USE_FAKER=True or implement CSV/API loading.")

    # -------- FAKER BRANCH (Default) --------
    fake = Faker()
    Faker.seed(SEED)

    categories = ["Toys", "Electronics", "Home", "Beauty", "Sports", "Books", "Groceries", "Clothing"]
    start = datetime(2024, 1, 1)
    end = datetime(2025, 9, 1)

    rows = []
    N = 300  # keep it quick to run; you can increase later
    for i in range(1, N + 1):
        cat = random.choice(categories)
        unit_price = {
            "Toys": (8, 35),
            "Electronics": (25, 250),
            "Home": (10, 120),
            "Beauty": (5, 60),
            "Sports": (10, 140),
            "Books": (6, 30),
            "Groceries": (2, 25),
            "Clothing": (8, 90),
        }[cat]
        qty = random.randint(1, 5)
        price = round(random.uniform(*unit_price), 2)
        discount = round(random.uniform(0, 0.25), 2)
        dt = random_date(start, end)

        rows.append({
            "order_id": i,
            "order_date": dt,
            "customer": fake.name(),
            "category": cat,
            "quantity": qty,
            "unit_price": price,
            "discount": discount,  # fraction (0–0.25)
        })

    df = pd.DataFrame(rows)

    # Basic engineered fields many questions need
    df["gross_revenue"] = df["quantity"] * df["unit_price"]
    df["net_revenue"] = df["gross_revenue"] * (1 - df["discount"])
    df["order_month"] = pd.to_datetime(df["order_date"]).dt.to_period("M").astype(str)

    return df


# ------------------ PLOTS ------------------
def plot_revenue_by_category(df: pd.DataFrame):
    """Bar chart example (works if you have 'category' and 'net_revenue')."""
    if not {"category", "net_revenue"}.issubset(df.columns):
        print("Skipping 'revenue by category' (required columns not found).")
        return
    cat = (
        df.groupby("category", as_index=False)["net_revenue"]
        .sum()
        .sort_values("net_revenue", ascending=False)
    )

    fig = plt.figure(figsize=(8, 5))
    plt.bar(cat["category"], cat["net_revenue"])
    plt.title("Revenue by Category")
    plt.xlabel("Category")
    plt.ylabel("Net Revenue ($)")
    plt.xticks(rotation=25)
    save_chart(fig, "revenue_by_category.png")


def plot_monthly_revenue(df: pd.DataFrame):
    """Line chart example (works if you have 'order_month' + 'net_revenue')."""
    if not {"order_month", "net_revenue"}.issubset(df.columns):
        print("Skipping 'monthly revenue' (required columns not found).")
        return
    monthly = (
        df.groupby("order_month", as_index=False)["net_revenue"]
        .sum()
        .sort_values("order_month")
    )

    fig = plt.figure(figsize=(9, 5))
    plt.plot(monthly["order_month"], monthly["net_revenue"], marker="o")
    plt.title("Monthly Net Revenue")
    plt.xlabel("Month (YYYY-MM)")
    plt.ylabel("Net Revenue ($)")
    plt.xticks(rotation=45, ha="right")
    save_chart(fig, "monthly_net_revenue.png")


def plot_quantity_hist(df: pd.DataFrame):
    """Histogram example (works if you have 'quantity')."""
    if "quantity" not in df.columns:
        print("Skipping 'quantity distribution' (column not found).")
        return
    fig = plt.figure(figsize=(7, 5))
    plt.hist(df["quantity"], bins=5)
    plt.title("Quantity per Order (Distribution)")
    plt.xlabel("Quantity")
    plt.ylabel("Count")
    save_chart(fig, "quantity_distribution.png")

def plot_unit_price_boxplot(df: pd.DataFrame):
    """Boxplot of unit_price by category (shows median/spread/outliers)."""
    if not {"category", "unit_price"}.issubset(df.columns):
        print("Skipping 'unit price boxplot' (required columns not found).")
        return
    fig = plt.figure(figsize=(9, 5))
    ax = plt.gca()
    df.boxplot(column="unit_price", by="category", grid=False, ax=ax)
    plt.title("Unit Price by Category (Boxplot)")
    plt.suptitle("")  # remove pandas' default super title
    plt.xlabel("Category")
    plt.ylabel("Unit Price ($)")
    save_chart(fig, "unit_price_boxplot.png")



# ------------------ MAIN ------------------
def main():
    # 1) Load/create data
    df = load_data()

    # 2) Quick peek in console (optional)
    print("DataFrame shape:", df.shape)
    print(df.head())

    # 3) TODO[4]: Put YOUR question here (and also in README)
    #    e.g., "Which categories generate the most revenue?"

    # 4) Make charts (add/remove as your question changes)
    plot_revenue_by_category(df)
    plot_monthly_revenue(df)
    plot_quantity_hist(df)
    plot_unit_price_boxplot(df)

    import os
    os.makedirs("charts", exist_ok=True)  # safe if already exists
    df.to_csv("orders.csv", index=False)
    print("Saved orders.csv for inspection")

    print(f"Charts saved to ./{CHART_DIR}")


if __name__ == "__main__":
    main()
