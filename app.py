import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import init_db, get_db
from utils.predictor import predict_segment
from utils.recommendation import get_strategy

app = Flask(__name__)
app.secret_key = 'customer_segmentation_secret_key_change_in_production'

# Initialize Database
init_db()

# Decorator to protect routes requiring authentication
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Authentication Routes ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        conn = get_db()
        existing_user = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()

        if existing_user:
            conn.close()
            flash('Email address already registered. Please sign in.', 'warning')
            return redirect(url_for('login'))

        hashed_password = generate_password_hash(password)
        conn.execute(
            'INSERT INTO users (fullname, email, password) VALUES (?, ?, ?)',
            (fullname, email, hashed_password)
        )
        conn.commit()
        conn.close()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']

        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['fullname']
            session['user_email'] = user['email']
            flash(f"Welcome back, {user['fullname']}!", 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# --- Protected Application Routes ---

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    total = conn.execute('SELECT COUNT(*) FROM predictions').fetchone()[0]
    recents = conn.execute('SELECT * FROM predictions ORDER BY id DESC LIMIT 5').fetchall()
    conn.close()
    return render_template('dashboard.html', total=total, recents=recents)


@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    if request.method == 'POST':
        gender = request.form['gender']
        age = int(request.form['age'])
        income = float(request.form['annual_income'])
        spending = int(request.form['spending_score'])

        cluster_id = predict_segment(gender, age, income, spending)
        insight = get_strategy(cluster_id)

        conn = get_db()
        conn.execute(
            '''INSERT INTO predictions 
               (gender, age, income, spending, cluster, label, description, recommendation) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (gender, age, income, spending, cluster_id, 
             insight['label'], insight['description'], insight['recommendation'])
        )
        conn.commit()
        conn.close()

        return render_template('predict.html', 
                               result=True, 
                               cluster_id=cluster_id, 
                               insight=insight,
                               input_data={'gender': gender, 'age': age, 'income': income, 'spending': spending})

    return render_template('predict.html', result=False)


@app.route('/history')
@login_required
def history():
    conn = get_db()
    records = conn.execute('SELECT * FROM predictions ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('history.html', records=records)


@app.route('/analytics')
@login_required
def analytics():
    metrics = [
        {"algorithm": "K-Means", "silhouette": 0.554, "davies_bouldin": 0.821, "calinski": 165.3, "status": "Best Model"},
        {"algorithm": "Agglomerative", "silhouette": 0.523, "davies_bouldin": 0.892, "calinski": 148.1, "status": "Evaluated"},
        {"algorithm": "Hierarchical", "silhouette": 0.518, "davies_bouldin": 0.910, "calinski": 142.5, "status": "Evaluated"},
        {"algorithm": "DBSCAN", "silhouette": 0.412, "davies_bouldin": 1.150, "calinski": 95.8, "status": "Evaluated"}
    ]
    return render_template('analytics.html', metrics=metrics)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)