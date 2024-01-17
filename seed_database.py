import os
import json
from datetime import datetime

import crud 
import model 
import server

os.system("dropdb agenda")
os.system("createdb agenda")

model.connect_to_db(server.app)
model.db.create_all()




# model.db.session.add_all()
# model.db.session.commit()