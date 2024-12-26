from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Secret key for sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/users.db'  # SQLite DB for storing users
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model for storing user info
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Getting input from form
        login_input = request.form['login']
        password = request.form['password']
        
        # Check if the input is email or phone
        if '@' in login_input:
            user = User.query.filter_by(email=login_input).first()
        else:
            user = User.query.filter_by(phone=login_input).first()

        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials"
        
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

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

        user = User(email=email, phone=phone, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == '__main__':
    db.create_all()  # Create tables
    app.run(debug=True)
