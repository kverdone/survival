from wtforms import Form, TextField, PasswordField, RadioField
from wtforms.validators import InputRequired

class LoginForm(Form):
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])

class TNForm(Form):
    tn_games = RadioField()