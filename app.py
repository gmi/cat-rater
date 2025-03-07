from flask import Flask, render_template, request, redirect
import time
import os
from src import database_operations as db
from src import funcs

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", data=funcs.get_2_random())

@app.route('/vote', methods=['POST'])
def handle_vote():
    cat_id = request.form.get('cat_id')
    voter_ip = request.remote_addr  # Get client IP address
    
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

    # Check 1 vote per second globally by IP
    last_vote_time = db.get_last_vote_time(voter_ip)
    if time.time() - last_vote_time < 1:
        return 'Rate limit exceeded: 1 vote per second', 429

    # Check 5-minute cooldown for specific cat by IP
    last_vote_for_cat = db.get_last_cat_vote_time(voter_ip, cat_id)
    if time.time() - last_vote_for_cat < 300:
        remaining = int(300 - (time.time() - last_vote_for_cat))
        return f'Please wait {remaining} seconds before voting for this cat again', 429

    # Update database
    db.increment_rating(cat_id)
    db.log_vote(voter_ip, cat_id)

    return redirect('/')

@app.route("/leaderboard")
def lb():
    return(render_template("leaderboard.html", data=funcs.get_lb()))
if __name__ == '__main__':
    db.create_database()
    app.run(debug=True)