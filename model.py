"""Models for simple calendar app."""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def connect_to_db(flask_app, db_uri="postgresql:///agenda", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

class User(db.Model):
    """A user"""
    
    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String)
    email = db.Column(db.String(40), unique=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    day_start_time = db.Column(db.Time)
    day_end_time = db.Column(db.Time)
    search_interval_minutes = db.Column(db.Integer, default=30)

    events = db.relationship('Event', back_populates='user')

    def __repr__(self):
        return f'<User {self.fname} {self.lname} | user_id = {self.user_id} | email = {self.email}>'
    
class Event(db.Model):
    """An event user schedules"""

    __tablename__ = 'events'

    event_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'))
    title = db.Column(db.String)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)
    deleted_on = db.Column(db.DateTime)

    user = db.relationship('User', back_populates='events')
    recurring = db.relationship('RecurringPattern', uselist=False, back_populates='event')
    notifications = db.relationship('Notification', back_populates='event')

    def __repr__(self):
        return f'<Event: {self.title} | event_id = {self.event_id} | Scheduled on {self.start_time} by {self.users.username}>'
    
class Notification(db.Model):
    """Event reminders a user sets up"""

    __tablename__ = 'notifications'

    notification_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    event_id = db.Column(db.Integer, 
                        db.ForeignKey('events.event_id'))
    notification_type = db.Column(db.String)
    notification_time_minutes = db.Column(db.Integer)
    notification_time_days = db.Column(db.Integer)

    event = db.relationship('Event', back_populates='notifications')

    def __repr__(self):
        return f'<Notification {self.notification_id} for notification_type = {self.notification_type}>'

    
class RecurringPattern(db.Model):
    """Recurrence patterns for recurring events"""

    __tablename__ = 'recurring_patterns'

    event_id = db.Column(db.Integer, 
                        db.ForeignKey('events.event_id'),
                        primary_key=True)
    name = db.Column(db.String(40))
    recurrence_type = db.Column(db.String)
    recurrence_interval = db.Column(db.String)
    recurrence_days_of_week = db.Column(db.String)

    event = db.relationship('Event', uselist=False, back_populates='recurring')

    def __repr__(self):
        return f'<RecurringPattern {self.name}>'

if __name__ == "__main__":
    from server import app

    connect_to_db(app)