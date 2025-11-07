# 🗺️ Pothik Bondhu (পথিক বন্ধু) - v1.0

Welcome to **Pothik Bondhu**, your smart journey partner for exploring Bangladesh. This is a full-stack web application built with Django and JavaScript.

This app does more than just plan a route from A to B. It reveals the **"Route Wealth"** of your journey—the hidden gems, famous foods, and top sights of every district you pass through.

![Screenshot of Pothik Bondhu Dark Mode](image_92dbe0.png)
*(You can replace this with a real link to your screenshot later)*

---

## 🚀 Version 1.0 Features

* **Dynamic Route Planning:** Enter any two districts in Bangladesh and get an instant, optimal driving route drawn on an interactive map.
* **Complete "Route Wealth" Guide:** See your journey broken down step-by-step, district-by-district.
* **Custom 64-District Database:** A hand-curated database (powered by a Django fixture) that lists the unique "Top Sights" and "Famous Foods" for all 64 districts.
* **Live Weather Integration:** Get real-time weather data (temperature, conditions) for your start and end locations, powered by the OpenWeatherMap API.
* **Smart Form Validation:** An HTML `<datalist>` ensures users can only select valid district names, fixing all spelling and capitalization errors.
* **Fully Responsive Dark Mode:** A beautiful, modern UI built from scratch with custom CSS. It's 100% mobile-friendly and features a full dark-mode theme, animated loaders, and glowing effects.
* **Live API Integration:**
    * **Maps:** [Leaflet.js](https://leafletjs.com/) with dark mode tiles from [CartoDB](https://carto.com/).
    * **Routing:** [OSRM (Open Source Routing Machine)](http://project-osrm.org/)
    * **Geocoding:** [Nominatim (OpenStreetMap)](https://nominatim.org/)
    * **Weather:** [OpenWeatherMap](https://openweathermap.org/)

---

## 🛠️ Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML5, CSS3, JavaScript (ES6+)
* **Database:** SQLite3 (default), Django ORM
* **APIs:** OSRM, Nominatim (OpenStreetMap), OpenWeatherMap

---

## 🏁 How to Run This Project Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/emon6000/pothik-bondhu.git](https://github.com/emon6000/pothik-bondhu.git)
    cd pothik-bondhu
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Windows
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

3.  **Install all required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create your secret `.env` file:**
    * Create a file named `.env` in the root folder.
    * Add your secret keys to it:
    ```ini
    SECRET_KEY=your_django_secret_key
    WEATHER_API_KEY=your_openweathermap_api_key
    ```

5.  **Run the database migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Load the 64-District Database:**
    * This is the most important step! This will load all the sights and food data.
    ```bash
    python manage.py loaddata districts
    ```

7.  **Run the app!**
    ```bash
    python manage.py runserver
    ```
    The project will be running at `http://127.0.0.1:8000/`

---

## 👤 Author

* **Abdullah Al Mahmud Emon**
    * GitHub: [@emon6000](https://github.com/emon6000)
    * LinkedIn: [@abdem0n](https://www.linkedin.com/in/abdem0n/)