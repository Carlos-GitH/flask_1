from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

csrf = CSRFProtect(app)

bcrypt = Bcrypt(app)

from views.views_users import *
from views.views_games import *

if __name__ == '__main__':
    app.run(debug=True)