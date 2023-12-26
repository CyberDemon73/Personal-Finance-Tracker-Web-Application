from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

# Create the database tables within the Flask application context
with app.app_context():
    db.create_all()

    # Create a password hash
    password_hash = generate_password_hash('P@ssw0rd')

    # Create a new user record
    new_user = User(username='MohamedHisham', email='19200066@ecu.edu.eg', password_hash=password_hash)

    # Add the user record to the database
    db.session.add(new_user)
    db.session.commit()
