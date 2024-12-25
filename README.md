# Global Insights Map
#### Video Demo: https://youtu.be/xoC_NTUFRbw

## Description:
The **Global Insights Map** is an interactive web application that visualizes real-time global data such as weather conditions, population density, and pollution levels. It combines powerful APIs with a modern and user-friendly interface to offer an engaging experience for users to explore global insights and manage their favorite locations.

### Key Features:
1. **Interactive Map Integration**:
   - Built using **Leaflet.js**, the map allows users to explore weather, population, and pollution data worldwide.
   - Users can view detailed information for specific locations, including weather conditions, temperature, humidity, and more.
   - Custom markers and icons enhance user interaction.

2. **User Authentication**:
   - Secure user login and registration using **Flask**.
   - Passwords are hashed for security using **Werkzeug**.
   - Sessions ensure personalized experiences, such as storing and displaying favorites.

3. **Favorites Management**:
   - Add, view, and delete favorite locations on the map.
   - Favorites are stored in a database using **Flask-SQLAlchemy** for persistence.
   - CRUD operations (Create, Read, Update, Delete) are implemented for user-managed data.

4. **API Integration**:
   - **OpenWeatherMap API**: Fetch real-time weather data for locations.
   - **Population API**: Fetch and validate country-specific population data.
   - Future integrations can include pollution data from sources like OpenAQ.

5. **Modern UI**:
   - Built with **Bootstrap** for responsiveness and styling.
   - Clear and concise layout for ease of use, with dynamic data updates using **AJAX**.

---

## Project Structure:
The project is organized into modular components to ensure clarity and maintainability.

### 1. Backend
- **Framework**: Flask
- **Core Files**:
  - `app/__init__.py`: Initializes the Flask application and extensions such as SQLAlchemy and Migrate.
  - `app/routes.py`: Defines the core routes, handling user interaction, and API calls.
  - `app/models.py`: Contains the database models for `User` and `Favorite`.
  - `app/utils.py`: Includes utility functions such as `login_required` decorators, API requests, and data validation.

### 2. Frontend
- **Templates**:
  - `templates/base.html`: Base layout with navigation bar and included CSS/JS dependencies.
  - `templates/index.html`: Landing page with an overview of the application's functionality.
  - `templates/map.html`: Interactive map interface for exploring and managing locations.
  - `templates/favorites.html`: Displays a list of user favorites.
  - `templates/register.html` and `login.html`: User authentication pages.
- **Static Files**:
  - Custom styles in `static/css/style.css`.
  - JavaScript functionality embedded in templates for AJAX and dynamic updates.

### 3. Database
- **SQLAlchemy Models**:
  - `User`: Manages user data, including hashed passwords.
  - `Favorite`: Stores user-defined locations with latitude, longitude, and names.

### 4. APIs
- **OpenWeatherMap API**: Provides weather data based on location coordinates.
- **Population API**: Validates country names and fetches population details.

---

## How It Works:
1. **Homepage**:
   - Users land on the homepage with options to log in or register.
2. **User Authentication**:
   - New users can register, while existing users can log in to access personalized features.
3. **Map Interaction**:
   - The map displays weather data and allows users to click on any location for detailed insights.
4. **Favorites Management**:
   - Users can add locations as favorites, view them on the map, and delete them as needed.
5. **Dynamic Updates**:
   - AJAX is used for seamless interactions, such as saving favorites without refreshing the page.

---

## Technologies Used:
- **Frontend**:
  - HTML, CSS, JavaScript
  - Leaflet.js (Map rendering)
  - Bootstrap (UI design)
- **Backend**:
  - Flask (Framework)
  - Flask-SQLAlchemy (Database management)
  - Flask-Migrate (Database migrations)
  - Werkzeug (Password hashing)
- **APIs**:
  - OpenWeatherMap API
  - Population.io API
- **Database**:
  - SQLite (Development phase, can be replaced with other databases)

---

## Challenges and Decisions:
1. **Design Choices**:
   - Flask was chosen for its simplicity and flexibility in building web applications.
   - Leaflet.js was selected for its extensive map customization options and ease of integration.
2. **API Integration**:
   - Managing rate limits and handling errors from external APIs required robust exception handling.
3. **User Authentication**:
   - Ensuring secure password storage and session management was a key priority.

---

## Future Enhancements:
1. **Additional Data Layers**:
   - Integrate pollution data using APIs like OpenAQ or EPA’s AirNow.
   - Add historical weather and population trends.
2. **Enhanced User Experience**:
   - Implement a heatmap for population density.
   - Allow users to set notifications for weather changes in favorite locations.
3. **Scalability**:
   - Migrate from SQLite to a more robust database like PostgreSQL for production.
   - Implement caching mechanisms for API responses to improve performance.

---

## Installation and Setup:
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/global-insights-map.git
   cd global-insights-map
2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Set up the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
5. Run the application:
   ```bash
   flask run

---
## Credits:
- **CS50**: For providing the foundation and resources to build this project.
- **APIs**: OpenWeatherMap, Population.io.
- **Libraries**: Flask, Leaflet.js, Bootstrap.

---

## Acknowledgments:
Special thanks to all the open-source contributors whose work made this project possible. Additionally, I appreciate the support and guidance from CS50 and the broader programming community.

ChatGPT by OpenAI. Assisted in API integration and debugging. 
Available at: https://chatgpt.com/
