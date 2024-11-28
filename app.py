from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Use SQLite for local deployment (this file will be created in the root of your project)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Feedback model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        feedback = Feedback(name=name, email=email, subject=subject, message=message)
        db.session.add(feedback)
        db.session.commit()
        return redirect(url_for('thank_you'))

@app.route('/thank-you')
def thank_you():
    return 'Thank you for your feedback!'

if __name__ == '__main__':
    db.create_all()  # Creates the SQLite database and tables
    app.run(debug=True)
