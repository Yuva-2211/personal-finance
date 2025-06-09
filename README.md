
# 💰 Personal Finance Analyser App

A lightweight, user-friendly personal finance tracker built using **Streamlit** and **SQLite**. This app helps users securely log expenses, track savings, and visualize their financial habits with intuitive charts and personalized insights.

---

## 🚀 Features

### 🔐 User Authentication
- Secure login and registration system.
- User data stored locally using **SQLite**.

### 📝 Daily Expense Logging
- Log daily expenses under predefined categories:
  - Food
  - Fuel
  - Groceries
  - Other
  - Savings

### 📊 Insightful Analysis
- **Total expense** and **total savings** overview.
- **Expense-to-savings ratio** for better financial awareness.
- Tailored **spending advice** based on your data.

### 📈 Visualizations
- **Pie Chart** showing expense distribution by category.
- **Bar Chart** comparing income and expenses.

---

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Yuva-2211/personal-finance.git
cd personal-finance
````

### 2. Install Required Packages

```bash
pip install streamlit pandas matplotlib seaborn
```

### 3. Run the App

```bash
streamlit run app.py
```

---

## 📁 File Structure

```
personal-finance/
├── app.py              # Main Streamlit application
├── user_data.db        # SQLite database (auto-created upon first run)
├── README.md           # Project documentation
```

---

## 🧰 Technologies Used

* **Streamlit** – For building the interactive web interface
* **SQLite3** – Lightweight relational database for storing user data
* **Pandas** – For handling and analyzing tabular data
* **Matplotlib & Seaborn** – For generating visual insights

---

## 🔄 Sample Flow

1. Register with your **name**, **password**, and **monthly salary**.
2. Log daily expenses under specific categories.
3. Get visual feedback via charts and metrics.
4. Receive personalized financial advice based on your spending and savings behavior.

---

## 📬 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to fork the repository and submit a pull request.

---

---

## 🙌 Acknowledgements

Created with ❤️ by **Yuva** – Learning, building, and growing one line of code at a time.

[Connect with me on LinkedIn](https://www.linkedin.com/in/yuva-shankar-narayana/)
