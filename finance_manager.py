import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from datetime import datetime

# Database setup
conn = sqlite3.connect('finance_manager.db')
cursor = conn.cursor()

# Create a table to store transactions
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    amount REAL,
    category TEXT,
    date TEXT,
    description TEXT
)
''')

conn.commit()

# Function to add a transaction
def add_transaction(amount, category, description):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
    INSERT INTO transactions (amount, category, date, description)
    VALUES (?, ?, ?, ?)
    ''', (amount, category, date, description))
    conn.commit()

# Function to get all transactions
def get_transactions():
    cursor.execute('SELECT * FROM transactions')
    return cursor.fetchall()

# Function to categorize transactions and calculate totals
def categorize_expenses():
    transactions = pd.read_sql('SELECT * FROM transactions', conn)
    categorized = transactions.groupby('category')['amount'].sum().reset_index()
    return categorized

# Function to visualize expenses by category
def visualize_expenses():
    categorized = categorize_expenses()
    plt.figure(figsize=(10, 6))
    sns.barplot(x='category', y='amount', data=categorized)
    plt.title('Expenses by Category')
    plt.xlabel('Category')
    plt.ylabel('Amount Spent')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Function to calculate total expenses and income
def financial_summary():
    transactions = pd.read_sql('SELECT * FROM transactions', conn)
    total_expenses = transactions[transactions['amount'] < 0]['amount'].sum()
    total_income = transactions[transactions['amount'] > 0]['amount'].sum()
    print(f"Total Income: ${total_income:.2f}")
    print(f"Total Expenses: ${total_expenses:.2f}")
    print(f"Net Savings: ${total_income + total_expenses:.2f}")

# Main menu
def main():
    print("Personal Finance Manager")
    while True:
        print("\n1. Add Transaction")
        print("2. View Transactions")
        print("3. View Expense Categories")
        print("4. View Financial Summary")
        print("5. Visualize Expenses")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            amount = float(input("Enter amount (negative for expenses, positive for income): "))
            category = input("Enter category (e.g., Food, Rent, etc.): ")
            description = input("Enter description (optional): ")
            add_transaction(amount, category, description)
            print("Transaction added.")
        elif choice == '2':
            transactions = get_transactions()
            for t in transactions:
                print(f"ID: {t[0]}, Amount: {t[1]}, Category: {t[2]}, Date: {t[3]}, Description: {t[4]}")
        elif choice == '3':
            categorized = categorize_expenses()
            print(categorized)
        elif choice == '4':
            financial_summary()
        elif choice == '5':
            visualize_expenses()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
