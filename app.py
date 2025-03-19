from flask import Flask, render_template, request, redirect, url_for, session, flash
import joblib
import numpy as np
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# MySQL config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'  # Add your MySQL password here
app.config['MYSQL_DB'] = 'flask_users'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Load the pre-trained Random Forest model
model = joblib.load('school_needs_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        
        # Insert user into database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(username, password) VALUES (%s, %s)", (username, hashed_password))
        mysql.connection.commit()
        cur.close()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user['password'], password):
            session['logged_in'] = True
            session['username'] = user['username']
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))  # Redirect to main dashboard after login
        else:
            flash("Invalid credentials, please try again.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        return render_template('dashboard.html')  # Main page after successful login
    else:
        flash("Please log in to access the dashboard.", "danger")
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    if 'logged_in' not in session:
        flash("Please log in to access the prediction tool.", "danger")
        return redirect(url_for('login'))
    
    try:
        # Get data from form fields
        state = request.form['state']
        grade_configurations = request.form['grade_configurations']
        total_students = request.form['total_students']
        teachers = request.form['teachers']
        infrastructure_status = request.form['infrastructure_status']
        ai_recommended_category = request.form['ai_recommended_category']

        # Convert the input data into numerical format (modify based on actual encoding logic)
        state_encoded = int(state)  # Example: Assuming it's an integer value
        grade_configurations_encoded = int(grade_configurations)
        total_students = int(total_students)  # Convert student count to integer
        teachers = int(teachers)  # Convert teacher count to integer
        infrastructure_status_encoded = int(infrastructure_status)
        ai_recommended_category_encoded = int(ai_recommended_category)

        # Create a feature array
        features = np.array([[state_encoded, grade_configurations_encoded, total_students, teachers,
                              infrastructure_status_encoded, ai_recommended_category_encoded]])

        # Predict the outcome using the loaded model
        prediction = model.predict(features)

        # Convert prediction to human-readable text
        prediction_text = "Odd Structure" if prediction[0] == 1 else "Standard Structure"

        return render_template('result.html', prediction=prediction_text)

    except Exception as e:
        return f"Error during prediction: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
