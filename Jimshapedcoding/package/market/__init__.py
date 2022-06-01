from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt # for password encryption pip install flask_bcrypt
from flask_login import LoginManager # this is our entire app login manager so pip install login_manager
# Bcrypt from flask_crypt uses to convert plain text password to encrypted hash password.
# so instead of storing plain text password we can save as encrypted hash password.


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db' # Uniform resource identifier which is not a url,
app.config['SECRET_KEY'] = "d1c7462821e4912d62ff0231" # secret key is a another secret layer in forms for clients privacy  when they register with passwords to keep secret
db = SQLAlchemy(app)   
bcrypt = Bcrypt(app)
Login_manager = LoginManager(app)
Login_manager.login_view = 'login_page' # To the login required decorator addressing the page to redirect loginpage with these flask built-in functiions of Login_manager
Login_manager.login_message_category = 'info' # This turns the login flash message "please login to access" to blue color 
from market import routes



# __init__ is a python special file where it is known as initialization of our flask variables or objects 
# lines of  code before loading others. it is the start and  initial flask application file where we can run
#  this whole   package on run.py file just simply importing  app from this package.
# Note: any regular python considered package is included into this special python file only before it loads 
# what it wants to import to the file then start initilization and make the directory a package.