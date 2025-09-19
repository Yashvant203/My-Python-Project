import mysql.connector
from mysql.connector import Error

# Function to establish MySQL connection
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="VP16@ddubca",  # replace with your MySQL password
            database="bank_system"
        )
        if conn.is_connected():
            print("Connection established successfully!")
            return conn
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to create a new customer
def create_customer(conn, name, email, phone, address):
    try:
        cursor = conn.cursor()
        query = "INSERT INTO customers (name, email, phone, address) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, email, phone, address))
        conn.commit()
        print("Customer added successfully!")
    except Error as e:
        print(f"Error: {e}")

# Function to create an account for a customer
def create_account(conn, customer_id, account_type):
    try:
        cursor = conn.cursor()
        query = "INSERT INTO accounts (customer_id, account_type) VALUES (%s, %s)"
        cursor.execute(query, (customer_id, account_type))
        conn.commit()
        print(f"Account created successfully for Customer ID: {customer_id}")
    except Error as e:
        print(f"Error: {e}")

# Function to deposit money into an account
def deposit_money(conn, account_id, amount):
    try:
        cursor = conn.cursor()
        query = "UPDATE accounts SET balance = balance + %s WHERE account_id = %s"
        cursor.execute(query, (amount, account_id))
        conn.commit()
        print(f"Deposited {amount} into Account ID: {account_id}")
        
        # Log the transaction
        query = "INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, %s, %s)"
        cursor.execute(query, (account_id, 'Deposit', amount))
        conn.commit()

    except Error as e:
        print(f"Error: {e}")

# Function to withdraw money from an account
def withdraw_money(conn, account_id, amount):
    try:
        cursor = conn.cursor()
        query = "SELECT balance FROM accounts WHERE account_id = %s"
        cursor.execute(query, (account_id,))
        balance = cursor.fetchone()[0]
        
        if balance >= amount:
            query = "UPDATE accounts SET balance = balance - %s WHERE account_id = %s"
            cursor.execute(query, (amount, account_id))
            conn.commit()
            print(f"Withdrew {amount} from Account ID: {account_id}")
            
            # Log the transaction
            query = "INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, %s, %s)"
            cursor.execute(query, (account_id, 'Withdrawal', amount))
            conn.commit()
        else:
            print("Insufficient balance.")
        
    except Error as e:
        print(f"Error: {e}")

# Function to view account balance
def view_balance(conn, account_id):
    try:
        cursor = conn.cursor()
        query = "SELECT balance FROM accounts WHERE account_id = %s"
        cursor.execute(query, (account_id,))
        balance = cursor.fetchone()[0]
        print(f"Balance for Account ID {account_id}: {balance}")
    except Error as e:
        print(f"Error: {e}")

# Function to view transaction history for an account
def view_transactions(conn, account_id):
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM transactions WHERE account_id = %s"
        cursor.execute(query, (account_id,))
        transactions = cursor.fetchall()
        
        print(f"\nTransactions for Account ID {account_id}:")
        for transaction in transactions:
            print(f"ID: {transaction[0]}, Type: {transaction[2]}, Amount: {transaction[3]}, Date: {transaction[4]}")
    except Error as e:
        print(f"Error: {e}")

# Main function for the banking system
def main():
    conn = create_connection()
    if conn is None:
        return
    
    while True:
        print("\nBanking Management System")
        print("1. Create Customer")
        print("2. Create Account")
        print("3. Deposit Money")
        print("4. Withdraw Money")
        print("5. View Balance")
        print("6. View Transactions")
        print("7. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter customer name: ")
            email = input("Enter customer email: ")
            phone = input("Enter customer phone: ")
            address = input("Enter customer address: ")
            create_customer(conn, name, email, phone, address)
        
        elif choice == '2':
            customer_id = int(input("Enter customer ID: "))
            account_type = input("Enter account type (Saving/Current): ")
            create_account(conn, customer_id, account_type)
        
        elif choice == '3':
            account_id = int(input("Enter account ID: "))
            amount = float(input("Enter amount to deposit: "))
            deposit_money(conn, account_id, amount)
        
        elif choice == '4':
            account_id = int(input("Enter account ID: "))
            amount = float(input("Enter amount to withdraw: "))
            withdraw_money(conn, account_id, amount)
        
        elif choice == '5':
            account_id = int(input("Enter account ID: "))
            view_balance(conn, account_id)
        
        elif choice == '6':
            account_id = int(input("Enter account ID: "))
            view_transactions(conn, account_id)
        
        elif choice == '7':
            print("Exiting system...")
            conn.close()
            break
        
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
