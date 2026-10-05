import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Customer 360 Dashboard", layout="wide")

# Data load karo
customer_360 = pd.read_csv('customer_360.csv')
monthly_revenue = pd.read_csv('monthly_revenue.csv')
product_performance = pd.read_csv('product_performance.csv')
category_performance = pd.read_csv('category_performance.csv')
store_performance = pd.read_csv('store_performance.csv')
campaign_performance = pd.read_csv('campaign_performance.csv')

# Title
st.title("📊 Enterprise Customer 360 Analytics Dashboard")

# ===== KPI Cards =====
col1, col2, col3, col4 = st.columns(4)

total_customers = customer_360['customer_id'].nunique()
total_revenue = customer_360['total_spend'].sum()
churn_rate = (customer_360['Churn_Flag'] == 'Churned').mean() * 100
avg_clv = customer_360['CLV'].mean()

col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Total Revenue", f"${total_revenue:,.0f}")
col3.metric("Churn Rate", f"{churn_rate:.1f}%")
col4.metric("Avg CLV", f"${avg_clv:,.2f}")

st.markdown("---")

# ===== Revenue Trend =====
st.subheader("📈 Monthly Revenue Trend")
fig_revenue = px.line(monthly_revenue, x='month', y='total_amount', markers=True)
st.plotly_chart(fig_revenue, use_container_width=True)

# ===== Two columns: Segment Pie + Category Bar =====
col_left, col_right = st.columns(2)

with col_left:
	st.subheader("🎯 Customer Segments")
	segment_counts = customer_360['Customer_Segment'].value_counts().reset_index()
	segment_counts.columns = ['Segment', 'Count']
	fig_segment = px.pie(segment_counts, names='Segment', values='Count', hole=0.4)
	st.plotly_chart(fig_segment, use_container_width=True)

with col_right:
	st.subheader("🛒 Category Performance")
	fig_category = px.bar(category_performance, x='product_category', y='total_revenue')
	st.plotly_chart(fig_category, use_container_width=True)

# ===== Top Products =====
st.subheader("🏆 Top 10 Products by Revenue")
top_products = product_performance.sort_values('total_revenue', ascending=False).head(10)
fig_products = px.bar(top_products, x='product_name', y='total_revenue')
st.plotly_chart(fig_products, use_container_width=True)

# ===== Store Performance Table =====
st.subheader("🏬 Store Performance")
st.dataframe(store_performance.sort_values('total_revenue', ascending=False))

# ===== Campaign Performance =====
st.subheader("📧 Marketing Campaign Performance")
st.dataframe(campaign_performance)

# ===== Customer Table (searchable) =====
st.subheader("👥 Customer Details")
st.dataframe(customer_360[['customer_id', 'total_spend', 'total_transactions', 'CLV', 'Customer_Segment', 'Churn_Flag']])
