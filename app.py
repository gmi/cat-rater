from flask import Flask, render_template, request, redirect, session
import os
import time
from src import database_operations as db
from src import funcs

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or 'dev-secret-key'

@app.route('/')
def home():
    return render_template("index.html", data=funcs.get_2_random())

@app.route('/vote', methods=['POST'])
def handle_vote():
    cat_id = request.form.get('cat_id')
    if not cat_id:
        return 'Invalid request', 400
    
    try:
        cat_id = int(cat_id)
    except ValueError:
        return 'Invalid cat ID', 400

    # Check if cat exists
    cat = db.get_cat_by_id(cat_id)
    if not cat:
        return 'Cat not found', 404

    current_time = time.time()

    # Check 1 vote per second globally
    last_vote_time = session.get('last_vote_time', 0)
    if current_time - last_vote_time < 1:
        return 'Rate limit exceeded: 1 vote per second', 429

    # Check 5-minute cooldown for same cat
    last_voted_cats = session.get('last_voted_cats', {})
    last_vote_for_cat = last_voted_cats.get(str(cat_id), 0)
    if current_time - last_vote_for_cat < 300:
        remaining = int(300 - (current_time - last_vote_for_cat))
        return f'Please wait {remaining} seconds before voting for this cat again', 429

    # Update database
    db.increment_rating(cat_id)

    # Update session
    session['last_vote_time'] = current_time
    last_voted_cats[str(cat_id)] = current_time
    session['last_voted_cats'] = last_voted_cats

    return redirect('/')

if __name__ == '__main__':
    db.create_database()
    app.run(debug=True)