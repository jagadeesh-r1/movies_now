from operator import or_
import re
from flask.globals import session
import redis
import uuid
import bcrypt
import logging
from flask import Blueprint, jsonify, request, render_template_string
from config import Config
from app.models.users import Users
from app.utils import get_session


session = get_session(Config.SQLALCHEMY_DATABASE_URI)

redis_db = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_DB,password=Config.REDIS_PASSWORD)



users = Blueprint('users', __name__)

logger = logging.getLogger(__name__)

@users.route('/', methods=["GET"])
def health_check():
    return jsonify({"message":"hello! I'm working"})




@users.route('/login', methods =['POST'])
def login():

    request_data = request.get_json()
    if 'username' in request_data and 'password' in request_data:
        username = request_data['username']
        password = request_data['password'].encode("utf-8")
        # password = bcrypt.hashpw(password.encode('utf-8'),salt=bcrypt.gensalt())
        # print(bcrypt.hashpw(password.encode('utf-8'),salt=bcrypt.gensalt()))
        print(password)
        account = session.query(Users.username,Users.password,Users.user_id).filter(Users.username == username).first()

        print(account)
        if account and bcrypt.checkpw(password,account[1].encode("utf-8")):
            msg = 'Logged in successfully !'
            session_id = str(uuid.uuid4())
            redis_db.set(session_id,str(account[2]))
            response = {
                "status" : True,
                "data":{
                    "message" : msg + "Please Use the following Token as Bearer Token for other API endpoint requests",
                    "token" : session_id
                }
            }
            return jsonify(response)
        else:
            msg = 'Incorrect username / password !'
            response = {
                "status" : False,
                "data":{
                    "message" : msg,
                    "Error Code" : "INCORRECT_CREDENTIALS"
                }
            }
            return jsonify(response)
    return jsonify({})
  
@users.route('/logout', methods = ["POST"])
def logout():
    request_data = request.headers
    token = request_data["Authorization"].split(" ")[1]
    redis_db.delete(token)
    msg = "User logged out Successfully!"
    response = {
                "status" : True,
                "data":{
                    "message" : msg
                }
            }
    return jsonify(response)
  
@users.route('/register', methods =['POST'])
def register():
    msg = ''
    request_data = request.get_json()
    if 'username' in request_data and 'password' in request_data and 'email' in request_data :
        username = request_data['username']
        password = request_data['password']
        password = bcrypt.hashpw(password.encode('utf-8'),salt=bcrypt.gensalt()).decode("utf-8")
        email = request_data['email']
        phone = request_data['phone']
        city = request_data['city']

        account = session.query(Users.username,Users.email).filter(or_(Users.username.like(username),Users.email.like(email))).first()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please Send Required Fields!'
        else:
            
            new_user = Users(username=username,password=password,email=email,phone=phone,city_id=city)
            session.add(new_user)
            session.commit()
            msg = 'You have successfully registered !'
            response = {
                        "status" : True,
                        "data":{
                            "message" : msg
                        }
                    }
            return jsonify(response)
    response = {
                "status" : False,
                "data":{
                    "message" : msg
                }
            }
    return jsonify(response)


# @users.route('/users/<user_id>', methods =['GET'])
# def get_users(user_id):
#     pass