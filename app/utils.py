import requests
from config import API_KEYS
from functools import wraps
from flask import session, jsonify
import pycountry

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Login required"}), 401
        return func(*args, **kwargs)
    return wrapper

VALID_COUNTRIES = []

def fetch_valid_countries():
    global VALID_COUNTRIES
    url = "https://d6wn6bmjj722w.population.io/1.0/countries/"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        VALID_COUNTRIES = [country for country in data.get("countries", [])]
    else:
        print("Failed to fetch country list from the API")

def validate_country_name(input_country):
    for country in VALID_COUNTRIES:
        if country.lower() == input_country.lower():
            return country  # Return the exact country name from the API
    return None


def get_population(country_code):
    country_name = get_country_name(country_code)
    valid_country = validate_country_name(country_name)
    
    if not valid_country:
        return {"error": "No population data available."}

    url = f"https://d6wn6bmjj722w.population.io/1.0/population/{valid_country}/today-and-tomorrow/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "total_population" in data:
            return {
                "country": valid_country,
                "population_today": data["total_population"][0]["population"],
                "population_tomorrow": data["total_population"][1]["population"],
            }
        return {"error": "No population data available for the given country"}
    else:
        return {"error": f"API error: {response.status_code}"}


def get_country_name(country_code):
    try:
        country = pycountry.countries.get(alpha_2=country_code)
        return country.name if country else "Unknown Country"
    except Exception as e:
        print(f"Error converting country code {country_code} to name: {e}")
        return "Unknown Country"


