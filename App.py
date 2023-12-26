from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash
from datetime import datetime
import os
import logging

app = Flask(__name__, static_url_path='/static', static_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
logging.basicConfig(level=logging.INFO)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    balance = db.relationship('Balance', backref='user', uselist=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

class SavingsGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0.0)
    deadline = db.Column(db.DateTime)

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    limit = db.Column(db.Float, nullable=False)

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    source = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': self.amount,
            'source': self.source,
            'date': self.date.isoformat()
        }

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': self.amount,
            'category': self.category,
            'date': self.date.isoformat()
        }
    
class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error.html', error='Page not found'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error='Internal server error'), 500
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def is_logged_in():
    """Check if the current user is logged in."""
    return current_user.is_authenticated

@app.route('/', methods=['GET', 'POST'])
def login():
    logging.info("Login route accessed")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        logging.info(f"Attempting login for user: {username}")

        user = User.query.filter_by(username=username).first()
        if user:
            logging.info("User found in database")
            if bcrypt.check_password_hash(user.password_hash, password):
                logging.info("Password matched, logging in user")
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                logging.info("Password mismatch")
        else:
            logging.info("User not found")

        return render_template('Login.html', error='Invalid username or password')
    
    logging.info("Rendering login page")
    return render_template('Login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, password_hash=hashed_password, email=email)
            initial_balance = Balance(user_id=new_user.id, amount=0.0)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login')) 

        return render_template('signup.html')
    except Exception as e:
        db.session.rollback()
        return render_template('error.html', error=f'Error during signup: {e}'), 500

@app.route('/dashboard')
def dashboard():
    if not is_logged_in():
        return redirect(url_for('login'))
    user_id = current_user.id
    user_balance = Balance.query.filter_by(user_id=user_id).first()
    balance_amount = user_balance.amount if user_balance else 0
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    total_spent = sum(transaction.amount for transaction in transactions)
    return render_template('Dashboard.html', user_name=current_user.username, balance=balance_amount, transactions=transactions, total_spent=total_spent)

@app.route('/add_balance', methods=['GET', 'POST'])
@login_required
def add_balance():
    user_id = current_user.id
    user_balance = Balance.query.filter_by(user_id=user_id).first()

    if request.method == 'POST':
        # Check if it's an AJAX request
        if request.is_json:
            data = request.get_json()
            amount_to_add = float(data['amount'])
        else:
            amount_to_add = float(request.form['amount'])

        # Check if the balance record exists and update it
        if user_balance:
            user_balance.amount += amount_to_add
        else:
            # If no balance record exists, create a new one
            user_balance = Balance(user_id=user_id, amount=amount_to_add)
            db.session.add(user_balance)

        # Commit the changes to the database
        db.session.commit()

        # For AJAX request, return JSON response
        if request.is_json:
            return jsonify({'message': 'Balance updated successfully'}), 200
        else:
            # For regular form submission, re-render the balance page with updated info
            return render_template('Balance.html', balance=user_balance.amount)

    # If it's a GET request, render the balance page
    balance_amount = user_balance.amount if user_balance else 0
    return render_template('Balance.html', balance=balance_amount)

@app.route('/logout')
def logout():
    if not is_logged_in():
        return redirect(url_for('login'))
    logout_user()
    return redirect(url_for('login'))

# Add income record
@app.route('/income', methods=['POST'])
@login_required  # Make sure the user is logged in
def add_income():
    # Get the user_id from the current user
    user_id = current_user.id
    amount_str = request.json['amount']  # Get the amount as a string
    source = request.json['source']
    date_str = request.json['date']  # Get the date as a string

    try:
        # Convert the amount and date strings to their respective data types
        amount = float(amount_str)
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid data format'}), 400

    # Create new income record
    new_income = Income(user_id=user_id, amount=amount, source=source, date=date)
    db.session.add(new_income)
    db.session.commit()

    # Update the user's balance
    user_balance = Balance.query.filter_by(user_id=user_id).first()
    if user_balance:
        user_balance.amount += amount
    else:
        # If no balance record exists, create a new one
        user_balance = Balance(user_id=user_id, amount=amount)
        db.session.add(user_balance)
    db.session.commit()

    return jsonify({'message': 'Income record added successfully'}), 201

# Get income records
@app.route('/income', methods=['GET'])
@login_required
def get_income():
    user_id = current_user.id
    income_records = Income.query.filter_by(user_id=user_id).all()

    # Render the 'Income.html' template and pass the income_records data to it
    return render_template('Income.html', income_records=income_records)

# Add expense record
@app.route('/expenses', methods=['POST'])
@login_required
def add_expense():
    try:
        # Extract data from the request
        user_id = current_user.id
        amount = request.json['amount']
        category = request.json['category']
        date_str = request.json['date']

        # Convert the date string to a datetime object
        date = datetime.strptime(date_str, '%Y-%m-%d')

        # Create a new expense record
        new_expense = Expense(user_id=user_id, amount=amount, category=category, date=date)
        db.session.add(new_expense)

        # Additionally, create and add a transaction record
        new_transaction = Transaction(user_id=user_id, amount=amount, category=category, date=date)
        db.session.add(new_transaction)

        # Commit changes to the database
        db.session.commit()

        return jsonify({'message': 'Expense and transaction added successfully'}), 201

    except Exception as e:
        # Rollback in case of error
        db.session.rollback()
        # Log the exception and return an error response
        app.logger.error(f"Error in add_expense: {e}")
        return jsonify({'error': 'An error occurred while adding the expense'}), 500

@app.route('/get_transactions')
@login_required
def get_transactions():
    user_id = current_user.id
    # Fetch transaction data for the current user from the database
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    
    # Create a list of transactions in the desired format
    transaction_data = [{'category': transaction.category, 'amount': transaction.amount} for transaction in transactions]
    
    # Return the transaction data as JSON
    return jsonify(transaction_data)

# Get expense records
@app.route('/expenses', methods=['GET'])
@login_required
def get_expenses():
    try:
        # Assume user_id is retrieved from request or session
        user_id = current_user.id
        expenses = Expense.query.filter_by(user_id=user_id).all()

        # Convert expenses to a suitable format if necessary
        expenses_data = [expense.to_dict() for expense in expenses]

        # Render the Expense.html template, passing in the expenses data
        return render_template('Expense.html', expenses=expenses_data)

    except Exception as e:
        # Log the exception for debugging
        app.logger.error(f"Error in get_expenses: {e}")
        # Optionally, render a different template or return an error message
        return render_template('error.html', error=str(e))

    # Optional: In case of no expenses or user_id not found, handle accordingly
    # return render_template('Expense.html', expenses=[])


# Get transactions by category
@app.route('/transactions/<category>', methods=['GET'])
@login_required
def transactions_by_category(category):
    user_id = request.args.get('user_id')

    # Fetch transactions for the given category and user
    transactions = Transaction.query.filter_by(user_id=user_id, category=category).all()

    # Convert transactions to a JSON-serializable format
    transactions_data = [transaction.to_dict() for transaction in transactions]

    return jsonify(transactions_data), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)
