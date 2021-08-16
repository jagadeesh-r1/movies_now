import logging
from flask import Blueprint, jsonify, request
from app.services.movies_now import MoviesNow
from .users import redis_db


movies = Blueprint('movies', __name__)

logger = logging.getLogger(__name__)

@movies.route('/cities',methods=['GET'])
def get_cities():
    '''
    Endpoint gives list of cities in the DB.
    '''
    data = MoviesNow.get_cities()
    if not data:
        data = {}
    return jsonify(data)

@movies.route('/movies',methods=['GET'])
def get_movies():
    '''
    Endpoint gives list of movies in the DB.
    '''
    data = MoviesNow.get_movies()
    if not data:
        data = {}
    return jsonify(data)

@movies.route('/theaters/<city_id>',methods=['GET'])
def get_city_theaters(city_id):
    '''
    Gives the Theaters in a Given City.
    '''
    data = MoviesNow.get_city_theaters(city_id)
    if not data:
        data = {}
    return jsonify(data)

@movies.route('/screens/<theater_id>',methods=['GET'])
def get_screens_in_theater(theater_id):
    
    data = MoviesNow.get_screens_info(theater_id)
    if not data:
        data = {}
    return jsonify(data)


@movies.route('/shows/<movie_id>/<screen_id>',methods=['GET'])
def get_shows(movie_id,screen_id):
    request_params = request.args
    data = MoviesNow.get_shows_info(movie_id,screen_id,date=request_params.get("date"))
    if not data:
        data = {}
    return jsonify(data)



@movies.route('/book_tickets',methods=['POST'])
def book_tickets():
    authentication_token = request.headers["Authorization"].split(" ")[1]

    if redis_db.get(authentication_token):

        request_data = request.get_json()
        request_data["data"]["user_id"] = int(redis_db.get(authentication_token).decode("utf-8"))
        data = MoviesNow.book_tickets(request_data["data"])
        if not data:
            data = {}
        return jsonify(data)
    else:
        response = {
            "status" : False,
            "data":{
                "message":"Please LogIn to Book Tickets",
                "Error Code": "SESSION_NOT_FOUND"
            }
        }
        return response

@movies.route('/bookings/<user_id>', methods=["GET"])
def get_bookings(user_id):
    authentication_token = request.headers["Authorization"].split(" ")[1]

    if redis_db.get(authentication_token):

        user_id = int(redis_db.get(authentication_token).decode("utf-8"))
        data = MoviesNow.get_bookings(user_id)
        if not data:
            data = {}
        return jsonify(data)
    else:
        response = {
            "status" : False,
            "data":{
                "message":"Please LogIn to Get Bookings",
                "Error Code": "SESSION_NOT_FOUND"
            }
        }
        return response