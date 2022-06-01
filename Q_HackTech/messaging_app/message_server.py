import flask
from twilio.rest import Client
from flask import Flask, request, render_template, redirect, abort
from twilio.twiml.messaging_response import MessagingResponse
from collections import deque
import werkzeug


app = Flask(__name__)

class Person:
    def __init__(self, name, number):
        self.name = name
        self.number = number

class Database:
    def __init__(self):
        self.q = []
        self.q_dict = {}

    # Takes in a Person object and adds it to the database
    def add(self, person):
        self.q.append(person)
        self.q_dict[person.number] = person
        person.index = len(self.q) - 1 

    def update_indices(self):
        for i in range(len(self.q)):
            person = self.q[i]
            person.index = i

    def pop_first(self):
        number = self.q[0].number
        return self.remove(number)

    def remove(self, number):
        person = self.q_dict[number]
        index = person.index
        del self.q[index]
        del self.q_dict[number]
        self.update_indices()
        return person

    def lookup(self, number):
        return self.q_dict[number]

    def exists(self, number):
        return number in self.q_dict

def print_all(database):
    for person in database.q:
        print(person.name, person.number)

person1 = Person("Person1", "1")
person2 = Person("Person2", "2")
person3 = Person("Person3", "3")
person4 = Person("Person4", "4")
person5 = Person("Person5", "5")

database = Database()
database.add(person1)
database.add(person2)
database.add(person3)
database.add(person4)
database.add(person5)


# @app.route("/", methods=["POST"])
# def send_message():
# 	phone_number = request.form.get('phone_number')
# 	message = request.form.get('message')
 
# 	ACCOUNT_SID = "AC8463c9cf9bee23b138a7aa6fcece2d82" # old: "ACfdea28b27b6aade7a9277dcb59c9ecdb" 
# 	AUTH_TOKEN = "7b762b4d98ba3e30a69bf11985d15083" # old: "0a171e4be02bd256d1122f32303608f7" 
     
# 	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 

# 	client.messages.create(
# 		to=phone_number, 
# 		from_="+14242773397", # old: "+14243284604" 
# 		body=message,  
# 	)

# 	resp = flask.Response("success")
# 	resp.headers['Access-Control-Allow-Origin'] = '*'
# 	return resp


# @app.route("/", methods=['GET', 'POST'])
# def hello_monkey():
#     """Respond and greet the caller by name."""
 
#     from_number = request.values.get('From', None)
#     if from_number in callers:
#         message = callers[from_number] + ", thanks for the message!"
#     else:
#         message = "Monkey, thanks for the message!"
 
#     resp = twilio.twiml.Response()
#     resp.message(message)
 
#     return str(resp)

@app.route("/message/<phonenumber>", methods=['GET', 'POST'])
def hello_monkey(phonenumber):
#    abort(500)
    """Respond and greet the caller by name."""
    phonenumber = phonenumber
    from_number = "+1(609) 834-4775"
    body =  request.get_json('message')

    if not database.exists(from_number):
        person = Person(body, from_number)
        database.add(person)
        message = "Successfully added to queue!"
    elif body == "REMOVE":
        database.remove(from_number)
        message = "Successfully removed from queue!"
    elif body == "POSITION":
        position = database.lookup(from_number).index
        message = "There are " + position + " people ahead of you."
    else:
        message = "Please enter a proper command."

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