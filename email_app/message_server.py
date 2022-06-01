from twilio.rest import Client 
import flask 
from twilio.base.exceptions import TwilioRestException
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/", methods=["GET","POST"])
def send_message():
	phone_number = request.form.get('phone_number')
	message = request.form.get('message')

	# put your own credentials here 
	ACCOUNT_SID = "ACfdea28b27b6aade7a9277dcb59c9ecdb" 
	AUTH_TOKEN = "[AuthToken]" 
	client = Client(ACCOUNT_SID, AUTH_TOKEN) 
	
	try:
		client.messages.create(
		to="+13106621364", 
		from_="+14243284604", 
		body="testing",  
	)
	except TwilioRestException as e:
		('Twilio SMS: ERROR - {}'.format(str(e)))
		
	resp = flask.Response("success")
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp
	

if __name__ == "__main__":
	app.run(debug=True)

