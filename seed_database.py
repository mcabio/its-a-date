import os
import json
from datetime import datetime

import crud 
import model 
import server

import crud
import server

os.system("dropdb agenda")
os.system("createdb agenda")

model.connect_to_db(server.app, db_uri='postgresql:///agenda')
model.db.create_all()

def seed_users_and_events():
    """Seed the database with users and events."""
    
    # Create users
    user1 = crud.create_user(username='firstuser', 
                                 password='user1', 
                                 email='user1@example.com',
                                 fname='User', 
                                 lname='One',
                                 day_start_time='8:30:00',
                                 day_end_time='20:30:00')
    user2 = crud.create_user(username='twouser', 
                                  password='user2',
                                  email='user2@example.com', 
                                  fname='User', 
                                  lname='Two',
                                  day_start_time='7:30:00',
                                  day_end_time='23:30:00')
    user3 = crud.create_user(username='thethird', 
                             password='user3', 
                             email='user3@example.com',
                             fname='User', 
                             lname='Three',
                             day_start_time='6:00:00',
                             day_end_time='22:30:00')
    user4 = crud.create_user(email='user4@example.com', 
                                  password='user4', 
                                  username='lucky4', 
                                  fname='User', 
                                  lname='Four',
                                  day_start_time='9:30:00',
                                  day_end_time='23:30:00')
    
    created_on = datetime.now()
    updated_on = None  # Set to None initially
    deleted_on = None  # Set to None initially

    # Create events for user1
    event1 = crud.create_event(user1, 
                               title='The very first', 
                               description='Its here',
                               start_time=datetime(2024, 1, 1, 10, 0), 
                               end_time=datetime(2024, 1, 1, 12, 0),
                               created_on=created_on,
                               updated_on=updated_on,
                               deleted_on=deleted_on)

    event2 = crud.create_event(user2, title='When two becomes 1', 
                               description='Spice girls',
                               start_time=datetime(2024, 2, 14, 14, 0), 
                               end_time=datetime(2024, 2, 14, 16, 0),
                               created_on=created_on,
                               updated_on=updated_on,
                               deleted_on=deleted_on)

    # Create events for user2
    event3 = crud.create_event(user3, title='Third times a charm', 
                               description='Lucky shiz',
                               start_time=datetime(2024, 4, 20, 15, 0), 
                               end_time=datetime(2024, 4, 20, 18, 0),
                               created_on=created_on,
                               updated_on=updated_on,
                               deleted_on=deleted_on)

    event4 = crud.create_event(user3, title='May the 4th be with you', 
                               description='The force is with you',
                               start_time=datetime(2024, 2, 8, 14, 0), 
                               end_time=datetime(2024, 2, 8, 16, 0),
                               created_on=created_on,
                               updated_on=updated_on,
                               deleted_on=deleted_on)
    event5 = crud.create_event(user4, title='I plead the 5th', 
                               description='Filthy fifth',
                               start_time=datetime(2024, 4, 20, 16, 0), 
                               end_time=datetime(2024, 4, 20, 20, 0),
                               created_on=created_on,
                               updated_on=updated_on,
                               deleted_on=deleted_on)
    event6 = crud.create_event(user4, title='Six on the beach', 
                               description='Mixed drinx',
                               start_time=datetime(2024, 5, 5, 20, 0), 
                               end_time=datetime(2024, 5, 5, 23, 0),
                               created_on=created_on,
                               updated_on=updated_on,
                               deleted_on=deleted_on)
    event7 = crud.create_event(user4, title='Seventh heaven', 
                               description='Clovers and horseshoes',
                               start_time=datetime(2024, 6, 21, 9, 0), 
                               end_time=datetime(2024, 6, 21, 13, 0),
                               created_on=created_on,
                               updated_on=updated_on,
                               deleted_on=deleted_on)
    event8 = crud.create_event(user3, title='Crazy 8s', 
                               description='3.5 grams',
                               start_time=datetime(2024, 11, 8, 11, 0), 
                               end_time=datetime(2024, 11, 8, 12, 0),
                               created_on=created_on,
                               updated_on=updated_on,
                               deleted_on=deleted_on)
    event9 = crud.create_event(user2, title='Cloud 9', 
                               description='Description 4',
                               start_time=datetime(2024, 10, 27, 9, 0), 
                               end_time=datetime(2024, 10, 27, 15, 0),
                               created_on=created_on,
                               updated_on=updated_on,
                               deleted_on=deleted_on)
    event10 = crud.create_event(user2, title='Rin ten ten', 
                                description='A detective',
                               start_time=datetime(2024, 10, 31, 14, 0), 
                               end_time=datetime(2024, 10, 31, 16, 0),
                               created_on=created_on,
                               updated_on=updated_on,
                               deleted_on=deleted_on)
    event11 = crud.create_event(user1, title='Ill EVEN', 
                                description='Even it out',
                               start_time=datetime(2024, 7, 31, 14, 0), 
                               end_time=datetime(2024, 7, 31, 16, 0),
                               created_on=created_on,
                               updated_on=updated_on,
                               deleted_on=deleted_on)
    event12 = crud.create_event(user4, title='Bakers dozen', 
                                description='Eeesshhhh',
                               start_time=datetime(2024, 8, 13, 14, 0), 
                               end_time=datetime(2024, 8, 13, 16, 0),
                               created_on=created_on,
                               updated_on=updated_on,
                               deleted_on=deleted_on)

    model.db.session.add_all([user1, 
                              user2, 
                              user3, 
                              user4, 
                              event1, 
                              event2, 
                              event3, 
                              event4, 
                              event5, 
                              event6, 
                              event7, 
                              event8, 
                              event9, 
                              event10, 
                              event11, 
                              event12])
    model.db.session.commit()

if __name__ == '__main__':
    seed_users_and_events()
