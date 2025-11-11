import os
import csv
from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime

app = Flask(__name__)
# SECURITY NOTE: In a real production app, use a secure, secret key.
# For now, this simple key works for flash messages.
app.secret_key = 'sanatan_secure_key_temporary'

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling newsletter subscriptions
@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    
    if email:
        # NOTE FOR DEPLOYMENT: On many free hosting platforms (like Render free tier),
        # local files like 'subscribers.csv' are deleted every time the server restarts.
        # For a permanent solution, you would need a real database or an external email service.
        # We are using CSV here as requested for simplicity.
        csv_file = 'subscribers.csv'
        file_exists = os.path.isfile(csv_file)
        
        try:
            with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(['Date', 'Email']) # Write header if new file
                writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), email])
            
            flash("Dhanyavad! You have successfully joined our journey.", "success")
        except Exception as e:
            # In case of permission errors on server
            flash("An error occurred. Please try again later.", "error")
            print(f"Subscription error: {e}")
            
    else:
        flash("Please enter a valid email address.", "warning")
        
    return redirect(url_for('index') + '#newsletter')

# This ensures the app runs locally when you execute 'python app.py'
if __name__ == '__main__':
    # host='0.0.0.0' tells Flask to listen for connections from any device on the network
    app.run(debug=True, host='0.0.0.0')