import streamlit as st
import pandas as pd
from utils import load_data
import io

# Data file
DATA_FILE = "../data.json"

st.title("📜 Expense History")
st.markdown("### View and manage your past expenses. 🔍")

# Load data
data = load_data(DATA_FILE)
expenses = data.get("expenses", [])

if expenses:
    df = pd.DataFrame(expenses)
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')  # Format dates

    # Filter by category
    st.subheader("🔧 Filters")
    categories = ["All"] + sorted(df["category"].unique().tolist())
    selected_category = st.selectbox("Filter by Category", categories)

    if selected_category != "All":
        df = df[df["category"] == selected_category]

    # Display table
    st.subheader("📋 Expenses Table")
    st.dataframe(df, use_container_width=True)

    # Summary
    total_filtered = df["amount"].sum()
    st.metric("Total Filtered Expenses", f"₹{total_filtered:,.2f}")

    # Download CSV
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue().encode("utf-8")
    st.download_button(
        label="📥 Download as CSV",
        data=csv_data,
        file_name="expenses_history.csv",
        mime="text/csv"
    )
else:
    st.warning("⚠️ No expenses recorded yet. Add some in 'Add Details'!")
