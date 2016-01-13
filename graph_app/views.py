from .models import User, get_todays_recent_offers
from flask import Flask, request, session, redirect, url_for, render_template, flash

app = Flask(__name__)

@app.route('/')
def index():
    offers = get_todays_recent_offers()
    return render_template('welcome.html', offers=offers)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if len(username) < 1:
            flash('* Please enter a fun username.')
        elif len(password) < 5:
            flash('* Please enter a password with at least 5 chracters.')
        elif not User(username).register(password):
            flash('* Sorry, that username already exists.')
        else:
            session['username'] = username
            flash('Logged in.')
            return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not User(username).verify_password(password):
            flash('* Invalid log-in, please try again.')
        else:
            session['username'] = username
            # flash('Logged in.')
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out.')
    return redirect(url_for('index'))

@app.route('/add_offer', methods=['POST'])
def add_offer():
    title = request.form['title']
    tags = request.form['tags']
    text = request.form['text']

    if not title or not tags or not text:
        if not title:
            flash('Please give your offer a title.')
        if not tags:
            flash('Please give your offer at least one tag.')
        if not text:
            flash('Please give your offer some details.')
    else:
        User(session['username']).add_offer(title, tags, text)

    return redirect(url_for('index'))

@app.route('/like_offer/<offer_id>')
def like_offer(offer_id):
    username = session.get('username')

    if not username:
        flash('You must be logged in to like an offer.')
        return redirect(url_for('login'))

    User(username).like_offer(offer_id)

    flash('Liked offer.')
    return redirect(request.referrer)

@app.route('/profile/<username>')
def profile(username):
    logged_in_username = session.get('username')
    user_being_viewed_username = username

    user_being_viewed = User(user_being_viewed_username)
    offers = user_being_viewed.get_recent_offers()

    similar = []
    common = []

    if logged_in_username:
        logged_in_user = User(logged_in_username)

        if logged_in_user.username == user_being_viewed.username:
            similar = logged_in_user.get_similar_users()
        else:
            common = logged_in_user.get_commonality_of_user(user_being_viewed)

    return render_template(
        'profile.html',
        username=username,
        offers=offers,
        similar=similar,
        common=common
    )
    