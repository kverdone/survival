from app import db, bcrypt
#from flask_wtf import Form
from wtforms import Form, TextField, PasswordField
from wtforms.validators import InputRequired


class User(db.Model, ):
    '''

    '''
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    '''email = db.Column(db.String, nullable=False, unique=True)
    created_date = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)


    players = db.relationship('Player', backref='user')'''

    def __init__(self, username=None, password=None):
        self.username = username
        #self.email = email
        self.password = password
        #self.is_admin = is_admin

    def __repr__(self):
        return '<User #{}>\t{}\t{}'.format(self.id, self.username, self.password)

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)

class LoginForm(Form):
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])