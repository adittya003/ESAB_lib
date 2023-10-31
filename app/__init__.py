from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

from . import routes

from . import models
