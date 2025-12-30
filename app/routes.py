from flask import Blueprint, jsonify, request, session, render_template, redirect, url_for
from .models import User,Favorite, db
from .utils import get_weather, get_population, get_coordinates_openweather,get_air_pollution,login_required
from . import db

routes = Blueprint("routes", __name__)
favorites = []

@routes.route("/")
def homepage():
    # Check if the user is logged in
    if "user_id" in session:
        return redirect(url_for("routes.map_page"))  # Redirect to map page
    return render_template("index.html")  # Serve the landing page

@routes.route("/map", methods=["GET"])
@login_required
def map_page():
    # Get latitude and longitude from query parameters (if any)
    lat = request.args.get("lat", default=None, type=float)
    lon = request.args.get("lon", default=None, type=float)
    return render_template("map.html", lat=lat, lon=lon)


@routes.route("/map")
@login_required
def map_view():
    user_id = session.get("user_id")

    # Fetch all favorite locations for the logged-in user
    user_favorites = Favorite.query.filter_by(user_id=user_id).all()

    # Convert to a list of dictionaries
    favorites_list = [
        {"name": fav.name, "lat": fav.lat, "lon": fav.lon} 
        for fav in user_favorites
    ]

    return render_template("map.html", favorites=favorites_list,username=session.get("username"))



@routes.route("/register", methods=["GET"])
def register_page():
    # Render the registration form (HTML page)
    return render_template("register.html")

@routes.route("/register", methods=["POST"])
def register():
    # Handle the form submission for registration
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
    """
    Authenticate a user and start a session.
    """
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session["user_id"] = user.id
        session["username"] = user.username
        return redirect(url_for("routes.map_page"))  # Redirect to the map page

    return jsonify({"error": "Invalid username or password"}), 401

@routes.route("/logout", methods=["GET"])
def logout():
    """
    Log out the current user by clearing the session.
    """
    session.clear()
    return redirect(url_for("routes.homepage"))  # Redirect to the homepage


# Fetch weather data
@routes.route("/weather/<location>")
def weather(location):
    data = get_weather(location)
    return jsonify(data)

@routes.route("/population/<country>")
def population(country):
    data = get_population(country)
    return jsonify(data)


@routes.route("/pollution/place", methods=["GET"])
def pollution_place():
    """
    Fetch air pollution data for a given place name.
    Example: /pollution/place?name=New Delhi
    """
    place_name = request.args.get("name")
    if not place_name:
        return jsonify({"error": "Place name is required. Example: /pollution/place?name=New Delhi"}), 400

    # Step 1: Get coordinates
    coordinates = get_coordinates_openweather(place_name)
    if "error" in coordinates:
        return jsonify(coordinates), 404

    # Step 2: Get air pollution data
    pollution_data = get_air_pollution(coordinates["latitude"], coordinates["longitude"])

    return jsonify({
        "place": f"{coordinates['name']}, {coordinates['country']}",
        "coordinates": {
            "latitude": coordinates["latitude"],
            "longitude": coordinates["longitude"]
        },
        "pollution": pollution_data
    })

@routes.route("/favorites", methods=["GET", "POST", "DELETE"])
@login_required
def favorites():
    user_id = session.get("user_id")

    if request.method == "GET":
        # Fetch all favorites for the logged-in user
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

        fav = Favorite.query.filter_by(id=fav_id, user_id=user_id).first()
        if fav:
            db.session.delete(fav)
            db.session.commit()
            return jsonify({"message": "Favorite deleted successfully!"}), 200

        return jsonify({"error": "Favorite not found."}), 404

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
