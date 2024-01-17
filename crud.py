"""CRUD operations."""
from model import db, User, Event, Notification, RecurringPattern, connect_to_db
from sqlalchemy.exc import IntegrityError


def create_user(email, password, username, fname, lname, day_start_time, day_end_time, search_interval_minutes):
    """Create and return a new user."""
    
    user = User(email=email, 
                password=password, 
                username=username, 
                fname=fname, 
                lname=lname, 
                day_start_time=day_start_time, 
                day_end_time=day_end_time, 
                search_interval_minutes=search_interval_minutes)
    
    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        # Handle the IntegrityError, e.g., by logging or providing a flash message
        raise e

    return user


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user_by_id(user_id):
    """Return a user by user_id"""

    return User.query.get(user_id)

def get_user_by_email(email):
    """Return a user by email"""

    return User.query.filter(User.email == email).first()

def create_event(user, title, description, start_time, end_time):
    """Create and return a new event"""

    event = Event(user=user, 
                  title=title, 
                  description=description, 
                  start_time=start_time, 
                  end_time=end_time,
                  )
    
    return event
    



