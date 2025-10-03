import streamlit as st
from datetime import date
from utils import load_data, save_data
import pandas as pd

# Data file
DATA_FILE = "../data.json"

st.title("➕ Add Expense Details")
st.markdown("### Log your daily spends here! 📝")

# Load data
data = load_data(DATA_FILE)
expenses = data.get("expenses", [])

# Form for adding expense
st.subheader("📋 Add New Expense")
col1, col2 = st.columns(2)
with col1:
    expense_date = st.date_input("Date", value=date.today())
with col2:
    category = st.selectbox("Category", ["Food", "Travel", "Personal", "Health", "Others"])

amount = st.number_input("Amount (₹)", min_value=0.0, step=0.01, format="%.2f")
description = st.text_input("Description (optional)")

if st.button("💾 Save Expense"):
    if amount > 0:
        new_expense = {
            "date": expense_date.strftime("%Y-%m-%d"),
            "amount": float(amount),
            "category": category,
            "description": description
        }
        expenses.append(new_expense)
        data["expenses"] = expenses
        if save_data(DATA_FILE, data):
            st.success("✅ Expense added successfully!")
            st.rerun()  # Refresh to clear form
        else:
            st.error("❌ Failed to save. Try again.")
    else:
        st.warning("⚠️ Amount must be greater than 0.")

# Quick preview
if expenses:
    st.subheader("📊 Recent Expenses")
    df_preview = pd.DataFrame(expenses[-5:])  # Last 5
    st.dataframe(df_preview, use_container_width=True)
else:
    st.info("ℹ️ No expenses yet. Add your first one above!")