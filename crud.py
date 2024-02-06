"""CRUD operations."""
from model import db, User, Event, Notification, RecurringPattern, connect_to_db
from sqlalchemy.exc import IntegrityError


def create_user(email, password, username, fname, lname, day_start_time, day_end_time):
    """Create and return a new user."""
    
    user = User(email=email, 
                password=password, 
                username=username, 
                fname=fname, 
                lname=lname, 
                day_start_time=day_start_time, 
                day_end_time=day_end_time)
    
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

def create_event(user, title, description, start_date, start_time, 
                 end_date, end_time, created_on, updated_on, deleted_on=None):
    """Create and return a new event"""

    event = Event(user=user, 
                  title=title, 
                  description=description, 
                  start_date=start_date,
                  start_time=start_time, 
                  end_date=end_date,
                  end_time=end_time,
                  created_on=created_on,
                  updated_on=updated_on,
                  deleted_on=deleted_on)

    db.session.add(event)
    db.session.commit()
    
    return event
    
def get_event_by_id(event_id):
    
    return Event.query.get(event_id)

def get_events_by_user_id(user_id):
    """Get events based on user_id."""
    events = Event.query.filter_by(user_id=user_id).all()
    return events


