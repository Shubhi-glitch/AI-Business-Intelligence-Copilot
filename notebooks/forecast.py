import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# ==============================
# LOAD DATA
# ==============================

df = pd.read_csv("data/superstore.csv", encoding='latin1')

# ==============================
# DATE CONVERSION
# ==============================

df['Order Date'] = pd.to_datetime(df['Order Date'])

# ==============================
# MONTHLY SALES
# ==============================

monthly_sales = (
    df.groupby(
        df['Order Date'].dt.to_period('M')
    )['Sales']
    .sum()
    .reset_index()
)

monthly_sales['Order Date'] = (
    monthly_sales['Order Date']
    .astype(str)
)

# ==============================
# CREATE TIME INDEX
# ==============================

monthly_sales['Month_Index'] = np.arange(
    len(monthly_sales)
)

# ==============================
# FEATURES & TARGET
# ==============================

X = monthly_sales[['Month_Index']]

y = monthly_sales['Sales']

# ==============================
# TRAIN MODEL
# ==============================

model = LinearRegression()

model.fit(X, y)

# ==============================
# FUTURE PREDICTIONS
# ==============================

future_index = np.arange(
    len(monthly_sales),
    len(monthly_sales) + 12
).reshape(-1, 1)

future_sales = model.predict(future_index)

# ==============================
# PLOT
# ==============================

plt.figure(figsize=(12,6))

# Actual Sales
plt.plot(
    monthly_sales['Month_Index'],
    y,
    label='Actual Sales'
)

# Forecast Sales
plt.plot(
    future_index,
    future_sales,
    label='Forecast Sales'
)

plt.title("Sales Forecast")

plt.xlabel("Month Index")

plt.ylabel("Sales")

plt.legend()

plt.tight_layout()

plt.show()