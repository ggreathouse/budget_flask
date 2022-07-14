from flask import Flask, session
from config import Config
from .authentication.routes import auth
from .api.routes import api
from .models import db as root_db, login_manager, ma
from budget_inventory.helpers import JSONEncoder

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_session import Session
import os



app = Flask(__name__)
app.secret_key = os.urandom(24)

app.register_blueprint(auth)
app.register_blueprint(api)

app.config.from_object(Config)
app.config.update(SECRET_KEY=os.urandom(24))


server_session = Session(app)

root_db.init_app(app)
migrate = Migrate(app, root_db)

login_manager.init_app(app)
login_manager.login_view = 'auth.signin' #specify what page to load for nonauthenticated users

ma.init_app(app)

app.json_encoder = JSONEncoder

CORS(app)

