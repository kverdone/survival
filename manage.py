from flask.ext.script import Manager
from survival import app


manager = Manager(app)
manager.run()