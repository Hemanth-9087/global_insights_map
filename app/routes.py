from flask import Blueprint, jsonify, request, session, render_template, redirect, url_for
from .models import User,Favorite, db
from .utils import login_required ,get_country_name ,get_population
from . import db
from config import API_KEYS
import requests
from datetime import datetime

def format_timestamp(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%H:%M:%S')

routes = Blueprint("routes", __name__)
favorites = []

@routes.route("/")
def homepage():

    if "user_id" in session:
        return redirect(url_for("routes.map_page"))  
    return render_template("index.html")  

@routes.route("/map", methods=["GET"])
@login_required
def map_page():

    user_id = session.get("user_id")
    user_favorites = Favorite.query.filter_by(user_id=user_id).all()

    favorites_list = [
        {"name": fav.name, "lat": fav.lat, "lon": fav.lon,"id": fav.id} 
        for fav in user_favorites
    ]

    lat = request.args.get("lat", default=None, type=float)
    lon = request.args.get("lon", default=None, type=float)
    return render_template("map.html", api_key=API_KEYS["weather"],lat=lat, lon=lon,favorites=favorites_list,username=session.get("username"))


@routes.route("/register", methods=["GET"])
def register_page():

    return render_template("register.html")

@routes.route("/register", methods=["POST"])
def register():

    data = request.json
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"message": "Username already exists"}), 400
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already registered"}), 400

    new_user = User(username=data["username"], email=data["email"])
    new_user.set_password(data["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"})


@routes.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@routes.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session["user_id"] = user.id
        session["username"] = user.username
        return redirect(url_for("routes.map_page"))  

    return jsonify({"error": "Invalid username or password"}), 401

@routes.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("routes.homepage"))




@routes.route("/favorites", methods=["GET", "POST", "DELETE"])
@login_required
def favorites():
    user_id = session.get("user_id")

    if request.method == "GET":
        user_favorites = Favorite.query.filter_by(user_id=user_id).all()
        return render_template("favorites.html", favorites=user_favorites)

    elif request.method == "POST":
        data = request.get_json()
        name = data.get("name")
        lat = data.get("lat")
        lon = data.get("lon")

        if not name or not lat or not lon:
            return jsonify({"error": "Invalid input. Name, latitude, and longitude are required."}), 400

        new_fav = Favorite(name=name, lat=float(lat), lon=float(lon), user_id=user_id)
        db.session.add(new_fav)
        db.session.commit()
        return jsonify({"message": "Favorite added successfully!"}), 200

    elif request.method == "DELETE":
        data = request.get_json()
        fav_id = data.get("id")

        try:
            fav = Favorite.query.filter_by(id=fav_id, user_id=user_id).first()
            if fav:
                db.session.delete(fav)
                db.session.commit()
                return jsonify({"message": "Favorite deleted successfully!"}), 200

            return jsonify({"error": "Favorite not found."}), 404
        except Exception as e:
            print(f"Error while deleting favorite: {e}")
            db.session.rollback()
            return jsonify({"error": "Internal server error."}), 500

@routes.route("/delete_favorite", methods=["POST"])
@login_required
def delete_favorite():
    user_id = session.get("user_id")
    fav_id = request.form.get("id")

    fav = Favorite.query.filter_by(id=fav_id, user_id=user_id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
    return redirect(url_for("routes.favorites"))


@routes.route("/details", methods=["GET"])
@login_required
def details():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)

    if lat is None or lon is None:
        return jsonify({"error": "Latitude and Longitude are required"}), 400

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEYS['weather']}&units=metric"
    weather_response = requests.get(weather_url).json()

    if "sys" in weather_response:
        country_code = weather_response["sys"].get("country", "Unknown")
        country_name = get_country_name(country_code)
        sunrise_time = format_timestamp(weather_response["sys"]["sunrise"])
        sunset_time = format_timestamp(weather_response["sys"]["sunset"])
    else:
        country_name = "Unknown Country"
        sunrise_time = "Unavailable"
        sunset_time = "Unavailable"

    population_data = get_population(country_code) if country_name != "Unknown Country" else {"error": "Population data unavailable"}

    return render_template("details.html", 
                           weather=weather_response, 
                           lat=lat, 
                           lon=lon, 
                           country=country_name, 
                           sunrise=sunrise_time, 
                           sunset=sunset_time, 
                           population=population_data)
