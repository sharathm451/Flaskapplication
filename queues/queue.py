import mimetypes
import werkzeug
from flask import Response,make_response
import json
import flask
from flask import  redirect, url_for,flash, request,jsonify
from queues import db,app
from sqlalchemy.orm import validates 
import re


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    mobile_no = db.Column(db.Integer(),nullable=False,unique=True)


def validate_post(data_objects):
    if ('username' in data_objects and 'email_address' in data_objects and "mobile_no" in data_objects):
        return True
    else:
        return False

@app.route('/queue', methods=['POST'])
def register_page():
    body =  request.get_json()
    if validate_post(data_objects = body):
        if body["username"] and body["email_address"] and body["mobile_no"]:
            if not re.match("[^@]+@[^@]+\.[^@]+", body["email_address"]):
                return make_response('Provided email is not an email address') 

            if not re.match(r'(^[+0-9]{1,3})*([0-9]{10,11}$)',body["mobile_no"]):
                return make_response("provided number in not a mobile number")

            existing_user = User.query.filter(User.username == body["username"] or User.email_address == body["email_address"] or User.mobile_no == body["mobile_no"]).first()
            if existing_user:
                return make_response(f'{body["username"]} ({body["email_address"]}) already created!')

            users = User(username=body["username"],
                                email_address=body["email_address"],
                                mobile_no=body["mobile_no"])
            try:
                db.session.add(users)
                db.session.commit()
                print(User.query.all())
                resp = flask.Response("success")
                resp.headers['Access-Control-Allow-Origin'] = '*'
                return resp
            except AssertionError as exception_message: 
                return jsonify(msg='Error: {}. '.format(exception_message)), 400
    else:
        response = Response(json.dumps({
            "error":"Invalid registration data",
            "help-string":'wrong input data'
        }),status=400, mimetype='appliaction/json')
        return response

@app.route('/queue', methods=['GET'])
def get_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['username'] = user.username
        user_data['email_address'] = user.email_address
        user_data['mobile_no'] = user.mobile_no
        output.append(user_data)
    return jsonify({'users':output})
    
@app.route('/queue/<email_address>', methods=['GET'])
def get_auser(email_address):
    user = User.query.filter_by(email_address=email_address).first()
    if not user:
        return jsonify({"message": 'No user Found!'})
    user_data={}
    user_data['username'] = user.username
    user_data['email_address'] = user.email_address
    user_data['mobile_no']=user.mobile_no
    return jsonify({'user': user_data})

@app.route('/queue/<email_address>',methods=['DELETE'])
def del_user(email_address):
    user = User.query.filter_by(email_address=email_address).first()
    if not user:
        return jsonify({"message": 'No user Found!'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message":"The user has been deleted!"})


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