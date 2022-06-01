from market import app
from flask import render_template, redirect, url_for,flash
from market.models import Item, User # it imports database models to run the market_page Item.query commands below 
from market.forms import RegisterForm,LoginForm
from market import db
from flask import request
from flask_login import login_user, logout_user, login_required
## Please Attention: These are the circular imports because in main __init__file  you need to import 
## flask and basic packages and this routes file as package in the __init__ file to run the application
## viceversa overhere it also necessary to import necessary packages which are in __init__ file sometimes here.
## so that is why packages plays like a saviour from the circular imports 
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('inheritanceHome.html')

@app.route('/market') 
@login_required
def market_page():
    items = Item.query.all()
#    items = [
#        {'id':1, 'name':'Phone', 'barcode':'89324158', 'Price':500},
#        {'id':2, 'name':'Laptop', 'barcode':'5468213', 'Price':900},
#        {'id':3, 'name':'Keyboard', 'barcode':'4781253', 'Price':150}
#    ]
    return render_template('inheritanceMarket.html', items = items)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if request.method == 'POST' and  form.validate_on_submit():  # it is executed only the submit button executed to ensure following validations
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data) # so here instead of password_hash if we set password setter it will generate password_hash
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create) # This is for registered users directly to enter in market page rather than login page.
        flash(f"Account created successfully! you are logged in as :{user_to_create.username}", category='success')        
        return redirect(url_for('market_page'))
    if form.errors != {}: # if there are errors from validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger') # instead of print to show errors 
    return render_template('register.html', form=form)
# in terminal we can use flash function to show it in html template/in website 
# Note: category and form.errors are added in the base.html for errors flashing for whole structure.
# NOTE: The biggest bug formed  while trying this is adding unnecessary methods like get and post at market page
# and also adding action=/market in register.html in the form post method. so please take care of adding methods only necessarily

@app.route('/login', methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(   # understand that check_password_correction's is a method from property decorator in models.py file
            attempted_password=form.password.data):
            login_user(attempted_user) # this is built-in function that exists in login user package already
            flash("Success! you are  logged in as :{attempted_user.username}", category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')


    return render_template('login.html',form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("you have been logged out!", category='info') # info gives in blue color, success gives in green color,danger gives red color
    return redirect(url_for('home_page'))




