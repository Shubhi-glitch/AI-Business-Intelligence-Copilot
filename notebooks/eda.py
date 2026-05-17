import pandas as pd

# Load dataset
df = pd.read_csv("data/superstore.csv", encoding='latin1')

# ==============================
# BASIC INFORMATION
# ==============================

print("\nDATASET SHAPE")
print(df.shape)

print("\nCOLUMN NAMES")
print(df.columns)

# ==============================
# MISSING VALUES
# ==============================

print("\nMISSING VALUES")
print(df.isnull().sum())

# ==============================
# DUPLICATES
# ==============================

duplicates = df.duplicated().sum()

print("\nDUPLICATE ROWS")
print(duplicates)

# ==============================
# DATE CONVERSION
# ==============================

df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

print("\nDATE CONVERSION SUCCESSFUL")

# ==============================
# BUSINESS KPIs
# ==============================

total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_orders = df['Order ID'].nunique()
total_customers = df['Customer ID'].nunique()

print("\nBUSINESS KPIs")

print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Total Orders: {total_orders}")
print(f"Total Customers: {total_customers}")

# ==============================
# TOP CATEGORIES
# ==============================

print("\nTOP CATEGORIES BY SALES")

category_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)

print(category_sales)

# ==============================
# TOP REGIONS
# ==============================

print("\nREGION-WISE PROFIT")

region_profit = df.groupby('Region')['Profit'].sum().sort_values(ascending=False)

print(region_profit)