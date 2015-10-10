from flask import Flask, render_template, redirect, url_for, g, request, flash

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager, current_user, login_user, logout_user, login_required
from flask_admin import Admin, expose, AdminIndexView
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView

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
# MODELS/VIEW CLASSES
###############################
class MyModelView(ModelView):

    def is_accessible(self):
        return current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('index', next=request.url))

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_admin():
            flash('You are not an admin.')
            return redirect(url_for('index')) 
        #return super(MyAdminIndexView, self).index()
        return self.render('admin_index.html')

admin = Admin(app, name='Survival Admin', index_view=MyAdminIndexView(), template_mode='bootstrap3')
admin.add_view(MyModelView(User, db.session))


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
            flash('You are not an admin.')
            return redirect(url_for('index')) 
    return wrap

def verification_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_verified():
            return f(*args, **kwargs)
        else:
            flash('You are not verified.')
            return redirect(url_for('index')) 
    return wrap

###############################
# ROUTES
###############################
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello {}</h1>'.format(name) + str(current_user)

@app.route('/week/<int:week_id>')
@login_required
@verification_required
def week(week_id):
    return render_template('week.html')

@app.route('/my_admin')
@login_required
@admin_required
def my_admin():
    return render_template('my_admin.html')

@app.route('/my_admin/users')
@login_required
@admin_required
def my_admin_users():
    users = User.query.all()
    return render_template('my_admin_users.html', users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.')
        return redirect(url_for('index'))

    form = LoginForm(request.form)

    next_page = request.values.get('next','/')

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

@app.route('/picks/<int:week_number>/tn')
@login_required
@verification_required
def picks_tn(week_number):
    
    tn = Game.query.filter(Game.week_number == week_number).filter(Game.time_slot == 'SM').all()

    tn_form = TNForm()
    tn_form.tn_games.choices = []
    tn_games = []

    for game in tn:
        home_team = Team.query.filter(Team.id == game.home_team_id).all()[0]
        away_team = Team.query.filter(Team.id == game.away_team_id).all()[0]
        tn_form.tn_games.choices.append((game.home_team_id, home_team))
        tn_form.tn_games.choices.append((game.away_team_id, away_team))
        tn_games.append((game.home_team_id, home_team, home_team.city_short))
        tn_games.append((game.away_team_id, away_team, away_team.city_short))

    print tn_form.tn_games.choices

    for game in tn_form.tn_games:
        print game

    print tn_games


    '''tn_teams = set(x.home_team_id for x in tn) | set(x.away_team_id for x in tn)
    #print tn_teams
    tn_form = PickForm()
    tn_form.games.choices = [(x,x) for x in tn_teams]
    tn_form.games.name = 'tn'''  

    return render_template('picks_tn.html', tn_form=tn_form, week_number=week_number, tn_games=tn_games)


@app.route('/picks/<int:week_number>')
@login_required
@verification_required
def picks(week_number):
    
    tn = Game.query.filter(Game.week_number == week_number).all()

    slot_map = {
                'TN': 'Thursday Night Game',
                'SM': 'Sunday Morning Games',
                'SA': 'Sunday Afternoon Games',
                'SN': 'Sunday Night Games',
                'MN': 'Monday Night Games'
            }

    games = {
                'TN': [], 
                'SM': [],
                'SA': [],
                'SN': [],
                'MN': []
            }

    for game in tn:
        time_slot = game.time_slot
        home_team = Team.query.filter(Team.id == game.home_team_id).all()[0]
        away_team = Team.query.filter(Team.id == game.away_team_id).all()[0]
        
        to_add = {
                    'away_id': away_team.id,
                    'away_short': away_team.city_short,
                    'away_name': away_team,
                    'home_id': home_team.id,
                    'home_short': home_team.city_short,
                    'home_name': home_team,
                    'game_id': game.id,
                    'slot': slot_map[time_slot]
                }

        games[time_slot].append(to_add)
    '''
        games[time_slot].append(to_add)
        tn_games.append((game.home_team_id, home_team, home_team.city_short))
        tn_games.append((game.away_team_id, away_team, away_team.city_short))
    '''
    

    return render_template('picks.html', week_number=week_number, games=games)



if __name__ == '__main__':
    app.run()