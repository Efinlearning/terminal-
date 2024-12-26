from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)

# Generate a secret key for session management
app.config['SECRET_KEY'] = secrets.token_hex(24)

# Set up SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# User model (database schema)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Ensure the tables are created when the app is first run
if __name__ == '__main__':
    # Wrap the database creation in an application context
    with app.app_context():
        db.create_all()  # Creates the database tables if they don't exist already

    app.run(debug=True)
