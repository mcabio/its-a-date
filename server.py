"""Server for calendar app."""

from flask import (Flask, jsonify, render_template, request, abort, flash, session,
                   redirect, url_for)
import requests
from werkzeug.security import check_password_hash
from passlib.hash import argon2
from model import connect_to_db, db, Event, User
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
    
@app.route('/user-preferences', methods=["GET"])
def user_preferences():
    # Get user_id from the session
    user_id = session.get('user_id')

    if not user_id:
        flash("Please log in to access the dashboard.")
        return redirect('/')

    # Query the database to get user preferences based on user_id
    user_preferences = crud.get_user_by_id(user_id)

    if not user_preferences:
        return jsonify({'error': 'User not found'}), 404

    # Extract relevant information
    user_info = {
        'user_id': user_preferences.user_id,
        'day_start_time': user_preferences.day_start_time.strftime('%H:%M:%S') if user_preferences.day_start_time else None,
        'day_end_time': user_preferences.day_end_time.strftime('%H:%M:%S') if user_preferences.day_end_time else None
        # Add other user-specific information as needed
    }

    user_data = {'user_preferences': user_info}

    return jsonify(user_data)



@app.route('/edit-user/<int:user_id>', methods=["GET", "POST"])
def edit_user(user_id):
    """Edit user"""
    print("Executing edit_user route")
    if request.method == "GET":
        user = crud.get_user_by_id(user_id)
        return render_template('edit-user.html', user=user)

    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")
    day_start_time = request.form.get("day_start_time")
    day_end_time = request.form.get("day_end_time")

    user = crud.get_user_by_id(user_id)

    if not user:
        flash('Old password incorrect, please try again.')
        return render_template('edit-user.html')
    
    else: 
        if user.password.startswith('$argon2'):
            # If the password is already hashed with Argon2, verify it
            if not argon2.verify(old_password, user.password):
                flash("Old password is incorrect. Please try again.")
                return render_template('edit-user.html', user=user)


    # Update user preferences
    user.password = argon2.hash(new_password)
    user.day_start_time = day_start_time
    user.day_end_time = day_end_time

    db.session.commit()

    if 'current_user' in session:
        # Clear session data
        session.pop('current_user', None)
        session.pop('user_id', None)
        flash("Preferences updated successfully! Please log in with the new password.")
    else:
        flash('You are not currently logged in.')

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


@app.route('/my-events', methods=["GET", "POST"])
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
                "month": event.start_date.strftime('%B'),
                "start_date": event.start_date.strftime('%m-%d-%y'),
                "start_time": event.start_time.strftime('%I:%M %p') if event.start_time else None,
                "end_date": event.end_date.strftime('%m-%d-%y'),
                "end_time": event.end_time.strftime('%I:%M %p') if event.end_time else None,
            })

    except Exception as e:
        print("Error:", str(e))
        # return jsonify({"error": str(e)}), 500

    return render_template('my-events.html', events_data=events_data)





@app.route('/create-event', methods=["POST", "GET"])
def create_event():
    """Create new event"""
    if 'current_user' not in session:
        flash("Please log in to schedule events.")
        return redirect('/')

    username = session['current_user']
    user = crud.get_user_by_username(username)

    if request.method == "GET":
        return render_template('create-event.html')

    username = session['current_user']
    user = crud.get_user_by_username(username)

    title = request.form.get("title")
    description = request.form.get("description")
    start_date_str = request.form.get("start_date")
    start_time_str = request.form.get("start_time")
    end_date_str = request.form.get("end_date")
    end_time_str = request.form.get("end_time")
    created_on = datetime.now()
    updated_on = datetime.now()
    deleted_on = None

    # Convert date string to datetime object
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    # this will combine the date and the time to create a start time and end time
    start_time = datetime.combine(start_date, datetime.strptime(start_time_str, "%H:%M").time())
    end_time = datetime.combine(end_date, datetime.strptime(end_time_str, "%H:%M").time())

    event = crud.create_event(user, title, description, start_date, start_time, end_date, end_time, created_on, updated_on, deleted_on)

    # This will prepare the data for the json file.
    response_data = {
        "event_id": event.event_id,
        "title": event.title,
        "description": event.description,
        "start_date": event.start_date,
        "start_time": event.start_time.isoformat(),
        "end_date": event.end_date,
        "end_time": event.end_time.isoformat(),
        # "created_on": event.created_on.isoformat(),
        # "updated_on": event.updated_on.isoformat() if event.updated_on else None,
        # "deleted_on": event.deleted_on.isoformat() if event.deleted_on else None,
    }

    db.session.add(event)
    db.session.commit()
    flash("Success! Event added.")
    
    return redirect('/dashboard')

@app.route('/api/event', methods=["GET"])
def publish_event():
    """Publish events onto the calendar for the user in session."""
    
    # Get user_id from the session
    user_id = session.get('user_id')


    if user_id is None:
        return jsonify({'error': 'User not logged in'}), 401

    # Get the start and end dates from the request parameters
    start_str = request.args.get('start')
    end_str = request.args.get('end')

    if start_str is None or end_str is None:
        return jsonify({'error': 'Missing start or end parameter'}), 400

    try:
        month_start = datetime.fromisoformat(start_str)
        month_end = datetime.fromisoformat(end_str)
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    # Query the database for events within the specified start and end dates and user_id
    events = Event.query.filter(
        Event.user_id == user_id,
        Event.start_date.between(month_start.date(), month_end.date()),
        Event.deleted_on.is_(None)
    ).all()

    # Convert events to a list of dictionaries containing the required information
    events_data = []
    for event in events:
        events_data.append({
            'event_id': event.event_id,
            'title': event.title,
            'description': event.description,
            'start_date': event.start_date.strftime('%Y-%m-%d'),
            'start_time': event.start_time.strftime('%H:%M:%S') if event.start_time else None,
            'end_date': event.end_date.strftime('%Y-%m-%d'),
            'end_time': event.end_time.strftime('%H:%M:%S') if event.end_time else None,
        })

    # Return the events data as JSON
    response_data = {'events': events_data}
    return jsonify(response_data)




