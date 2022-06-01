from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db' # Uniform resource identifier which is not a url,
#                                                                #  it's a identifier of our database
# The above statement is a dictionary that is going to acccept some new key values, the conventional way to add key
# is give name as  SQLALCHEMY_DATABASE_URI to find out the database which is given in sqlite uri 
db = SQLAlchemy(app)                                         

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30))
    price = db.Column(db.Integer(), nullable=False,unique=True)
    barcode = db.Column(db.String(length=12),nullable=False,unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)

    def __repr__(self): 
        return f'Item {self.name}'


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('inheritanceHome.html')

@app.route('/market')
def market_page():
    items = Item.query.all()
#    items = [
#        {'id':1, 'name':'Phone', 'barcode':'89324158', 'Price':500},
#        {'id':2, 'name':'Laptop', 'barcode':'5468213', 'Price':900},
#        {'id':3, 'name':'Keyboard', 'barcode':'4781253', 'Price':150}
#    ]
    return render_template('inheritanceMarket.html', items = items)



if __name__=="__main__":
    app.run(debug=True)



# Sqlite3 commands 
# once after writing this code we can execute this codes to create database and other operations
# In the same directory of this python file start executing following commands


# cmd - python
# cmd - from market import db    it is basically  to take several actions within that db created previously in py file
# cmd - db.create_all()      it create database file in this project directory
# cmd - from market import Item
# cmd item1 = Item(name='Iphone 10', price=500, barcode='564281', description='desc') # id with primary key automatically takes care of 1,2,...
# cmd db.session.add(item1)
# cmd db.session.commit()  # it commits the saving info in our database
# cmd Item.query.all()
# cmd item2 = Item(name='Laptop',price=600,description='description',barcode='32546712') 
# cmd db.session.add(item2)
# cmd db.session.commit()
# cmd Item.query.all() 
# exit()
# cmd from market import db
# cmd from market import Item
# cmd Item.query.all()  # you can see differnce seeing items with  objects
# for item in Item.query.all(): # returns all of our objects in for loop
#       item.name
#       item.price
#       item.description
#       item.id
#       item.barcode
# cmd os.system('cls')
# cmd Item.query.filter_by(price=500) # This only return memory address as boolean answer
# cmd for item in Item.query.filter_by(price=500): # To get the filter which matches price=500 display it's name of it by iterating multiple matches.
#           item.name







