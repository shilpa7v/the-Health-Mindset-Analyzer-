from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import random
import matplotlib.pyplot as plt
from gtts import gTTS
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_mindset.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

questions = [
    "I prioritize my physical health.",
    "I regularly engage in physical exercise.",
    "I eat a balanced and nutritious diet.",
    "I prioritize my mental health.",
    "I actively manage my stress levels.",
    "I prioritize getting enough sleep.",
    "I seek out information on healthy living."
]

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    answers = db.Column(db.String(200), nullable=False)
    feedback = db.Column(db.String(500), nullable=False)
    mindset_changed = db.Column(db.Boolean, nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    random.shuffle(questions)
    return render_template('index.html', questions=questions)

@app.route('/submit', methods=['POST'])
@login_required
def submit():
    name = request.form['name']
    age = request.form['age']
    answers = [int(request.form[f'question{i}']) for i in range(1, len(questions)+1)]
    language = request.form['language'].lower()

    feedback_text, speech_text, mindset_changed = give_feedback(answers, language, name)
    speech_file = save_speech(speech_text, language)
    chart_file = generate_pie_chart(answers)

    new_response = Response(name=name, age=age, answers=','.join(map(str, answers)), feedback=feedback_text, mindset_changed=mindset_changed)
    db.session.add(new_response)
    db.session.commit()

    return render_template('result.html', feedback_text=feedback_text, speech_file=speech_file, chart_file=chart_file, name=name, mindset_changed=mindset_changed)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    responses = Response.query.filter_by(name=current_user.username).all()
    return render_template('dashboard.html', responses=responses)

@app.route('/achievements')
@login_required
def achievements():
    # Example logic for checking achievements
    responses = Response.query.filter_by(name=current_user.username).all()
    improvement = False
    if len(responses) > 1:
        improvement = responses[-1].mindset_changed != responses[-2].mindset_changed
    return render_template('achievements.html', improvement=improvement)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

def save_speech(text, language):
    tts = gTTS(text=text, lang=language)
    speech_file = "output.mp3"
    tts.save(speech_file)
    return speech_file

def generate_pie_chart(answers):
    labels = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
    counts = [answers.count(i) for i in range(1, 6)]
    explode = (0.1, 0, 0, 0, 0)
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0']

    plt.figure(figsize=(8, 6))
    plt.pie(counts, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of Responses')
    plt.axis('equal')
    chart_file = 'static/chart.png'
    plt.savefig(chart_file)
    plt.close()
    return chart_file

def give_feedback(answers, language='en', name=""):
    feedback = {
        'en': {
            'health_focused': f"{name}, your mindset seems to be focused on health. Keep up the good work!",
            'less_health_focused': f"{name}, you might need to focus more on your health. Here are some tips to improve."
        }
    }
    language_feedback = feedback.get(language, feedback['en'])
    healthy_count = sum(answer in [4, 5] for answer in answers)
    feedback_text = language_feedback['health_focused'] if healthy_count >= len(answers) / 2 else language_feedback['less_health_focused']
    return feedback_text, "Speech text placeholder", healthy_count >= len(answers) / 2

if __name__ == "__main__":
    app.run(debug=True)
