from collections import deque
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import flask
from flask import Flask, request, render_template, redirect, abort
import werkzeug

def delete_nth(d, n):
    d.rotate(-n)
    d.popleft()
    d.rotate(n)

Q = deque()

app = Flask(__name__)
@app.route('/queue', methods=["GET","POST"])
def send_message():
	phone_number = request.form.get('phone_number')
	message = request.form.get('message')
 
	ACCOUNT_SID = "ACfdea28b27b6aade7a9277dcb59c9ecdb" 
	AUTH_TOKEN = "0a171e4be02bd256d1122f32303608f7" 
	 
	client = Client(ACCOUNT_SID, AUTH_TOKEN) 
	try:
		client.messages.create(
		to= phone_number, 
		from_="+14243284604", 
		body=message,  
	)
	except TwilioRestException as e:
		('Twilio SMS: ERROR - {}'.format(str(e)))

	resp = flask.Response("success")
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
