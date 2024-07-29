from flask import Flask, request, render_template, redirect, url_for, session
from models import Conference, Feedback, db, User
from database import init_db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

with app.app_context():
    init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('index'))
        return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/add_conference', methods=['GET', 'POST'])
def add_conference():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        new_conference = Conference(title=title, description=description, location=location)
        db.session.add(new_conference)
        db.session.commit()
        return redirect(url_for('conferences'))
    return render_template('add_conference.html')

@app.route('/conferences')
def conferences():
    all_conferences = Conference.query.all()
    return render_template('conferences.html', conferences=all_conferences)

@app.route('/delete_conference/<int:id>', methods=['POST'])
def delete_conference(id):
    conference = Conference.query.get_or_404(id)
    db.session.delete(conference)
    db.session.commit()
    return redirect(url_for('conferences'))

@app.route('/feedback/<int:conference_id>', methods=['GET', 'POST'])
def feedback(conference_id):
    conference = Conference.query.get_or_404(conference_id)
    
    if request.method == 'POST':
        content = request.form['content']
        user_id = 1  # Replace with the current user's ID from the session or user context
        feedback = Feedback(conference_id=conference_id, user_id=user_id, content=content)
        db.session.add(feedback)
        db.session.commit()
        return redirect(url_for('conferences'))
    
    return render_template('feedback.html', conference=conference)

if __name__ == '__main__':
    app.run(debug=True)
