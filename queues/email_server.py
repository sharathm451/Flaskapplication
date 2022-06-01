from pickle import NONE
import flask
import json
from flask import Flask, request, render_template,redirect,abort,Response
import werkzeug
import smtplib
from queues import app


queue = []

def validate_post(data_objects):
    if ('message' in data_objects):
        return True
    else:
        return False


@app.route("/email/<emailid>", methods=["GET","POST"])
def send_email(emailid):
    email = emailid 
    message =  request.get_json()

    if validate_post(data_objects=message):
        if message['message']:
            fromaddr = 'macharlasharath805@gmail.com'
            toaddrs  = email
            a = "From: macharlasharath805@gmail.com"
            b = "To: " + str(email)
            c = "Subject: Queue update!"
            d = ""
            msg = "\r\n".join([
            str(a),
            str(b),
            str(c),
            str(d),
            str(message['message'])
            ])
            username = 'macharlasharath805@gmail.com'
            password = 'ldsprckiiqxfizmk'
            HOST = "smtp.gmail.com"
            PORT = "587"
            server = smtplib.SMTP('smtp.gmail.com')
            server.connect(HOST, PORT)
            server.ehlo()
            server.starttls()
            server.login(username,password)
            server.sendmail(fromaddr, toaddrs, msg)
            server.close()
            print('successfully sent the mail')


            resp = flask.Response("success")
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
    else:
        response = Response(json.dumps({
        "error":"Invalid registration data",
        "help-string":'wrong input data'
        }),status=400, mimetype='appliaction/json')
        return response



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