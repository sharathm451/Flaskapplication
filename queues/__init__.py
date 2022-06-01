from email.message import Message
import flask
from twilio.rest import Client
from flask import Flask, request, abort
from twilio.twiml.messaging_response import MessagingResponse
from collections import deque
from flask_sqlalchemy import SQLAlchemy
import werkzeug
import ctypes
from sqlalchemy.orm import validates 
import json
from flask import  redirect, url_for,flash,jsonify,Response


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Q.db' # Uniform resource identifier which is not a url,
app.config['SECRET_KEY'] = "8c4abc4fc171319986998b93"
db = SQLAlchemy(app)   

    
class Person:
    def __init__(self, name, number):
        self.name = name
        self.number = number

class Database:
    def __init__(self):
        self.q = []                    # will add 5 objects of Person class in to this Database.q 
        self.q_dict = {}

    # Takes in a Person object and adds it to the database
    def add(self, person):
        self.q.append(person)
        self.q_dict[person.number] = person # for every Person class object iteration, the dict value is assigned to key
        person.index = len(self.q) - 1      # so then self.q_dict be like {"1":'person1',"2":'person2'...}

    def update_indices(self):
        for i in range(len(self.q)):
            person = self.q[i]
            person.index = i

    def pop_first(self):
        number = self.q[0].number    # first  person with index 0 have number '1'
        return self.remove(number)     #self.remove calls instance object of class Database  remove method that is only one database object 
                                
    def remove(self, number):  
        person = self.q_dict[number]     # person with key number 1 is person1
        print(person)  
        index = person.index             # index of that person1 is 0 which we assigned in add method 
        del self.q[index]                # deleting person1 by indexing 
        del self.q_dict[number]          # deleting person1 key number 1 
        self.update_indices()            # updating indices with remained persons
        return person                    # pop_first method redirecting here to return that removed person1

    def lookup(self, number):
        return self.q_dict[number]

    def exists(self, number):
        print (number in self.q_dict)    

def print_all(database):
    for person in database.q:
        print(person.name, person.number)

# person1 = Person("Person1", "1")
# person2 = Person("Person2", "2")

database = Database()

def validate_post(data_objects):
    if (any(s in data_objects for s in ('message', 'Message', 'MESSAGE')) or any(s in data_objects for s in ('position', 'Position', 'POSITION')) or any(s in data_objects for s in ('REMOVE', 'remove', 'Remove'))):
        return True
    else:
        return False


@app.route("/message/<phonenumber>", methods=['GET', 'POST'])
def hello_monkey(phonenumber):
#    abort(500)
    """Respond and greet the caller by name."""
    phonenumber = phonenumber
    from_number = "+1(609) 834-4775"
    msg =  request.get_json()
    print(msg)
    body = msg.get('message')
    address = id(database.q_dict)
    print(ctypes.cast(address,ctypes.py_object).value)

    if validate_post(data_objects = msg):
        if  any(s in msg.keys() for s in ('message', 'Message', 'MESSAGE')) and any(k in msg.keys() for k in ('position', 'POSITION', 'Position')):
            bodies = body.lower()
            if from_number not in database.q_dict.keys():
                if any(s in body for s in ('add ','Add','ADD')):
                    body = Person(body, from_number)
                    database.add(body)
                    message1 = "Successfully added to queue"
                    position = database.lookup(from_number).index
                    position = str(position)
                    message2 = "There are " + position + " people ahead of you!"
                    message = message1 + " and " +  message2
                else:
                    message = "Give a proper command like add user to the queue"
            elif any(i in msg.keys() for i in ('remove', 'Remove', 'REMOVE')) or 'remove' in bodies:
                database.remove(from_number)
                message = "Successfully removed from queue!"
            elif any(g in msg.keys() for g in ('position', 'POSITION', 'Position')) or 'position' in bodies:
                position = database.lookup(from_number).index
                position = str(position)
                message = "There are " + position + " people ahead of you."
            else:
                message = "Please enter a proper command as you might be already in  queue."


        elif any(s in msg.keys() for s in ('message', 'Message', 'MESSAGE')): 
            bodies = body.lower()
            if from_number not in database.q_dict.keys():
                if any(s in body for s in ('add ','Add','ADD')):
                    body = Person(body, from_number)
                    database.add(body)
                    message = "Successfully added to queue!"
                else:
                    message = "Give a proper command like add user to the queue"
            elif any(i in msg.keys() for i in ('remove', 'Remove', 'REMOVE')) and 'remove' in bodies:
                database.remove(from_number)
                message = "Successfully removed from queue!"
            elif any(g in msg.keys() for g in ('position', 'POSITION', 'Position')) and 'position' in bodies:
                position = database.lookup(from_number).index
                position = str(position)
                message = "There are " + position + " people ahead of you."
            else:
                message = "Please enter a proper command as you might be already in  queue."

        elif any(g in msg.keys() for g in ('position', 'POSITION', 'Position')):
            if from_number  in database.q_dict.keys():
                position = database.lookup(from_number).index
                position = str(position)
                message = "There are " + position + " people ahead of you!"
            else:
                message = "Give a proper command as you might be not in queue"
        else:
            message = "Please enter the proper command/keys like message,position"
    else:
        response = Response(json.dumps({
            "error":"Invalid registration data",
            "help-string":'wrong input data'
        }),status=400, mimetype='appliaction/json')
        return response

    ACCOUNT_SID = "AC6515345468aefbd0c471629875fcd66a" # old: "ACfdea28b27b6aade7a9277dcb59c9ecdb" 
    AUTH_TOKEN = "3731564ce0cba5d0e355d5d31cc0ae21" # old: "0a171e4be02bd256d1122f32303608f7" 
    
    client = Client(ACCOUNT_SID, AUTH_TOKEN) 

    message = client.messages.create(
        to=phonenumber, 
        from_=from_number,
        body=message)

    print(message.sid)
    
    resp = flask.Response("success")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
    
        

@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return str('bad request!')

@app.errorhandler(500)
def server_error(e):

    app.logger.error(f"Server error: {request.url}")

    return str("server error 500")

@app.errorhandler(404)
def page_not_found(e):

    app.logger.info(f"Page not found: {request.url}")

    return str('Page Not Found 404 error') 

if __name__ == "__main__":
    app.run(debug=True)