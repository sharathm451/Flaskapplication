from market import db,Login_manager
from market import bcrypt
from flask_login import UserMixin # This will eases by importing UserMixin instead of some hard coded methods like is_authenticated, get_active ...in User loader class, 

# LoginManager.user_loader callback is to make our flask application to understand if we navigate from different pages to 
# when we are authenticated then each refresh there is a different request session that the flask application has to understand if the user is logged in or not
# so this is why we use this decorated login_manager needs to be executed every time we load some different pages
@Login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 
 

class User(db.Model, UserMixin): # UserMixin is an additional property methods containing one like is_authenticated, is_active, get_id  to inherit from class UserMixin
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True) # backref gives the owner in search of item owner
# lazy is set true because if not set true sqlalchemy will not grab all items/objects in one shot.
    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"
    @property
    def password(self):
        return self.password

    @password.setter # its a oops setter method.
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password) #it checks converted existing passwordhash and given password in loginform and returns

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30))
    price = db.Column(db.Integer(), nullable=False,unique=True)
    barcode = db.Column(db.String(length=12),nullable=False,unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
#   foreign key is used to make relational database with one  common key
    def __repr__(self):  # dunder magical method 
        return f'Item {self.name}'  # This function is mainly to customize the viewing your items as Item iphone 10 
#   instead of Item 1 Item 2                                     



# commands in python shell
# cmd python
# cmd from market.models import db   # as we made models file in market package
# cmd db.drop_all()  # this is an additional option to deleta all data in database 
# cmd db.create_all()
# cmd  from market.models import User,Item
# u1 = User(username='jsc',password_hash='524613',email_address='jsc@jsc.com')
# import os 
# os.system('cls') # to clean terminal
# db.session.add(u1)
# db.session.commit()
# User.query.all()
# i1 = Item(name='iphone 10',description='descr',barcode='455611',price=8000)
# db.session.add(i1)
# db.session.commit()
# i2 = Item(name='Laptop',description='description',barcode='45885611',price=1000)
# db.session.add(i2)
# db.session.commit() 
# Item.query.all()


# item1 = Item.query.filter_by(name='iphone 10') # it shows memory address
# item1 = Item.query.filter_by(name='iphone 10').first()
# item1 # it show the filtered Item
# item1.owner # it doesn't show any result because no relational finding command it is 

# db.session.rollback()  # this one rollback if you mistakenly commits anything

# item1.owner = User.query.filter_by(username='jsc').first().id
# db.session.add(item1)
# db.session.commit()
# item1.owner  # now shows the owner

# i = Item.query.filter_by(name='Iphone 10').first()
# i.owned_user  # now it shows the owner of the item with backref 



