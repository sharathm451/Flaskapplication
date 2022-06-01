from email import message
from pickle import FALSE, TRUE
import flask
from flask import Flask, request, render_template,redirect,abort
import werkzeug
import smtplib
from flask_mail import Mail
from flask_mail import Message


app = Flask(__name__)

from smtplib import SMTP_SSL, SMTP, SMTPAuthenticationError
from ssl import create_default_context
from email.message import EmailMessage

sender = 'aaa@bbb.com'
description = "This is the test description supposed to be in body of the email."
msg = EmailMessage()
msg.set_content(description)
msg['Subject'] = 'This is a test title'
msg['From'] = f"Python SMTP <{'qmessaging@gmail.com'}>"
msg['To'] = 'sharathm451@gmail.com'


# def using_ssl():
#     try:
#         server = SMTP_SSL(host='smtp.gmail.com', port=465, context=create_default_context())
#         server.login(sender, 'csuahackathon')
#         server.send_message(msg=msg)
#         server.quit()
#         server.close()
#     except SMTPAuthenticationError:
#         print('Login Failed')

# def using_tls():
#     try:
#         server = SMTP(host='smtp.gmail.com', port=587)
#         server.starttls(context=create_default_context())
#         server.ehlo()
#         server.login(sender, 'csuahackathon')
#         server.send_message(msg=msg)
#         server.quit()
#         server.close()
#     except SMTPAuthenticationError:
#         print('Login Failed')



app.config['DEBUG'] =  True
app.config['TESTING'] = FALSE
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = TRUE
app.config['MAIL_USE_SSL'] = FALSE
# app.config['MAIL_DEBUG'] = TRUE
app.config['MAIL_USERNAME'] = "macharlasharath805@gmail.com"
app.config['MAIL_PASSWORD'] = 'ldsprckiiqxfizmk'
app.config['MAIL_DEFAULT_SENDER'] = "macharlasharath805@gmail.com"
app.config['MAIL_MAX_EMAILS'] = None    
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False
server = smtplib.SMTP('smtp.gmail.com:587')     

mail = Mail(app)

@app.route('/')
def index():
    msg = Message('Hey there', recipients=['sharathm451@gmail.com'])
    mail.send(msg)
    return str('Message has been sent')


# queue = []

# @app.route("/email<emailid>", methods=["GET","POST"])
# def send_email(emailid):
#     email = emailid 
#     message = "hello how are you?"

#     emails = request.form.get('email')
#     messages = request.form.get('message')

#     fromaddr = 'qmessaging@gmail.com'
#     toaddrs  = email
#     a = "From: qmessaging@gmail.com"
#     b = "To: " + str(email)
#     c = "Subject: Queue update!"
#     d = ""
#     msg = "\r\n".join([
#       str(a),
#       str(b),
#       str(c),
#       str(d),
#       str(message)
#     ])
#     mail.send(msg)
    
#     resp = flask.Response("success")
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp

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