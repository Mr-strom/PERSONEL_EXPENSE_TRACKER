import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_data

# Data file
DATA_FILE = "../data.json"

st.title("📊 Monthly Charts & Insights")
st.markdown("### Visualize your spending patterns! 🎨")

# Load data
data = load_data(DATA_FILE)
expenses = data.get("expenses", [])

if expenses:
    df = pd.DataFrame(expenses)
    df['date'] = pd.to_datetime(df['date'])
    df['day'] = df['date'].dt.day  # For daily bar chart

    # Pie Chart: Category-wise
    st.subheader("🥧 Category-wise Spending")
    category_sums = df.groupby("category")["amount"].sum()
    if not category_sums.empty:
        fig1, ax1 = plt.subplots()
        ax1.pie(category_sums.values, labels=category_sums.index, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        ax1.set_title("Expense Distribution by Category")
        st.pyplot(fig1)
    else:
        st.warning("No data for pie chart.")

    # Bar Chart: Daily Expenses
    st.subheader("📈 Daily Expenses Trend")
    daily_sums = df.groupby("day")["amount"].sum()
    if not daily_sums.empty:
        fig2, ax2 = plt.subplots()
        daily_sums.plot(kind='bar', ax=ax2, color='skyblue')
        ax2.set_xlabel("Day of Month")
        ax2.set_ylabel("Amount (₹)")
        ax2.set_title("Daily Spending")
        plt.xticks(rotation=45)
        st.pyplot(fig2)
    else:
        st.warning("No data for bar chart.")

    # Quick Insight
    avg_spend = df["amount"].mean()
    st.info(f"💡 Average spend per expense: ₹{avg_spend:.2f}")
else:
    st.warning("⚠️ No expense data available. Add expenses first!")
