"""Server for calendar app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, url_for)
from werkzeug.security import check_password_hash
from passlib.hash import argon2
from model import connect_to_db, db
from datetime import datetime
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'secretkey'
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage"""

    return render_template('homepage.html')



@app.route('/login', methods=['POST', 'GET'])
def login():
    """Log user into application."""

    if 'current_user' in session:
        flash('You are already logged in.')
        return redirect(url_for('dashboard'))
    
    username = request.form.get('username')
    password = request.form.get('password')

    # Retrieve user by username
    user = crud.get_user_by_username(username)

    if user and argon2.verify(password, user.password):
        # If the user exists and the password is correct, store username in the session
        session['current_user'] = username
        flash(f'Logged in as {username}')
        return redirect(url_for('dashboard'))
    else:
        flash('Wrong username or password!')
        return redirect('/login')



@app.route('/new-user', methods=["GET", "POST"])
def register_user():
    """Create new user"""

    if request.method == "GET":
        return render_template('new-user.html')

    email = request.form.get("email")
    password = request.form.get("password")  # Capture the password correctly
    username = request.form.get("username") 
    fname = request.form.get("first_name")  
    lname = request.form.get("last_name")
    day_start_time = request.form.get("day_start_time")
    day_end_time = request.form.get("day_end_time")
    search_interval_minutes = request.form.get("search_interval_minutes")

    hashed_password = argon2.hash(password)  # Hash the password

    user = crud.get_user_by_email(email)

    if user:
        flash("Cannot create an account with that email. Try again")
        return render_template('new-user.html')
    else:
        user = crud.create_user(email, 
                                hashed_password,  # Use the hashed password
                                username,
                                fname, 
                                lname, 
                                day_start_time, 
                                day_end_time, 
                                search_interval_minutes)
        db.session.add(user)
        db.session.commit()
        flash("Welcome! Please log in.")
        return redirect('/')



@app.route('/dashboard')
def dashboard():
    # Check if the user is authenticated
    if 'current_user' not in session:
        flash("Please log in to access the dashboard.")
        return redirect('/')

    username = session['current_user']

    # Retrieve user by username
    user = crud.get_user_by_username(username)

    # Check if the user exists
    if user is None:
        flash("User not found.")
        return redirect('/')

    # Pass the user data to the template
    return render_template('dashboard.html', user=user)


@app.route('/create-event', methods=["POST", "GET"])
def create_event():
    """Create new event"""

    if request.method == "GET":
        return render_template('create-event.html')

    # Assuming you have the current user's username in the session
    username = session['current_user']
    user = crud.get_user_by_username(username)

    title = request.form.get("title")
    description = request.form.get("description")
    start_time_str = request.form.get("start_time")
    end_time_str = request.form.get("end_time")
    created_on = datetime.now()
    updated_on = datetime.now()
    deleted_on = None

    # Combine the current date with the provided time
    start_time = datetime.combine(datetime.today(), datetime.strptime(start_time_str, "%H:%M").time())
    end_time = datetime.combine(datetime.today(), datetime.strptime(end_time_str, "%H:%M").time())

    # Use the user instance when creating the event
    event = crud.create_event(user, title, description, start_time, end_time, created_on, updated_on, deleted_on)

    db.session.add(event)
    db.session.commit()
    flash("Success! Event added.")
    return redirect('/dashboard')




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)