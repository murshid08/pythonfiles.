from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

path = os.path.dirname( os.path.realpath(__file__) )
database_path = os.path.join(path, '../mydb.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_path
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category ='info'

from source import routes