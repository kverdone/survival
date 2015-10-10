from app import app,db,bcrypt
from models import User, Game, Team

db.drop_all()
db.create_all()

db.session.add(User(username='admin', password='pass', admin=True, verified=True))
db.session.add(User(username='verified', password='pass', admin=False, verified=True))
db.session.add(User(username='unverified', password='pass', admin=False, verified=False))

db.session.add(Game(week_number=1, active=True, home_team_id=1, away_team_id=2, time_slot='TN'))
db.session.add(Game(week_number=1, active=True, home_team_id=3, away_team_id=4, time_slot='SM'))
db.session.add(Game(week_number=1, active=True, home_team_id=5, away_team_id=6, time_slot='SM'))
db.session.add(Game(week_number=1, active=True, home_team_id=7, away_team_id=8, time_slot='SA'))
db.session.add(Game(week_number=1, active=True, home_team_id=9, away_team_id=10, time_slot='SA'))
db.session.add(Game(week_number=1, active=True, home_team_id=11, away_team_id=12, time_slot='SA'))
db.session.add(Game(week_number=1, active=True, home_team_id=13, away_team_id=14, time_slot='SN'))

teams = [
        ['HOU', 'Houston', 'Texans'],
        ['IND', 'Indianapolis', 'Colts'],
        ['WAS', 'Washington', 'Redskins'],
        ['ATL', 'Atlanta', 'Falcons'],
        ['CLE', 'Cleveland', 'Browns'],
        ['BAL', 'Baltimore', 'Ravens'],
        ['SEA', 'Seattle', 'Seahawks'],
        ['CIN', 'Cincinatti', 'Bengals'],
        ['STL', 'St. Louis', 'Rams'],
        ['GB', 'Green Bay', 'Packers'],
        ['CHI', 'Chicago', 'Bears'],
        ['KC', 'Kansas City', 'Chiefs'],
        ['NO', 'New Orleans', 'Saints'],
        ['PHI', 'Philadelphia', 'Eagles'],
        ['JAX', 'Jacksonville', 'Jaguar'],
        ['TB', 'Tampa Bay', 'Buccaneers'],
        ['BUF', 'Buffalo', 'Bills'],
        ['TEN', 'Tennessee', 'Titans'],
        ['ARI', 'Arizona', 'Cardinals'],
        ['DET', 'Detroit', 'Lions'],
        ['NE', 'New England', 'Patriots'],
        ['DAL', 'Dallas', 'Cowboys'],
        ['DEN', 'Denver', 'Broncos'],
        ['OAK', 'Oakland', 'Raiders'],
        ['SF', 'San Francisco', '49ers'],
        ['NYG', 'New York', 'Giants'],
        ['PIT', 'Pittsburgh', 'Steelers'],
        ['SD', 'San Diego', 'Chargers'],
        ['CAR', 'Carolina', 'Panthers'],
        ['MIA', 'Miami', 'Dolphins'],
        ['MIN', 'Minnesota', 'Vikings'],
        ['NYJ', 'New York', 'Jets']
        ]

for team in teams:
    db.session.add(Team(team[0], team[1], team[2]))

db.session.commit()