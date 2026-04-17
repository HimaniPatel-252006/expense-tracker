from flask import Flask, request, jsonify, send_file
import sqlite3

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount INTEGER,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Serve frontend
@app.route('/')
def home():
    return send_file('index.html')


# ➕ Add Expense
@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data received"}), 400

    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO expenses (amount, category) VALUES (?, ?)",
        (data['amount'], data['category'])
    )

    conn.commit()
    conn.close()

    return jsonify({"status": "saved"})


# 📋 Get Expenses
@app.route('/expenses', methods=['GET'])
def get_expenses():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    conn.close()

    expenses = []
    for row in rows:
        expenses.append({
            "id": row[0],
            "amount": row[1],
            "category": row[2]
        })

    return jsonify(expenses)


# ❌ Delete Expense
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"status": "deleted"})


if __name__ == '__main__':
    app.run(debug=True)