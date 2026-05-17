import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/superstore.csv", encoding='latin1')

# ==============================
# SALES BY CATEGORY
# ==============================

category_sales = df.groupby('Category')['Sales'].sum()

plt.figure(figsize=(8,5))

plt.bar(category_sales.index, category_sales.values)

plt.title("Sales by Category")

plt.xlabel("Category")

plt.ylabel("Sales")

plt.tight_layout()

plt.show()

# ==============================
# PROFIT BY REGION
# ==============================

region_profit = df.groupby('Region')['Profit'].sum()

plt.figure(figsize=(8,5))

plt.bar(region_profit.index, region_profit.values)

plt.title("Profit by Region")

plt.xlabel("Region")

plt.ylabel("Profit")

plt.tight_layout()

plt.show()

# ==============================
# TOP 10 SUB-CATEGORIES
# ==============================

sub_category_sales = (
    df.groupby('Sub-Category')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12,6))

plt.bar(sub_category_sales.index, sub_category_sales.values)

plt.title("Top 10 Sub-Categories by Sales")

plt.xlabel("Sub-Category")

plt.ylabel("Sales")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()
# ==============================
# MONTHLY SALES TREND
# ==============================

# Convert order date
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Create month-year column
df['Month-Year'] = df['Order Date'].dt.to_period('M')

# Monthly sales
monthly_sales = df.groupby('Month-Year')['Sales'].sum()

# Convert index to string
monthly_sales.index = monthly_sales.index.astype(str)

# Plot
plt.figure(figsize=(14,6))

plt.plot(monthly_sales.index, monthly_sales.values)

plt.title("Monthly Sales Trend")

plt.xlabel("Month-Year")

plt.ylabel("Sales")

plt.xticks(rotation=90)

plt.tight_layout()

plt.show()