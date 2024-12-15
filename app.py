from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Database connection function
def connect_db():
    return sqlite3.connect('tax_system.db')

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Route to fetch all transactions
@app.route('/payments', methods=['GET'])
def get_payments():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TaxPayments")
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

# Route to add a new transaction
@app.route('/payments', methods=['POST'])
def add_payment():
    data = request.json
    if not data.get('due_date'):  # Validate due_date
        return jsonify({"error": "Due date is required!"}), 400

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO TaxPayments (company, amount, payment_date, status, due_date)
            VALUES (?, ?, ?, ?, ?)""",
            (data['company'], data['amount'], data.get('payment_date'), data['status'], data['due_date'])
        )
        conn.commit()
        return jsonify({"message": "Payment added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()


# Update an existing payment
@app.route('/payments/<int:id>', methods=['PUT'])
def update_payment(id):
    data = request.json
    if not data.get('due_date'):  # Validate due_date
        return jsonify({"error": "Due date is required!"}), 400

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE TaxPayments
            SET company = ?, amount = ?, payment_date = ?, status = ?, due_date = ?
            WHERE id = ?""",
            (data['company'], data['amount'], data.get('payment_date'), data['status'], data['due_date'], id)
        )
        conn.commit()
        return jsonify({"message": "Payment updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()



# Route to delete a transaction
@app.route('/payments/<int:id>', methods=['DELETE'])
def delete_payment(id):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM TaxPayments WHERE id = ?", (id,))
        conn.commit()
        return jsonify({"message": "Payment deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

"""

# Route to filter payments by due date and calculate totals
@app.route('/payments/summary', methods=['GET'])
def get_summary():
    due_date = request.args.get('due_date')
    tax_rate = float(request.args.get('tax_rate', 0.0))  # Tax rate
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TaxPayments WHERE due_date = ?", (due_date,))
    rows = cursor.fetchall()

    total_paid = sum(row[2] for row in rows if row[4] == 'paid')
    total_unpaid = sum(row[2] for row in rows if row[4] == 'unpaid')
    total_tax_due = (total_paid + total_unpaid) * tax_rate

    conn.close()

    return jsonify({
        "records": rows,
        "total_paid": total_paid,
        "total_unpaid": total_unpaid,
        "total_tax_due": total_tax_due
    })

if __name__ == '__main__':
    app.run(debug=True)
"""

@app.route('/payments/summary', methods=['GET'])
def get_summary():
    due_date = request.args.get('due_date')  # Get the due date
    tax_rate = float(request.args.get('tax_rate', 0.0))  # Tax rate provided by the user

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TaxPayments WHERE due_date = ?", (due_date,))
    rows = cursor.fetchall()

    total_amount = sum(row[2] for row in rows)  # Total amount
    tax_due = total_amount * tax_rate  # Tax due

    conn.close()
    return jsonify({
        "records": rows,
        "total_amount": total_amount,
        "tax_due": tax_due
    })

if __name__ == '__main__':
    app.run(debug=True)