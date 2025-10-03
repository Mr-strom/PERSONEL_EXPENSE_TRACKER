import streamlit as st
from utils import load_data, save_data
import pandas as pd

# Data file
DATA_FILE = "../data.json"

st.title("🏆 Savings System & Goal Tracker")
st.markdown("### Set goals and track your progress towards financial freedom! 🎯")

# Load data
data = load_data(DATA_FILE)
expenses = data.get("expenses", [])
monthly_budget = data.get("monthly_budget", 0.0)
goals = data.get("goals", [])

# Set Monthly Budget
st.subheader("💰 Set Monthly Budget")
new_budget = st.number_input("Enter your monthly budget (₹)", min_value=0.0, value=monthly_budget, step=100.0, format="%.2f")
if st.button("💾 Update Budget"):
    data["monthly_budget"] = float(new_budget)
    if save_data(DATA_FILE, data):
        st.success("✅ Budget updated!")
        st.rerun()

# Calculate Savings
total_expenses = sum(exp["amount"] for exp in expenses) if expenses else 0.0
savings = monthly_budget - total_expenses if monthly_budget > 0 else 0.0

col1, col2 = st.columns(2)
col1.metric("Total Expenses", f"₹{total_expenses:,.2f}")
col2.metric("Current Savings", f"₹{savings:,.2f}")

if savings < 0:
    st.warning("⚠️ Over budget! Adjust your spending.")
elif savings > 0:
    st.success("🎉 On track to save!")

# Goal Tracker
st.subheader("🎯 Your Goals")
if goals:
    for i, goal in enumerate(goals):
        progress = min((savings / goal["target"]) * 100, 100)
        st.progress(progress)
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**{goal['name']}** - Target: ₹{goal['target']:,.2f}")
        with col2:
            st.write(f"Progress: ₹{min(savings, goal['target']):,.2f} / ₹{goal['target']:,.2f}")
        
        if st.button(f"🗑️ Delete Goal: {goal['name']}", key=f"del_{i}"):
            goals.pop(i)
            data["goals"] = goals
            save_data(DATA_FILE, data)
            st.rerun()
else:
    st.info("ℹ️ No goals set yet. Add one below!")

# Add New Goal
with st.expander("➕ Add New Goal"):
    goal_name = st.text_input("Goal Name (e.g., New Phone)")
    goal_target = st.number_input("Target Amount (₹)", min_value=0.0, step=100.0, format="%.2f")
    if st.button("💾 Add Goal") and goal_name and goal_target > 0:
        new_goal = {"name": goal_name, "target": float(goal_target)}
        goals.append(new_goal)
        data["goals"] = goals
        if save_data(DATA_FILE, data):
            st.success(f"✅ Goal '{goal_name}' added!")
            st.rerun()

if not monthly_budget:
    st.warning("⚠️ Set your monthly budget above to track savings accurately!")