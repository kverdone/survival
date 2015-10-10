from app import db, bcrypt
#from flask_wtf import Form
from datetime import datetime


class User(db.Model):
    '''

    '''
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    verified = db.Column(db.Boolean, nullable=False)
    '''email = db.Column(db.String, nullable=False, unique=True)
    created_date = db.Column(db.DateTime, nullable=False)
    players = db.relationship('Player', backref='user')'''

    def __init__(self, username=None, password=None, admin=False, verified=False):
        self.username = username
        #self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.admin = admin
        self.verified = verified

    def __repr__(self):
        return '<User #{}>\t{}\t{}'.format(self.id, self.username, self.admin)

    def is_admin(self):
        return self.admin

    def is_verified(self):
        return self.verified

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)


class Season(db.Model):
    __tablename__ = 'seasons'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    season = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    '''players = db.relationship('Player', backref='user')'''

    def __init__(self, name=None, season=None, active=False):
        self.name = name
        self.season = season
        self.active = active

    def __repr__(self):
        return '<Season #{}>\t{}\t{}\t{}'.format(self.id, self.name, self.season, self.active)

    def is_active(self):
        return self.active


class Week(db.Model):
    __tablename__ = 'weeks'

    id = db.Column(db.Integer, primary_key=True)
    week_number = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    '''players = db.relationship('Player', backref='user')'''

    def __init__(self, week_number=None, active=False):
        self.week_number = week_number
        self.active = active

    def __repr__(self):
        return '<Season #{}>\t{}\t{}\t{}'.format(self.id, self.week_number, self.season, self.active)

    def is_active(self):
        return self.active


class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    '''week_id = db.relationship...'''
    week_number = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=False)
    home_team_id = db.Column(db.Integer, nullable=False)
    away_team_id = db.Column(db.Integer, nullable=False)
    home_team_score = db.Column(db.Integer, default=None)
    away_team_score = db.Column(db.Integer, default=None)
    winner_id = db.Column(db.Integer, default=None)
    time_slot = db.Column(db.String, nullable=False)
    '''players = db.relationship('Player', backref='user')'''

    def __init__(self, week_number=None, active=False, home_team_id=None, away_team_id=None, time_slot=None):
        self.week_number = week_number
        self.active = active
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.time_slot = time_slot

    def __repr__(self):
        #return str([self.id, self.week_number, self.active, self.home_team_id, self.away_team_id, self.time_slot])
        return str(vars(self))

    def is_active(self):
        return self.active

    def get_winner(self):
        if self.home_team_score and self.away_team_score:
            if self.home_team_score == self.away_team_score:
                self.winner_id = -1

            if self.home_team_score > self.away_team_score:
                self.winner_id = self.home_team_id

            else:
                self.winner_id = self.away_team_id

            return self.winner_id

        else:
            return None


class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    city_short = db.Column(db.String, nullable=False)
    city_long = db.Column(db.String, nullable=False)
    team_long = db.Column(db.String, nullable=False)

    def __init__(self, city_short, city_long, team_long):
        self.city_short = city_short
        self.city_long = city_long
        self.team_long = team_long

    def __repr__(self):
        #return '{} - {} {} {}'.format(id, self.city_short, self.city_long, self.team_long)
        return '{} {}'.format(self.city_long, self.team_long)






