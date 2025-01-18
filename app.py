from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key =  b'\x04\x85\x858\x8e\xbc\xa8\xaa\xe7L\xdb@\xde\xb4\x01\xac\xdb\xd3\xdc\x82\xce\x1bH'

# Connect to MySQL database
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='budget_db',
            user='root', 
            password='KBABU0307' 
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

@app.route('/')
def dashboard():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT SUM(amount) AS total_income FROM income")
    total_income = cursor.fetchone()['total_income'] or 0

    cursor.execute("SELECT SUM(amount) AS total_expenses FROM expenses")
    total_expenses = cursor.fetchone()['total_expenses'] or 0

    cursor.execute("SELECT SUM(amount) AS total_savings FROM savings")
    total_savings = cursor.fetchone()['total_savings'] or 0

    connection.close()

    # Pass data to the template for visualization
    return render_template('dashboard.html', total_income=total_income, 
                           total_expenses=total_expenses, total_savings=total_savings)

@app.route('/add_income', methods=['POST', 'GET'])
def add_income():
    if request.method == 'POST':
        amount = request.form['amount']
        description = request.form['description']
        date = request.form['date']

        connection = get_db_connection()
        if not connection:
            flash("Database connection failed.")
            return redirect(url_for('dashboard'))

        try:
            cursor = connection.cursor(dictionary=True)  # Enable dictionary cursor
            cursor.execute("INSERT INTO income (amount, description, date) VALUES (%s, %s, %s)",
                           (amount, description, date))

            # Fetch aggregated values
            cursor.execute("SELECT SUM(amount) AS total_income FROM income")
            total_income = cursor.fetchone().get('total_income', 0)

            cursor.execute("SELECT SUM(amount) AS total_expenses FROM expenses")
            total_expenses = cursor.fetchone().get('total_expenses', 0)

            cursor.execute("SELECT SUM(amount) AS total_savings FROM savings")
            total_savings = cursor.fetchone().get('total_savings', 0)

            connection.commit()
            print('Income added successfully!')
        except Exception as e:
            print("Error while adding income:", e)
            flash("Failed to add income.")
        finally:
            connection.close()

        # Redirect or render the page
        return redirect(url_for('dashboard'))

    # If the method is GET, render the form
    return render_template('addincome.html')

@app.route('/add_expense', methods=['POST', 'GET'])
def add_expense():
    if request.method == 'POST':
        amount = request.form['amount']
        description = request.form['description']
        date = request.form['date']

        connection = get_db_connection()
        if not connection:
            flash("Database connection failed.")
            return redirect(url_for('dashboard'))

        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO expenses (amount, description, date) VALUES (%s, %s, %s)",
                           (amount, description, date))
            connection.commit()
            flash('Expense added successfully!')
        except Exception as e:
            print("Error while adding expense:", e)
            flash("Failed to add expense.")
        finally:
            connection.close()

        # Redirect to a safe page after the POST request
        return redirect(url_for('dashboard'))

    # If the method is GET, render the form
    return render_template('add_expense.html')

@app.route('/add_savings', methods=['POST', 'GET'])
def add_savings():
    if request.method == 'POST':
        amount = request.form['amount']
        description = request.form['description']
        date = request.form['date']

        connection = get_db_connection()
        if not connection:
            flash("Database connection failed.")
            return redirect(url_for('dashboard'))

        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO savings (amount, description, date) VALUES (%s, %s, %s)",
                           (amount, description, date))
            connection.commit()
            flash('Savings added successfully!')
        except Exception as e:
            print("Error while adding savings:", e)
            flash("Failed to add savings.")
        finally:
            connection.close()

        # Redirect to a different page after successful POST
        return redirect(url_for('dashboard'))

    # If the method is GET, render the form (optional)
    return render_template('add_savings.html')


if __name__ == '__main__':
    app.run(debug=True)
