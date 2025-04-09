from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ed05a860e6a32fd50bd383f7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:alger0101@localhost/restaurant'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

from notes import routes




