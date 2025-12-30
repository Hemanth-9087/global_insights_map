# config.py
import os

# Prefer environment variables so secrets and keys are not stored in source control.
API_KEYS = {
    "weather": os.getenv("WEATHER_API_KEY", "3d292cd40cedd75da4fdf04ea8479338"),
}

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///favorites.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
