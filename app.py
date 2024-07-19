# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from db_queries import *


app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'  # Change this to a random secret key

@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        uid = str(uuid.uuid4())
        hashed_password = generate_password_hash(password)
        
        if register_user(uid, username, email, hashed_password):
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = get_user_by_username(username)
        if user and check_password_hash(user['hashpw'], password):
            session['user_id'] = user['uid']
            session['username'] = user['username']
            session['is_admin'] = is_admin(user['uid'])
            
            if session['is_admin']:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('player_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing_page'))

@app.route('/player_dashboard')
def player_dashboard():
    if 'user_id' not in session or session['is_admin']:
        return redirect(url_for('login'))
    
    quests_in_progress = get_quests_in_progress(session['user_id'])
    quests_completed = get_quests_completed(session['user_id'])
    quests_available = get_quests_available(session['user_id'])
    all_topics = get_all_topics()
    
    return render_template('player_dashboard.html', 
                           username=session['username'],
                           quests_in_progress=quests_in_progress,
                           quests_completed=quests_completed,
                           quests_available=quests_available,
                           all_topics=all_topics)

@app.route('/player_stats')
def player_stats():
    if 'user_id' not in session or session['is_admin']:
        return redirect(url_for('login'))
    
    uid = session['user_id']
    
    # Get total problems completed per difficulty
    problems_per_difficulty = get_problems_per_difficulty(uid)
    
    # Get problems completed per topic (and per difficulty)
    problems_per_topic = get_problems_per_topic(uid)
    
    # Get problems completed today
    problems_completed_today = get_problems_completed_today(uid)
    
    return render_template('player_stats.html',
                           username=session['username'],
                           problems_per_difficulty=problems_per_difficulty,
                           problems_per_topic=problems_per_topic,
                           problems_completed_today=problems_completed_today)

@app.route('/quest/<string:quest_id>')
def quest_page(quest_id):
    if 'user_id' not in session or session['is_admin']:
        return redirect(url_for('login'))
    
    quest = get_quest(quest_id)
    problems = get_quest_problems(quest_id)
    is_started = is_quest_started(session['user_id'], quest_id)
    completed_problems = get_completed_problems(session['user_id'])
    
    return render_template('quest_page.html',
                           quest=quest,
                           problems=problems,
                           is_started=is_started,
                           completed_problems=completed_problems)

@app.route('/start_quest/<string:quest_id>')
def start_quest(quest_id):
    if 'user_id' not in session or session['is_admin']:
        return redirect(url_for('login'))
    
    start_quest_for_player(session['user_id'], quest_id)
    return redirect(url_for('quest_page', quest_id=quest_id))

@app.route('/update_complete_problem/<string:quest_id>/<string:problem_id>/<string:is_complete>')
def update_complete_problem(quest_id, problem_id, is_complete):
    if 'user_id' not in session or session['is_admin']:
        return redirect(url_for('login'))
    
    if is_complete == 'true':
        complete_problem_for_player(session['user_id'], problem_id)
    elif is_complete == 'false':
        uncomplete_problem_for_player(session['user_id'], problem_id)
    return redirect(url_for('quest_page', quest_id=quest_id))

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or not session['is_admin']:
        return redirect(url_for('login'))
    
    created_quests = get_admin_created_quests(session['user_id'])
    return render_template('admin_dashboard.html',
                           username=session['username'],
                           created_quests=created_quests)

@app.route('/create_quest', methods=['GET', 'POST'])
def create_quest():
    if 'user_id' not in session or not session['is_admin']:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        quest_name = request.form['quest_name']
        problems = []
        for i in range(len(request.form.getlist('problem_link'))):
            problems.append({
                'link': request.form.getlist('problem_link')[i],
                'difficulty': request.form.getlist('difficulty')[i],
                'topics': request.form.getlist('topics')[i].split(',')
            })
        
        create_quest_with_problems(session['user_id'], quest_name, problems)
        flash('Quest created successfully', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('create_quest.html')

if __name__ == '__main__':
    app.run(debug=True)