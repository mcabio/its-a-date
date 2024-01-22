"""Server for calendar app."""

from flask import (Flask, jsonify, render_template, request, abort, flash, session,
                   redirect, url_for)
from werkzeug.security import check_password_hash
from passlib.hash import argon2
from model import connect_to_db, db, Event
from datetime import date, datetime, timedelta
from sqlalchemy import func
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'secretkey'
app.jinja_env.undefined = StrictUndefined

# Connect to the database
connect_to_db(app)

@app.route('/')
def homepage():
    """View homepage"""
    return render_template('homepage.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    """Log user into the application."""
    if 'current_user' in session:
        flash('You are already logged in.')
        return redirect('/dashboard')
    
    username = request.form.get('username')
    password = request.form.get('password')

    # Retrieve user by username
    user = crud.get_user_by_username(username)

    if user:
        # If the user exists and the password is correct, store username in the session
        session['current_user'] = username
        session['user_id'] = user.user_id
        flash(f'Nice to see you again {username}!')
        return redirect(url_for('dashboard'))

    elif user and argon2.verify(password, user.password):
        # If the user exists and the password is correct, store username in the session
        session['current_user'] = username
        session['user_id'] = user.user_id
        flash(f'Logged in as {username}')
        return redirect('/dashboard')
    else:
        flash('Username or password incorrect, please try again.')
        return render_template('homepage.html')  # Render the login page instead of redirecting



@app.route('/new-user', methods=["GET", "POST"])
def register_user():
    """Create new user"""
    if request.method == "GET":
        return render_template('new-user.html')

    email = request.form.get("email")
    password = request.form.get("password")
    username = request.form.get("username") 
    fname = request.form.get("first_name")  
    lname = request.form.get("last_name")
    day_start_time = request.form.get("day_start_time")
    day_end_time = request.form.get("day_end_time")

    hashed_password = argon2.hash(password)

    user = crud.get_user_by_email(email)

    if user:
        flash("Cannot create an account with that email. Try again")
        return render_template('new-user.html')
    else:
        user = crud.create_user(email, 
                                hashed_password,
                                username,
                                fname, 
                                lname, 
                                day_start_time, 
                                day_end_time)
        
        session['current_user'] = username
        session['user_id'] = user.user_id

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
    user = crud.get_user_by_username(username)

    # Check if the user exists
    if user is None:
        flash("User not found.")
        return redirect('/')

    # Query for dashboard events (excluding deleted events)
    dashboard_events = Event.query.filter(
        Event.user_id == user.user_id,
        Event.deleted_on.is_(None)
    ).all()

    # Pass the user and events data to the template
    return render_template('dashboard.html', user=user, dashboard_events=dashboard_events)


@app.route('/your-events', methods=["GET", "POST"])
def your_events():
    # Assuming you have the user_id in the session
    user_id = session.get('user_id')
    
    if user_id is None:
        return jsonify({"error": "User not authenticated"}), 401

    try:
        events = crud.get_events_by_user_id(user_id)  

        # Filter out deleted events
        events = [event for event in events if event.deleted_on is None]

        # Convert events to a list of dictionaries
        events_data = []
        for event in events:
            events_data.append({
                "event_id": event.event_id,
                "title": event.title,
                "description": event.description,
                "month": event.date.strftime('%B'),
                "date": event.date.strftime('%m-%d-%y'),
                "start_time": event.start_time.strftime('%I:%M %p') if event.start_time else None,
                "end_time": event.end_time.strftime('%I:%M %p') if event.end_time else None,
            })

    except Exception as e:
        print("Error:", str(e))
        # return jsonify({"error": str(e)}), 500

    return render_template('your-events.html', events_data=events_data)




@app.route('/create-event', methods=["POST", "GET"])
def create_event():
    """Create new event"""
    if request.method == "GET":
        return render_template('create-event.html')

    username = session['current_user']
    user = crud.get_user_by_username(username)

    title = request.form.get("title")
    description = request.form.get("description")
    date_str = request.form.get("date")
    start_time_str = request.form.get("start_time")
    end_time_str = request.form.get("end_time")
    created_on = datetime.now()
    updated_on = datetime.now()
    deleted_on = None

    # Convert date string to datetime object
    date = datetime.strptime(date_str, "%Y-%m-%d").date()

    # this will combine the date and the time to create a start time and end time
    start_time = datetime.combine(date, datetime.strptime(start_time_str, "%H:%M").time())
    end_time = datetime.combine(date, datetime.strptime(end_time_str, "%H:%M").time())

    event = crud.create_event(user, title, description, date, start_time, end_time, created_on, updated_on, deleted_on)

    # This will prepare the datay for the json file.
    response_data = {
        "event_id": event.event_id,
        "title": event.title,
        "description": event.description,
        "date": event.date,
        "start_time": event.start_time.isoformat(),
        "end_time": event.end_time.isoformat(),
        # "created_on": event.created_on.isoformat(),
        # "updated_on": event.updated_on.isoformat() if event.updated_on else None,
        # "deleted_on": event.deleted_on.isoformat() if event.deleted_on else None,
    }

    db.session.add(event)
    db.session.commit()
    flash("Success! Event added.")
    
    return redirect('/dashboard')

@app.route('/publish-event', methods=["GET"])
def publish_event():
    """Publish events onto the calendar for the user in session."""
    
    # Get user_id from the session
    user_id = session.get('user_id')

    if user_id is None:
        return jsonify({'error': 'User not logged in'}), 401

    # Get the start and end dates from the request parameters
    start_str = request.args.get('start')
    end_str = request.args.get('end')

    print(f"Received request. Start: {start_str}, End: {end_str}")

    if start_str is None or end_str is None:
        return abort(400, 'Missing start or end parameter')  # Bad Request

    try:
        start_date = datetime.fromisoformat(start_str)
        end_date = datetime.fromisoformat(end_str)
    except ValueError:
        return abort(400, 'Invalid date format')  # Bad Request

    # Query the database for events within the specified start and end dates and user_id
    events = Event.query.filter(
        Event.user_id == user_id,
        Event.date.between(start_date.date(), end_date.date()),
        Event.deleted_on == None
    ).all()

    # events = [event for event in events if event.deleted_on is None]

    # Convert events to a list of dictionaries containing the required information
    events_data = []
    for event in events:
        events_data.append({
            'title': event.title,
            'description': event.description,
            'date': event.date.strftime('%Y-%m-%d'),
            'start_time': event.start_time.strftime('%H:%M:%S') if event.start_time else None,
            'end_time': event.end_time.strftime('%H:%M:%S') if event.end_time else None,
        })

    # Return the events data as JSON
    response_data = {'events': events_data} if events_data else {'events': []}
    return jsonify(response_data)


@app.route('/edit-event/<int:event_id>', methods=['POST', 'GET'])
def edit_event(event_id):
    """Update the event details."""
    # Retrieve the event from the database
    event = Event.query.get(event_id)

    # Check if the event exists
    if event is None:
        flash("Event not found.")
        return redirect('/your-events')

    if request.method == "GET":
        # Convert date and times to string for rendering in the form
        event_date = event.date.strftime('%Y-%m-%d') if event.date else ''
        start_time = event.start_time.strftime('%H:%M') if event.start_time else ''
        end_time = event.end_time.strftime('%H:%M') if event.end_time else ''

        # Pass the event details to the template context
        return render_template('edit-event.html', event=event, event_date=event_date, start_time=start_time, end_time=end_time)
    
    # Process form submission (POST request)
    try:
        event.title = request.form.get('title')
        event.description = request.form.get('description')

        # Update date if provided
        date_str = request.form.get('date')
        if date_str:
            event.date = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Update start time if provided
        start_time_str = request.form.get('start_time')
        if start_time_str:
            event.start_time = datetime.strptime(start_time_str, "%H:%M").time()

        # Update end time if provided
        end_time_str = request.form.get('end_time')
        if end_time_str:
            event.end_time = datetime.strptime(end_time_str, "%H:%M").time()
    except ValueError as e:
        flash(f"Error updating event: {str(e)}")
        return redirect('/your-events')

    # Update the updated_on field with the current date and time
    event.updated_on = datetime.now()

    # Save the changes to the database
    db.session.commit()

    flash('Event updated successfully.')
    return redirect('/your-events')


@app.route('/delete-event/<int:event_id>', methods=['POST', 'GET'])
def delete_event(event_id):
    """Delete the event."""
    # Retrieve the event from the database
    event = Event.query.get(event_id)

    # Check if the event exists
    if event is None:
        flash("Event not found.")
        return redirect('/your-events')

    # Update the deleted_on field with the current date and time
    event.updated_on = datetime.now()
    event.deleted_on = datetime.now()

    # Save the changes to the database
    db.session.commit()

    flash('Event deleted successfully.')
    return redirect('/your-events')




@app.route('/logout', methods=['GET'])
def logout():
    """Logout user."""
    if 'current_user' in session:
        # Clear session data
        session.pop('current_user', None)
        session.pop('user_id', None)
        flash('You have been logged out.')
    else:
        flash('You are not currently logged in.')

    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)