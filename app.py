import os
import sys
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

# Define absolute paths for Render deployment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = 'customer_segmentation_secret_key_change_in_production'

# Import local helper files
from predictor import predict_segment
from recommendation import get_strategy
from database import get_db, init_db

# Initialize PostgreSQL database tables on startup
with app.app_context():
    init_db()


# Login Requirement Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# --- PUBLIC ROUTES ---

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db()
        cursor = conn.cursor()

        # Check if user email already exists (%s for PostgreSQL)
        cursor.execute('SELECT id FROM users WHERE email = %s', (email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            flash('Email address is already registered. Please log in.', 'danger')
            return redirect(url_for('register'))

        # Insert new user with hashed password
        hashed_pw = generate_password_hash(password)
        cursor.execute('INSERT INTO users (fullname, email, password) VALUES (%s, %s, %s)',
                       (fullname, email, hashed_pw))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['fullname']
            flash(f"Welcome back, {user['fullname']}!", 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))


# --- PROTECTED APP ROUTES ---

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    cursor = conn.cursor()

    # 1. Fetch total count of evaluations
    cursor.execute('SELECT COUNT(*) as count FROM predictions')
    result = cursor.fetchone()
    total_evaluations = result['count'] if result else 0

    # 2. Fetch top 5 recent predictions for the dashboard table
    cursor.execute('SELECT * FROM predictions ORDER BY id DESC LIMIT 5')
    recent_predictions = cursor.fetchall()

    cursor.close()
    conn.close()

    # 3. Pass both variables to dashboard.html
    return render_template(
        'dashboard.html',
        total_evaluations=total_evaluations,
        recent_predictions=recent_predictions
    )


@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    if request.method == 'POST':
        try:
            # 1. Parse inputs safely
            age = int(request.form.get('age', 0))
            gender = request.form.get('gender', 'Male')
            income = float(request.form.get('annual_income', 0))
            spending = int(request.form.get('spending_score', 0))

            input_data = {
                'age': age,
                'gender': gender,
                'income': income,
                'spending': spending
            }

            # 2. Predict cluster
            cluster_id = predict_segment(gender, age, income, spending)
            insight = get_strategy(cluster_id)

            # 3. Save prediction history to PostgreSQL (%s syntax)
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO predictions (gender, age, income, spending, cluster, label, description, recommendation)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (gender, age, income, spending, cluster_id, insight['label'], insight['description'], insight['recommendation']))
            conn.commit()
            cursor.close()
            conn.close()

            # 4. Return formatted results
            return render_template(
                'predict.html',
                result=True,
                cluster_id=cluster_id,
                insight=insight,
                input_data=input_data
            )

        except Exception as e:
            flash(f"Error during prediction: {str(e)}", "danger")
            return render_template('predict.html', result=False)

    return render_template('predict.html', result=False)


@app.route('/analytics')
@login_required
def analytics():
    metrics = [
        {'algorithm': 'K-Means', 'silhouette': 0.554, 'davies_bouldin': 0.812, 'calinski': 125.4, 'status': 'Best Model'},
        {'algorithm': 'Agglomerative', 'silhouette': 0.523, 'davies_bouldin': 0.890, 'calinski': 118.2, 'status': 'Evaluated'},
        {'algorithm': 'Hierarchical', 'silhouette': 0.518, 'davies_bouldin': 0.905, 'calinski': 115.8, 'status': 'Evaluated'},
        {'algorithm': 'DBSCAN', 'silhouette': 0.412, 'davies_bouldin': 1.120, 'calinski': 89.6, 'status': 'Evaluated'}
    ]
    return render_template('analytics.html', metrics=metrics)


@app.route('/history')
@login_required
def history():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM predictions ORDER BY id DESC')
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('history.html', records=records)

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
