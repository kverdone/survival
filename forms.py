from wtforms import Form, TextField, PasswordField
from wtforms.validators import InputRequired

class LoginForm(Form):
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])