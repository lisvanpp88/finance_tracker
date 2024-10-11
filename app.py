from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

#Database initialization

def init_db():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

#Route  for home page 
@app.route('/')
def index():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()

    c.execute('SELECT * FROM transactions')
    transactions = c.fetchall()

    #calculate  total balance

    income = sum(t[2] for t in transactions if t[3] == 'income')
    expenses = sum(t[2] for t in transactions if t[3] == 'expense')
    print(income)
    print(expenses)
    total_balance = income - expenses


    conn.close()
    return render_template('index.html', transactions=transactions, balance=total_balance)

# Route to add a new transaction
@app.route('/add', methods=['POST'])
def add_transaction():
    description = request.form['description']
    amount = float(request.form['amount'])
    transaction_type = request.form['type']

    conn = sqlite3.connect('finance.db')
    c = conn.cursor()

    c.execute('INSERT INTO transactions (description, amount, type) VALUES (?, ?, ?)', 
              (description, amount, transaction_type))
    
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Initialize database when app starts
if __name__ == '__main__':
    init_db()
    app.run(debug=True)



