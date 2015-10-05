from app import app,db
from models import User

db.create_all()

db.session.add(User('kyle','password'))

db.session.commit()