from datetime import datetime
from operator import and_
from app.utils import get_session
from config import Config
from app.routes.users import redis_db
from app.models.cities import Cities
from app.models.screens import Screens
from app.models.shows import Shows
from app.models.movies import Movies
from app.models.booking import Booking
from app.models.movie_theaters import MovieTheaters

class MoviesNow():

    session = None

    def __init__(self) -> None:
        self.session = get_session(Config.SQLALCHEMY_DATABASE_URI)
    
    def get_cities(self):

        city_list = self.session.query(Cities.city_id,Cities.name).all()

        cities = []

        for city in city_list:
            temp = {}
            temp['City id'] = city[0]
            temp['City Name'] = city[1]
            cities.append(temp)

        response = {
            "status" : True,
            "data": {
                "cities" : cities
            }
        }

        return response

    def get_movies(self):
        movie_list = self.session.query(Movies.movie_id,Movies.movie_title,Movies.description,Movies.duration,Movies.genre,Movies.release_date).all()

        movies = []

        for movie in movie_list:
            temp = {}
            temp['Movie id'] = movie[0]
            temp['Movie Title'] = movie[1]
            temp['Movie Description'] = movie[2]
            temp['Movie Duration'] = str(movie[3]) + "minutes"
            temp['Movie Genre'] = movie[4]
            temp['Movie Movie'] = movie[5]

            movies.append(temp)

        response = {
            "status" : True,
            "data": {
                "movies" : movies
            }
        }

        return response

    def get_city_theaters(self,city_id):

        theater_list = self.session.query(MovieTheaters.theater_id,MovieTheaters.theater_name,MovieTheaters.total_screens).filter(MovieTheaters.city_id == city_id).all()
        # print(theater_list)
        theaters = []
        for theater in theater_list:
            temp = {}
            temp["Theater id"] = theater[0]
            temp["Number of screens"] = theater[2]
            temp["Theater Name"] = theater[1]

            theaters.append(temp)
        
        response = {
            "status" : True,
            "data": {
                "city_id" : city_id,
                "Theaters" : theaters
            }
        }

        return response

    def get_screens_info(self,theater_id):
        screens_list = self.session.query(Screens.screen_id,Screens.screen_name,Screens.total_seats).filter(Screens.theater_id == theater_id).all()

        screens = []

        for screen in screens_list:
            temp = {}
            temp["Screen id"] = screen[0]
            temp["Screen Name"] = screen[1]
            temp["Total Seats"] = screen[2]

            screens.append(temp)

        response = {
            "status" : True,
            "data": {
                "theater_id" : theater_id,
                "Screens" : screens
            }
        }

        return response

    def get_shows_info(self,movie_id,screen_id,date=None):
        print(date)
        if date:
            show_list = self.session.query(Shows.show_id,Shows.screen_id,Shows.start_time,Shows.end_time,Shows.date,Shows.booked_seat_counts).filter(and_(Shows.movie_id == movie_id,Shows.screen_id == screen_id)).filter(Shows.date == date).all()
        else:
            show_list = self.session.query(Shows.show_id,Shows.screen_id,Shows.start_time,Shows.end_time,Shows.date,Shows.booked_seat_counts).filter(and_(Shows.movie_id == movie_id,Shows.screen_id == screen_id)).all()
        shows = []
        for show in show_list:
            temp = {}
            temp['Show id'] = show[0]
            # temp['Show Screen'] = show[1]
            temp['Show Start Time'] = show[2]
            temp['Show End Time'] = show[3]
            temp['Show Date'] = show[4]
            temp['Remaining Seats'] = 30 - show[5]

            shows.append(temp)

        response = {
            "status" : True,
            "data": {
                "movie_id" : movie_id,
                "screen_id" : screen_id,
                "Show Details" : shows
            }
        }

        return response       

    def book_tickets(self,request_data):

        user_id = request_data.get("user_id")
        show_id = request_data.get("show_id")
        no_of_tickets = request_data.get("no_of_seats",1)

        show_details = self.session.query(Shows.booked_seat_counts).filter(Shows.show_id == show_id).first()

        if show_details[0] < 30 and no_of_tickets + show_details[0] <=30:

            booking_instance = Booking(user_id = user_id,show_id = show_id,no_of_seats = no_of_tickets,timestamp=datetime.now(),status = "Confirmed")
            self.session.add(booking_instance)
            self.session.commit()

            self.session.query(Shows).filter(Shows.show_id == show_id).update({'booked_seat_counts': Shows.booked_seat_counts + no_of_tickets})
            self.session.commit()
            response = {
                "status": True,
                "data":{
                    "message":"Tickets Successfully Booked",
                    "show_id":show_id,
                    "Number of Tickets booked" : no_of_tickets
                }
            }
        else:
            response = {
                "status": False,
                "data":{
                    "message":"Tickets Count Less than Requested",
                    "show_id":show_id,
                    "Number of Tickets Requested" : no_of_tickets,
                    "Error Code":"INSUFFICIENT_SEATS"
                }
            }
        return response

    def get_bookings(self,user_id):

        bookings_list = self.session.query(Booking.id,Booking.show_id,Booking.timestamp,Booking.no_of_seats).filter(Booking.user_id == user_id).all()

        bookings = []

        for booking in bookings_list:
            temp = {}
            temp["Booking id"] = booking[0]
            temp["Booked Show id"] = booking[1]
            temp["Booking TimeStamp"] = booking[2]
            temp["No Of Seats Booked"] = booking[3]

            bookings.append(temp)
        
        response = {
            "status" : True,
            "data": {
                "user_id" : user_id,
                "Booking Details" : bookings
            }
        }

        return response 

MoviesNow = MoviesNow()