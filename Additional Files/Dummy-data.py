from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
from contextlib import contextmanager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
db = SQLAlchemy(app)

# Define models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

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
with app.app_context():

# Create the database tables
    db.create_all()


# Create dummy data
    def create_dummy_data():
    # Create and add a dummy user
        dummy_user = User(username='Abdelrhman Hatem', email='Abdelrahman@ecu.com', password_hash=generate_password_hash('password'))
        db.session.add(dummy_user)
        db.session.commit()

    # Create dummy transactions
        dummy_transactions = [
            Transaction(user_id=dummy_user.id, amount=100.0, category='Groceries', date=datetime.utcnow()),
            Transaction(user_id=dummy_user.id, amount=50.0, category='Dining', date=datetime.utcnow()),
            Transaction(user_id=dummy_user.id, amount=30.0, category='Shopping', date=datetime.utcnow()),
            Transaction(user_id=dummy_user.id, amount=20.0, category='Entertainment', date=datetime.utcnow()),
            Transaction(user_id=dummy_user.id, amount=10.0, category='Transportation', date=datetime.utcnow()),
        # Add more dummy transactions...
        ]
        db.session.add_all(dummy_transactions)

    # Create dummy savings goals
        dummy_savings_goals = [
            SavingsGoal(user_id=dummy_user.id, target_amount=1000.0, current_amount=200.0, deadline=datetime.utcnow()),
            SavingsGoal(user_id=dummy_user.id, target_amount=800.0, current_amount=150.0, deadline=datetime.utcnow()),
            SavingsGoal(user_id=dummy_user.id, target_amount=1200.0, current_amount=300.0, deadline=datetime.utcnow()),
            SavingsGoal(user_id=dummy_user.id, target_amount=1500.0, current_amount=600.0, deadline=datetime.utcnow()),
        # Add more dummy savings goals...
        ]
        db.session.add_all(dummy_savings_goals)

    # Create dummy budgets
        dummy_budgets = [
            Budget(user_id=dummy_user.id, category='Food', limit=200.0),
            Budget(user_id=dummy_user.id, category='Entertainment', limit=100.0),
            Budget(user_id=dummy_user.id, category='Transportation', limit=50.0),
            Budget(user_id=dummy_user.id, category='Shopping', limit=150.0),
            Budget(user_id=dummy_user.id, category='Utilities', limit=80.0),
        # Add more dummy budgets...
        ]
        db.session.add_all(dummy_budgets)

    # Create dummy income
        dummy_income = Income(user_id=dummy_user.id, amount=2000.0, source='Salary', date=datetime.utcnow())
        db.session.add(dummy_income)

    # Create dummy expenses
        dummy_expenses = [
            Expense(user_id=dummy_user.id, amount=50.0, category='Transportation', date=datetime.utcnow()),
            Expense(user_id=dummy_user.id, amount=30.0, category='Utilities', date=datetime.utcnow()),
            Expense(user_id=dummy_user.id, amount=25.0, category='Food', date=datetime.utcnow()),
            Expense(user_id=dummy_user.id, amount=15.0, category='Entertainment', date=datetime.utcnow()),
            Expense(user_id=dummy_user.id, amount=40.0, category='Shopping', date=datetime.utcnow()),
        # Add more dummy expenses...
        ]
        db.session.add_all(dummy_expenses)

    # Commit changes to the database
        db.session.commit()

@contextmanager
def app_context():
    with app.app_context():
        yield

if __name__ == '__main__':
    with app_context():
        db.create_all()  # Create database tables
        create_dummy_data()  # Populate the database with dummy data