# @app.route('/api/availability', methods=['GET'])
# def api_availability():

#     user_id = session['user_id']

#     start_str = request.args.get('start')
#     end_str = request.args.get('end')
#     print(f'!!!!!THIS IS THE START_STR!!!!!: {start_str}')
#     print(f'!!!!!THIS IS THE END_STR!!!!!: {end_str}')

#     month_start = datetime.fromisoformat(start_str)
#     month_end = datetime.fromisoformat(end_str)

#     # Query the database for events within the specified start and end dates and user_id
#     events = Event.query.filter(
#         Event.user_id == user_id,
#         Event.start_date.between(month_start.date(), month_end.date()),
#         Event.deleted_on.is_(None)
#     ).all()


#     # Extract the dates with events
#     dates_with_events = set()
#     for event in events:
#     # Include all dates within the range of the event
#         event_dates = [event.start_date + timedelta(n) for n in range((event.end_date - event.start_date).days + 1)]
#     dates_with_events.update(event_dates)
#     print(f'!!!!!THESE ARE THE DAYS WITH EVENTS!!!!!: {dates_with_events}')

#     # Calculate the days without events in the given month
#     days_without_events = [date for date in (month_start + timedelta(n) for n in range((month_end - month_start).days + 1))
#                            if date.date() not in dates_with_events]
#     print(f'!!!!!THESE ARE THE DAYS WITHOUT EVENTS!!!!!: {days_without_events}')

#     # Format the dates in the desired format (e.g., '2022-01-01')
#     days_available = [date.strftime('%Y-%m-%d') for date in days_without_events]
#     print(f'!!!THESE ARE DAYS AVAILABLE!!!: {days_available}')

#     available_data = {'availability': days_available}
#     print(available_data)
#     return jsonify(available_data)

@app.route('/api/availability', methods=['GET'])
def api_availability():
    user_id = session['user_id']

    start_str = request.args.get('start')
    end_str = request.args.get('end')
    print(f'!!!!!THIS IS THE START_STR!!!!!: {start_str}')
    print(f'!!!!!THIS IS THE END_STR!!!!!: {end_str}')

    month_start = datetime.fromisoformat(start_str)
    month_end = datetime.fromisoformat(end_str)

    # Query the database for events within the specified start and end dates and user_id
    events = Event.query.filter(
        Event.user_id == user_id,
        Event.start_date.between(month_start.date(), month_end.date()),
        Event.deleted_on.is_(None)
    ).all()

    # Extract the dates with events
    dates_with_events = set()
    for event in events:
        # Include all dates within the range of the event
        event_dates = [event.start_date + timedelta(n) for n in range((event.end_date - event.start_date).days + 1)]
        dates_with_events.update(event_dates)
    print(f'!!!!!THESE ARE THE DAYS WITH EVENTS!!!!!: {dates_with_events}')

    # Calculate the days without events in the given month
    days_without_events = [date for date in (month_start + timedelta(n) for n in range((month_end - month_start).days + 1))
                           if date.date() not in dates_with_events]
    print(f'!!!!!THESE ARE THE DAYS WITHOUT EVENTS!!!!!: {days_without_events}')

    # Format the dates in the desired format (e.g., '2022-01-01')
    days_available = [date.strftime('%Y-%m-%d') for date in days_without_events]
    print(f'!!!THESE ARE DAYS AVAILABLE!!!: {days_available}')

    available_data = {'availability': days_available}
    print(available_data)
    return jsonify(available_data)




@app.route('/my-availability', methods=['GET', 'POST'])
def my_availability():
    # Check if the user is authenticated
    if 'current_user' not in session:
        flash("Please log in to access the dashboard.")
        return redirect('/')

    user_id = session['user_id']  # Change session.get('user_id') to session['user_id']

    # Check if the user exists
    user = User.query.get(user_id)
    if user is None:
        flash("User not found.")
        return redirect('/')

  
    # # Pass the user, events, and available_slots data to the template
    return render_template('my-availability.html', user=user)






@app.route('/edit-event/<int:event_id>', methods=['POST', 'GET'])
def edit_event(event_id):
    """Update the event details."""
    # Retrieve the event from the database
    event = Event.query.get(event_id)

    # Check if the event exists
    if event is None:
        flash("Event not found.")
        return redirect('/my-events')

    if request.method == "GET":
        # Convert date and times to string for rendering in the form
        start_date = event.start_date.strftime('%Y-%m-%d') if event.start_date else ''
        start_time = event.start_time.strftime('%H:%M') if event.start_time else ''
        end_date = event.end_date.strftime('%Y-%m-%d') if event.end_date else ''
        end_time = event.end_time.strftime('%H:%M') if event.end_time else ''

        # Pass the event details to the template context
        return render_template('edit-event.html', event=event, start_date=start_date, start_time=start_time, end_date=end_date, end_time=end_time)
    
    # Process form submission (POST request)
    try:
        event.title = request.form.get('title')
        event.description = request.form.get('description')

        # Update start date if provided
        start_date_str = request.form.get('start_date')
        if start_date_str:
            event.start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()

        # Update start time if provided
        start_time_str = request.form.get('start_time')
        if start_time_str:
            event.start_time = datetime.strptime(start_time_str, "%H:%M").time()

        # Update end date if provided
        end_date_str = request.form.get('end_date')
        if end_date_str:
            event.end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

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
    return redirect('/my-events')


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
    return redirect('/my-events')




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