from sklearn.linear_model import LinearRegression
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="AI Business Intelligence Copilot",
    layout="wide"
)

# =========================================
# LOAD CSS
# =========================================

with open("frontend/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# =========================================
# TITLE
# =========================================

st.title("AI Business Intelligence Copilot")

st.markdown(
    "Interactive Sales & Profit Analytics Dashboard"
)

# =========================================
# LOAD DATA
# =========================================

df = pd.read_csv(
    "data/superstore.csv",
    encoding="latin1"
)

# =========================================
# DATE CONVERSION
# =========================================

df["Order Date"] = pd.to_datetime(
    df["Order Date"]
)

# =========================================
# SIDEBAR FILTERS
# =========================================

st.sidebar.markdown(
    "<div class='sidebar-title'>📊 Filter Dashboard</div>",
    unsafe_allow_html=True
)

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# =========================================
# FILTER DATA
# =========================================

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category))
]

# =========================================
# KPI CALCULATIONS
# =========================================

total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

total_orders = filtered_df["Order ID"].nunique()

total_customers = filtered_df["Customer ID"].nunique()

# =========================================
# KPI CARDS
# =========================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Sales",
    f"${total_sales:,.0f}"
)

col2.metric(
    "📈 Total Profit",
    f"${total_profit:,.0f}"
)

col3.metric(
    "🛒 Orders",
    total_orders
)

col4.metric(
    "👥 Customers",
    total_customers
)

# =========================================
# SALES BY CATEGORY
# =========================================

category_sales = (
    filtered_df.groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    title="Sales by Category",
    text_auto=True,
    color="Category"
)

fig1.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

# =========================================
# PROFIT BY REGION
# =========================================

region_profit = (
    filtered_df.groupby("Region")["Profit"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    region_profit,
    names="Region",
    values="Profit",
    title="Profit by Region",
    hole=0.5
)

fig2.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)"
)

# =========================================
# DISPLAY CHARTS
# =========================================

chart1, chart2 = st.columns(2)

chart1.plotly_chart(
    fig1,
    width="stretch"
)

chart2.plotly_chart(
    fig2,
    width="stretch"
)

# =========================================
# MONTHLY SALES TREND
# =========================================

filtered_df["Month-Year"] = (
    filtered_df["Order Date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_sales = (
    filtered_df.groupby("Month-Year")["Sales"]
    .sum()
    .reset_index()
)

fig3 = px.line(
    monthly_sales,
    x="Month-Year",
    y="Sales",
    title="Monthly Sales Trend",
    markers=True
)

fig3.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(
    fig3,
    width="stretch"
)

# =========================================
# TOP SUB-CATEGORIES
# =========================================

sub_category_sales = (
    filtered_df.groupby("Sub-Category")["Sales"]
    .sum()
    .reset_index()
    .sort_values(
        by="Sales",
        ascending=False
    )
    .head(10)
)

fig4 = px.bar(
    sub_category_sales,
    x="Sub-Category",
    y="Sales",
    title="Top 10 Sub-Categories",
    text_auto=True,
    color="Sub-Category"
)

fig4.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(
    fig4,
    width="stretch"
)

# =========================================
# DATA PREVIEW
# =========================================

st.subheader("📄 Dataset Preview")

st.dataframe(
    filtered_df.head(20),
    width="stretch"
)

# =========================================
# BUSINESS INSIGHTS
# =========================================

st.markdown("## 📌 Business Insights")

# Top Category

top_category_row = category_sales.loc[
    category_sales["Sales"].idxmax()
]

top_category = top_category_row["Category"]

top_category_sales = top_category_row["Sales"]

# Top Region

top_region_row = region_profit.loc[
    region_profit["Profit"].idxmax()
]

top_region = top_region_row["Region"]

top_region_profit = top_region_row["Profit"]

# Highest Month

top_month_row = monthly_sales.loc[
    monthly_sales["Sales"].idxmax()
]

highest_month = top_month_row["Month-Year"]

highest_month_sales = top_month_row["Sales"]

# Insights Cards

st.success(
    f"📈 Highest sales category is "
    f"{top_category} with sales of "
    f"${top_category_sales:,.0f}"
)

st.info(
    f"🌍 Most profitable region is "
    f"{top_region} with profit of "
    f"${top_region_profit:,.0f}"
)

st.warning(
    f"🚀 Highest monthly sales were recorded in "
    f"{highest_month} with sales of "
    f"${highest_month_sales:,.0f}"
)

# =========================================
# DOWNLOAD REPORTS
# =========================================

st.markdown("## 📥 Download Reports")

csv = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="sales_report.csv",
    mime="text/csv"
)
# =========================================
# SALES FORECASTING
# =========================================

st.markdown("## 🔮 Sales Forecasting")

# Monthly Sales for Forecast

forecast_df = (
    filtered_df.groupby("Month-Year")["Sales"]
    .sum()
    .reset_index()
)

# Create Index

forecast_df["Month_Index"] = np.arange(
    len(forecast_df)
)

# Features and Target

X = forecast_df[["Month_Index"]]

y = forecast_df["Sales"]

# Train Model

model = LinearRegression()

model.fit(X, y)

# Future Prediction

future_index = np.arange(
    len(forecast_df),
    len(forecast_df) + 6
).reshape(-1, 1)

future_sales = model.predict(
    future_index
)

# Future Months

future_months = [
    f"Future {i}"
    for i in range(1, 7)
]

forecast_future = pd.DataFrame({
    "Month": future_months,
    "Forecast Sales": future_sales
})

# Forecast Chart

fig_forecast = px.line(
    forecast_future,
    x="Month",
    y="Forecast Sales",
    title="Next 6 Months Sales Forecast",
    markers=True
)

fig_forecast.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(
    fig_forecast,
    width="stretch"
)
# =========================================
# CHAT WITH YOUR DATA
# =========================================

st.markdown("## 🤖 Chat With Your Data")

user_question = st.text_input(
    "Ask a business question",
    key="chat_input"
)

if user_question:

    question = user_question.lower()

    # TOTAL SALES

    if "total sales" in question:

        st.success(
            f"💰 Total Sales are ${total_sales:,.0f}"
        )

    # TOTAL PROFIT

    elif "total profit" in question:

        st.success(
            f"📈 Total Profit is ${total_profit:,.0f}"
        )

    # TOP CATEGORY

    elif "top category" in question:

        st.success(
            f"🏆 Top category is {top_category}"
        )

    # TOP REGION

    elif "top region" in question:

        st.success(
            f"🌍 Most profitable region is {top_region}"
        )

    # HIGHEST MONTH

    elif "highest month" in question:

        st.success(
            f"🚀 Highest sales month was "
            f"{highest_month}"
        )

    # TOTAL CUSTOMERS

    elif "total customers" in question:

        st.success(
            f"👥 Total customers are "
            f"{total_customers}"
        )

    # TOTAL ORDERS

    elif "total orders" in question:

        st.success(
            f"🛒 Total orders are "
            f"{total_orders}"
        )

    # UNKNOWN QUESTION

    else:

        st.error(
            "❌ Sorry, I can answer only dashboard business questions right now."
        )