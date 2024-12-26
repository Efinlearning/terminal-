from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import secrets
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)

# Generate a secret key
app.config['SECRET_KEY'] = secrets.token_hex(24)

# Set up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Route for the home page (redirects to login)
@app.route('/')
def index():
    return redirect(url_for('login'))

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form['login']
        password = request.form['password']
        
        # Check if login is email or phone
        user = None
        if '@' in login_input:
            user = User.query.filter_by(email=login_input).first()
        else:
            user = User.query.filter_by(phone=login_input).first()

        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        return "Invalid credentials"
    return render_template('login.html')

# Route for the dashboard page
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

# Route for logging out
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        
        # Validate email
        try:
            validate_email(email)
        except EmailNotValidError:
            return "Invalid email"

        # Add the user to the database
        user = User(email=email, phone=phone, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

# Run the app
if __name__ == '__main__':
    db.create_all()  # Creates tables if they don't exist
    app.run(debug=True)
