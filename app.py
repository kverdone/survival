from flask import Flask, render_template, redirect, url_for, g, request, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager, current_user, login_user, logout_user, login_required
from config import config
from functools import wraps

app = Flask(__name__)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

import os
app.config.from_object(config[os.getenv('FLASK_CONFIG') or 'default'])
 
db = SQLAlchemy(app)

from models import *
from forms import *

###############################
# MODELS
###############################


###############################
# HELPER FUNCTIONS
###############################
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def get_current_user():
    g.user = current_user

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_admin():
            return f(*args, **kwargs)
        else:
            flash('You do not have permission.')
            return redirect(url_for('index')) 
    return wrap


###############################
# ROUTES
###############################

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello {}</h1>'.format(name) + str(current_user)

@app.route('/week/<int:week_id>')
@login_required
def week(week_id):
    return render_template('week.html')

@app.route('/admin')
@login_required
@admin_required
def admin():
    return render_template('admin.html')

@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.')
        return redirect(url_for('index'))

    form = LoginForm(request.form)

    next_page = request.values.get('next')

    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        password = request.form.get('password')

        '''
        try:
            User.try_login(username, password)
        except:
            flash('Invalid credentials.')
            return render_template('login.html', form=form)
        '''

        user = User.query.filter_by(username=username).first()

        '''if not user:
            user = User(username, password)
            db.session.add(user)
            db.session.commit()'''
        if user and bcrypt.check_password_hash(user.password, password):
            # can pass remember=True in login_user() function
            login_user(user)
            flash('You have logged in.', 'success')
            return redirect(next_page)

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))





if __name__ == '__main__':
    app.run()