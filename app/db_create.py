# db_create.py

from views import db
from models import Domain
from datetime import date

# create teh database and the db table
db.create_all()


db.session.add(Domain("Some domain name"))

db.session.commit()