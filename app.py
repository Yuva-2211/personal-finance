import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import sqlite3

#DATABASE SETUP
conn = sqlite3.connect('user_data.db')
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT,
    password TEXT,
    salary REAL
)
""")

#Expense table
c.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    username TEXT,
    date TEXT,
    food REAL,
    fuel REAL,
    groceries REAL,
    other REAL,
    savings REAL
)
""")
conn.commit()
conn.close()

#USER MANAGEMENT FUNCTIONS
def create_user():
    st.subheader("Create Account")
    username = st.text_input("New Username", key="create_user")
    password = st.text_input("New Password", type="password", key="create_pass")
    salary = st.number_input("Monthly Salary (₹)", min_value=0.0, step=100.0)

    if st.button("Create"):
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, password, salary))
        conn.commit()
        conn.close()
        st.success("Account created successfully!")

def login_user():
    st.subheader("Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user_data = c.fetchone()
        conn.close()

        if user_data:
            st.session_state.username = username
            st.session_state.salary = user_data[2]
            st.success("Logged in successfully!")
            return True
        else:
            st.error("Invalid username or password")
            return False

def logout_user():
    st.session_state.username = None
    st.session_state.salary = None
    st.success("Logged out successfully!")

#MAIN APP 
def main_app():
    st.header("Personal Finance Tracker")
    st.subheader("Log Your Daily Expenses")

    date = st.date_input("Date")
    food = st.number_input("Food (₹)", min_value=0)
    fuel = st.number_input("Fuel (₹)", min_value=0)
    groceries = st.number_input("Groceries (₹)", min_value=0)
    other = st.number_input("Other (₹)", min_value=0)
    savings = st.number_input("Savings (₹)", min_value=0)

    if st.button("Add Expense"):
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute("""
            INSERT INTO expenses (username, date, food, fuel, groceries, other, savings)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            st.session_state.username, str(date), food, fuel, groceries, other, savings
        ))
        conn.commit()
        conn.close()
        st.success("Expense added!")

#LOAD USER'S EXPENSES
    conn = sqlite3.connect('user_data.db')
    df = pd.read_sql_query(
        "SELECT * FROM expenses WHERE username = ?",
        conn,
        params=(st.session_state.username,)
    )
    conn.close()

    if not df.empty:
        df['Date'] = pd.to_datetime(df['date'])
        df.drop(columns=['username', 'date'], inplace=True)

        st.write("All Expenses:")
        st.dataframe(df)

# ANALYSIS 
        total_expenses = df[['food', 'fuel', 'groceries', 'other']].sum().sum()
        total_savings = df['savings'].sum()
        expense_ratio = (total_expenses / (total_expenses + total_savings)) * 100 if total_expenses + total_savings > 0 else 0

        st.subheader("Analysis of Your Expenses")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Expenses", f"₹{total_expenses:.2f}")
        col2.metric("Total Savings", f"₹{total_savings:.2f}")
        col3.metric("Expense Ratio", f"{expense_ratio:.2f}%")

        if expense_ratio > 80:
            st.warning("You are spending too much! Try to reduce your expenses.")
        elif expense_ratio < 20:
            st.success("You're doing great! Keep saving and investing.")

#PIE CHART
        st.write("Expense Distribution")
        fig1, ax1 = plt.subplots()
        ax1.pie(
            df[['food', 'fuel', 'groceries', 'other']].sum(),
            labels=['Food', 'Fuel', 'Groceries', 'Other'],
            autopct='%1.1f%%',
            startangle=120
        )
        ax1.axis('equal')
        st.pyplot(fig1)

#BAR CHART
        df['Salary'] = st.session_state.salary
        melted_df = df.melt(
            id_vars=['Date', 'Salary'],
            value_vars=['food', 'fuel', 'groceries', 'other'],
            var_name='Category',
            value_name='Amount'
        )

        st.write("Expense Bar Chart with Salary Hue")
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        sns.barplot(data=melted_df, x='Category', y='Amount', hue='Salary', ax=ax2, palette='magma')
        ax2.set_title("Expenses by Category Colored by Salary")
        ax2.set_ylabel("Amount (₹)")
        ax2.set_xlabel("Expense Category")
        st.pyplot(fig2)

# --- ENTRY POINT ---
def main():
    st.title("Personal Finance Analyser App")

    if 'username' not in st.session_state:
        st.session_state.username = None
        st.session_state.salary = None

    if st.session_state.username is None:
        tab1, tab2 = st.tabs(["Create Account", "Login"])
        with tab1:
            create_user()
        with tab2:
            if login_user():
                main_app()
    else:
        st.write(f"Welcome back, **{st.session_state.username}**!")
        if st.button("Logout"):
            logout_user()
        else:
            main_app()

if __name__ == '__main__':
    main()
