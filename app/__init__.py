from flask import Flask
from flask_cors import CORS
from app.Database.db import Database



app = Flask(__name__)
CORS(app, resources=r'/api/*')
from .views import auth
from .views import redflag
from .views import intervention

database = Database()
database.create_tables()