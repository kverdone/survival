from app import app,db,bcrypt
from models import User

db.create_all()

db.session.add(User('kyle', 'password', True, True))
db.session.add(User('test1', 'test', False, True))
db.session.add(User('test2', 'test', False, False))

db.session.commit()