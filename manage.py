import os
from app import app, db
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from config import config

app.config.from_object(config[os.getenv('FLASK_CONFIG') or 'default'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()