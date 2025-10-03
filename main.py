import streamlit as st
import random
from utils import load_data
import pandas as pd

# Data file
DATA_FILE = "data.json"

st.set_page_config(page_title="Personal Expense Tracker", page_icon="💸", layout="wide")

def main():
    st.title("💸 Personal Expense Tracker Dashboard")
    st.markdown("### Track Your Expenses, Save Money, and Reach Your Goals! 🚀")

    # Motivational Quotes
    quotes = [
        "Do not save what is left after spending, but spend what is left after saving. – Warren Buffett",
        "A penny saved is a penny earned. – Benjamin Franklin",
        "Beware of little expenses. A small leak will sink a great ship. – Benjamin Franklin",
        "Don’t tell me what you value, show me your budget, and I’ll tell you what you value. – Joe Biden",
        "It’s not about having a lot of money, it’s about knowing how to manage it. – Anonymous",
        "If you buy things you do not need, soon you will have to sell things you need. – Warren Buffett",
    ]
    quote = random.choice(quotes)
    st.info(f"💡 **Motivation of the Day:** *{quote}*")

    # Load data
    data = load_data(DATA_FILE)
    expenses = data.get("expenses", [])
    monthly_budget = data.get("monthly_budget", 0.0)

    if expenses:
        df = pd.DataFrame(expenses)
        total_expenses = df["amount"].sum()
        savings = monthly_budget - total_expenses if monthly_budget > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Expenses", f"₹{total_expenses:,.2f}")
        col2.metric("Monthly Budget", f"₹{monthly_budget:,.2f}")
        col3.metric("Savings Left", f"₹{savings:,.2f}")

        if savings > 0:
            st.success(f"🎉 Great job! You're saving ₹{savings:,.2f} this month.")
        else:
            st.warning("⚠️ You're over budget. Time to cut back! 💪")
    else:
        st.warning("⚠️ No expenses recorded yet. Add some in the 'Add Details' page!")
        if monthly_budget == 0:
            st.info("💡 Set your monthly budget in the 'Savings System' page for better tracking.")

    st.markdown("---")
    st.caption("📊 Navigate using the sidebar to explore other pages.")

if __name__ == "__main__":
    main()


