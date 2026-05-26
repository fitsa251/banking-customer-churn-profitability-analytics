import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --------------------------------------------------
# Page Setup
# --------------------------------------------------
st.set_page_config(
    page_title="Banking Churn & Profitability Analytics",
    page_icon="🏦",
    layout="wide"
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------
st.markdown(
    """
    <style>
    .main {
        background-color: #f7f9fc;
    }

    .hero-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 55%, #2563eb 100%);
        padding: 2rem;
        border-radius: 22px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0px 8px 24px rgba(15, 23, 42, 0.18);
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
    }

    .hero-subtitle {
        font-size: 1rem;
        line-height: 1.6;
        max-width: 1000px;
        color: #e5e7eb;
    }

    .kpi-card {
        background-color: white;
        padding: 1.2rem;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        box-shadow: 0px 4px 14px rgba(15, 23, 42, 0.06);
        min-height: 125px;
    }

    .kpi-label {
        color: #64748b;
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 0.5rem;
    }

    .kpi-value {
        color: #0f172a;
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .kpi-note {
        color: #64748b;
        font-size: 0.8rem;
    }

    .section-card {
        background-color: white;
        padding: 1.4rem;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        box-shadow: 0px 4px 14px rgba(15, 23, 42, 0.05);
        margin-bottom: 1rem;
    }

    .insight-card {
        background-color: #ffffff;
        padding: 1rem;
        border-left: 5px solid #2563eb;
        border-radius: 14px;
        border-top: 1px solid #e5e7eb;
        border-right: 1px solid #e5e7eb;
        border-bottom: 1px solid #e5e7eb;
        margin-bottom: 0.8rem;
        box-shadow: 0px 3px 10px rgba(15, 23, 42, 0.04);
    }

    .insight-title {
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.25rem;
    }

    .insight-body {
        color: #475569;
        font-size: 0.92rem;
        line-height: 1.5;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        padding: 1rem;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        box-shadow: 0px 4px 14px rgba(15, 23, 42, 0.05);
    }

    .footer-note {
        color: #64748b;
        font-size: 0.85rem;
        margin-top: 2rem;
        padding: 1rem;
        background-color: #ffffff;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Helper Functions
# --------------------------------------------------
def money(value):
    return f"${value:,.0f}"

def percent(value):
    if pd.isna(value):
        return "0.00%"
    return f"{value:.2%}"

def number(value):
    return f"{value:,.0f}"

def kpi_card(label, value, note):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# Load Data
# --------------------------------------------------
@st.cache_data
def load_data():
    data_path = Path("data/banking_churn_profitability_data.csv")
    df = pd.read_csv(data_path)

    df["digital_engagement_band"] = pd.cut(
        df["digital_logins_90d"],
        bins=[-1, 5, 15, 30, 100],
        labels=["Very Low", "Low", "Medium", "High"]
    )

    df["support_call_band"] = pd.cut(
        df["support_calls_90d"],
        bins=[-1, 0, 2, 5, 100],
        labels=["0 Calls", "1-2 Calls", "3-5 Calls", "6+ Calls"]
    )

    return df

df = load_data()

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
st.sidebar.markdown("## 🧭 Dashboard Filters")
st.sidebar.caption("Use these filters to explore customer profitability, churn risk, and retention opportunities.")

segment_order = sorted(df["customer_segment"].unique())
risk_order = ["Low Risk", "Medium Risk", "High Risk"]
income_order = ["Under 40K", "40K-75K", "75K-125K", "125K-200K", "200K+"]
state_order = sorted(df["state"].unique())

selected_segment = st.sidebar.multiselect(
    "Customer Segment",
    options=segment_order,
    default=segment_order
)

selected_risk = st.sidebar.multiselect(
    "Churn Risk Band",
    options=risk_order,
    default=risk_order
)

selected_income = st.sidebar.multiselect(
    "Income Band",
    options=income_order,
    default=income_order
)

selected_state = st.sidebar.multiselect(
    "State",
    options=state_order,
    default=state_order
)

filtered_df = df[
    (df["customer_segment"].isin(selected_segment)) &
    (df["churn_risk_band"].isin(selected_risk)) &
    (df["income_band"].isin(selected_income)) &
    (df["state"].isin(selected_state))
]

if filtered_df.empty:
    st.warning("No data matches the selected filters. Please adjust the sidebar filters.")
    st.stop()

# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">🏦 Banking Customer Churn & Profitability Analytics</div>
        <div class="hero-subtitle">
            Interactive analytics dashboard for exploring customer profitability, churn risk, product usage,
            digital engagement, support activity, and retention opportunities using a synthetic banking dataset.
            Built with Python, Streamlit, Plotly, and Pandas.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------
total_customers = len(filtered_df)
total_balance = filtered_df["total_balance"].sum()
total_revenue = filtered_df["monthly_revenue"].sum()
total_profit = filtered_df["monthly_profit"].sum()
churn_rate = filtered_df["churned"].mean()
high_risk_customers = (filtered_df["churn_risk_band"] == "High Risk").sum()
avg_products = filtered_df["product_count"].mean()
avg_profit = filtered_df["monthly_profit"].mean()

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    kpi_card("Total Customers", number(total_customers), "Filtered customer base")

with kpi2:
    kpi_card("Total Balance", money(total_balance), "Total deposits held")

with kpi3:
    kpi_card("Monthly Profit", money(total_profit), "Estimated net monthly profit")

with kpi4:
    kpi_card("Churn Rate", percent(churn_rate), "Observed churn rate")

with kpi5:
    kpi_card("High Risk Customers", number(high_risk_customers), "Customers needing attention")

st.markdown("")

# --------------------------------------------------
# Tabs
# --------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Executive Overview",
    "⚠️ Churn Risk",
    "💰 Profitability",
    "🎯 Retention Opportunities",
    "📄 Data Explorer"
])

# --------------------------------------------------
# Tab 1: Executive Overview
# --------------------------------------------------
with tab1:
    st.markdown("### 📊 Executive Overview")

    segment_summary = (
        filtered_df.groupby("customer_segment")
        .agg(
            customers=("customer_id", "count"),
            total_balance=("total_balance", "sum"),
            total_revenue=("monthly_revenue", "sum"),
            total_profit=("monthly_profit", "sum"),
            avg_products=("product_count", "mean"),
            churn_rate=("churned", "mean")
        )
        .reset_index()
        .sort_values("total_profit", ascending=False)
    )

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            segment_summary,
            x="customer_segment",
            y="total_profit",
            text_auto=".2s",
            title="Monthly Profit by Customer Segment",
            color="customer_segment"
        )
        fig.update_layout(
            template="plotly_white",
            xaxis_title="Customer Segment",
            yaxis_title="Monthly Profit",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.pie(
            segment_summary,
            names="customer_segment",
            values="total_balance",
            hole=0.55,
            title="Balance Distribution by Customer Segment"
        )
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        fig = px.bar(
            segment_summary,
            x="customer_segment",
            y="churn_rate",
            text_auto=".2%",
            title="Churn Rate by Customer Segment",
            color="customer_segment"
        )
        fig.update_layout(
            template="plotly_white",
            xaxis_title="Customer Segment",
            yaxis_title="Churn Rate",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        fig = px.bar(
            segment_summary,
            x="customer_segment",
            y="avg_products",
            text_auto=".2f",
            title="Average Product Count by Segment",
            color="customer_segment"
        )
        fig.update_layout(
            template="plotly_white",
            xaxis_title="Customer Segment",
            yaxis_title="Average Products",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Segment Summary Table")
    st.dataframe(segment_summary, use_container_width=True)

# --------------------------------------------------
# Tab 2: Churn Risk
# --------------------------------------------------
with tab2:
    st.markdown("### ⚠️ Churn Risk Analysis")

    risk_summary = (
        filtered_df.groupby("churn_risk_band")
        .agg(
            customers=("customer_id", "count"),
            avg_balance=("total_balance", "mean"),
            avg_profit=("monthly_profit", "mean"),
            avg_products=("product_count", "mean"),
            avg_support_calls=("support_calls_90d", "mean"),
            avg_digital_logins=("digital_logins_90d", "mean"),
            churn_rate=("churned", "mean")
        )
        .reset_index()
    )

    risk_summary["churn_risk_band"] = pd.Categorical(
        risk_summary["churn_risk_band"],
        categories=risk_order,
        ordered=True
    )
    risk_summary = risk_summary.sort_values("churn_risk_band")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            risk_summary,
            x="churn_risk_band",
            y="churn_rate",
            text_auto=".2%",
            title="Churn Rate by Risk Band",
            color="churn_risk_band"
        )
        fig.update_layout(
            template="plotly_white",
            xaxis_title="Churn Risk Band",
            yaxis_title="Churn Rate",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            risk_summary,
            x="churn_risk_band",
            y="customers",
            text_auto=True,
            title="Customer Count by Churn Risk Band",
            color="churn_risk_band"
        )
        fig.update_layout(
            template="plotly_white",
            xaxis_title="Churn Risk Band",
            yaxis_title="Customers",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    product_summary = (
        filtered_df.groupby("product_count")
        .agg(
            customers=("customer_id", "count"),
            churn_rate=("churned", "mean"),
            avg_profit=("monthly_profit", "mean")
        )
        .reset_index()
    )

    fig = px.line(
        product_summary,
        x="product_count",
        y="churn_rate",
        markers=True,
        title="Churn Rate by Product Count"
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Product Count",
        yaxis_title="Churn Rate"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Risk Summary Table")
    st.dataframe(risk_summary, use_container_width=True)

# --------------------------------------------------
# Tab 3: Profitability
# --------------------------------------------------
with tab3:
    st.markdown("### 💰 Profitability Analysis")

    income_summary = (
        filtered_df.groupby("income_band")
        .agg(
            customers=("customer_id", "count"),
            total_balance=("total_balance", "sum"),
            total_revenue=("monthly_revenue", "sum"),
            total_profit=("monthly_profit", "sum"),
            avg_products=("product_count", "mean"),
            churn_rate=("churned", "mean")
        )
        .reset_index()
    )

    income_summary["income_band"] = pd.Categorical(
        income_summary["income_band"],
        categories=income_order,
        ordered=True
    )
    income_summary = income_summary.sort_values("income_band")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            income_summary,
            x="income_band",
            y="total_profit",
            text_auto=".2s",
            title="Monthly Profit by Income Band",
            color="income_band"
        )
        fig.update_layout(
            template="plotly_white",
            xaxis_title="Income Band",
            yaxis_title="Monthly Profit",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.scatter(
            filtered_df,
            x="total_balance",
            y="monthly_profit",
            color="customer_segment",
            size="product_count",
            hover_data=["customer_id", "churn_risk_band", "income_band"],
            title="Customer Balance vs Monthly Profit"
        )
        fig.update_layout(
            template="plotly_white",
            xaxis_title="Total Balance",
            yaxis_title="Monthly Profit"
        )
        st.plotly_chart(fig, use_container_width=True)

    negative_profit = filtered_df[filtered_df["monthly_profit"] < 0].sort_values("monthly_profit")

    st.markdown("### Negative-Profit Customer Review")
    st.dataframe(
        negative_profit[
            [
                "customer_id", "state", "customer_segment", "income_band",
                "total_balance", "product_count", "monthly_revenue",
                "servicing_cost", "monthly_profit", "support_calls_90d",
                "churn_risk_band"
            ]
        ].head(50),
        use_container_width=True
    )

# --------------------------------------------------
# Tab 4: Retention Opportunities
# --------------------------------------------------
with tab4:
    st.markdown("### 🎯 Retention Opportunities")

    high_value_at_risk = filtered_df[
        (filtered_df["churn_risk_band"] == "High Risk") &
        (
            (filtered_df["monthly_profit"] > filtered_df["monthly_profit"].median()) |
            (filtered_df["total_balance"] > filtered_df["total_balance"].median())
        )
    ].sort_values(["monthly_profit", "total_balance"], ascending=False)

    cross_sell_opportunities = filtered_df[
        (filtered_df["churn_risk_band"].isin(["Low Risk", "Medium Risk"])) &
        (filtered_df["product_count"].between(2, 4)) &
        (filtered_df["total_balance"] > filtered_df["total_balance"].mean())
    ].sort_values(["total_balance", "monthly_profit"], ascending=False)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("High-Value At-Risk Customers", number(len(high_value_at_risk)))

    with col2:
        st.metric("Cross-Sell Opportunities", number(len(cross_sell_opportunities)))

    with col3:
        st.metric("Average Products per Customer", f"{avg_products:.2f}")

    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-title">Retention Strategy</div>
            <div class="insight-body">
                Customers with strong balances or monthly profit but high churn risk should be prioritized for proactive outreach.
                Customers with fewer products and healthy balances may be good candidates for cross-sell campaigns.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### High-Value At-Risk Customers")
    st.dataframe(
        high_value_at_risk[
            [
                "customer_id", "state", "customer_segment", "income_band",
                "total_balance", "product_count", "monthly_profit",
                "support_calls_90d", "digital_logins_90d",
                "churn_probability", "churn_risk_band"
            ]
        ].head(50),
        use_container_width=True
    )

    st.markdown("### Cross-Sell Opportunity Customers")
    st.dataframe(
        cross_sell_opportunities[
            [
                "customer_id", "state", "customer_segment", "income_band",
                "credit_score_band", "total_balance", "product_count",
                "has_credit_card", "has_personal_loan", "has_investment_account",
                "monthly_profit", "churn_probability", "churn_risk_band"
            ]
        ].head(50),
        use_container_width=True
    )

# --------------------------------------------------
# Tab 5: Data Explorer
# --------------------------------------------------
with tab5:
    st.markdown("### 📄 Data Explorer")

    st.markdown(
        """
        Use this table to inspect the filtered customer-level banking dataset.
        """
    )

    selected_columns = st.multiselect(
        "Choose columns to display",
        options=list(filtered_df.columns),
        default=[
            "customer_id", "state", "customer_segment", "income_band",
            "total_balance", "product_count", "monthly_profit",
            "churn_probability", "churn_risk_band", "churned"
        ]
    )

    st.dataframe(
        filtered_df[selected_columns].head(500),
        use_container_width=True
    )

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_banking_churn_data.csv",
        mime="text/csv"
    )

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown(
    """
    <div class="footer-note">
        <strong>Dataset Note:</strong> This dashboard uses synthetic data created for portfolio and learning purposes.
        No real customer, bank, employer, or private financial data is used.
    </div>
    """,
    unsafe_allow_html=True
)