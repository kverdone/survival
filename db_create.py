from app import app,db,bcrypt
from models import User

db.create_all()

db.session.add(User('kyle', 'password', True))
db.session.add(User('test', 'test', False))

db.session.commit()