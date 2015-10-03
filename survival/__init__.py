from flask import Flask
import os
from config import config

app = Flask(__name__)

app.config.from_object(config[os.environ.get('APP_CONFIG','default')])

import survival.views