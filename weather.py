import os
import time
from datetime import datetime, timezone, timedelta

import requests
import pandas as pd
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


# =========================================================
# 1. LOAD .ENV
# =========================================================

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")


# =========================================================
# 2. CONFIGURATION
# =========================================================

LAT = 9.9252
LON = 78.1198
CITY = "Madurai"

DB_HOST = "localhost"
DB_USER = "root"
DB_NAME = "madurai_weather"
TABLE_NAME = "weather_records"

EXCEL_FILE = "madurai_weather.xlsx"

# New API record every 60 seconds
SLEEP_SECONDS = 60


# =========================================================
# 3. FETCH WEATHER FROM API
# =========================================================

def fetch_weather_data():

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "lat": LAT,
        "lon": LON,
        "appid": API_KEY,
        "units": "metric",
        "lang": "en"
    }

    response = requests.get(
        url,
        params=params,
        timeout=25
    )

    response.raise_for_status()

    data = response.json()

    weather = data["weather"][0]
    main = data.get("main", {})
    wind = data.get("wind", {})
    clouds = data.get("clouds", {})
    sys_data = data.get("sys", {})
    coordinates = data.get("coord", {})

    # IST
    ist = timezone(
        timedelta(hours=5, minutes=30)
    )

    recorded_at = datetime.now(ist)

    weather_record = {

        "city": data.get("name", CITY),

        "country": sys_data.get("country"),

        "latitude": coordinates.get("lat"),

        "longitude": coordinates.get("lon"),

        "temperature_c": main.get("temp"),

        "feels_like_c": main.get("feels_like"),

        "temp_min_c": main.get("temp_min"),

        "temp_max_c": main.get("temp_max"),

        "pressure_hpa": main.get("pressure"),

        "humidity_pct": main.get("humidity"),

        "visibility_m": data.get("visibility"),

        "wind_speed_mps": wind.get("speed"),

        "wind_deg": wind.get("deg"),

        "clouds_pct": clouds.get("all"),

        "weather_main": weather.get("main"),

        "weather_description": weather.get("description"),

        "recorded_at_ist":
            recorded_at.strftime("%Y-%m-%d %H:%M:%S")
    }

    return weather_record


# =========================================================
# 4. CONNECT MYSQL
# =========================================================

def connect_database():

    connection = mysql.connector.connect(

        host=DB_HOST,

        user=DB_USER,

        password=DB_PASSWORD

    )

    return connection


# =========================================================
# 5. CREATE DATABASE + TABLE
# =========================================================

def setup_database(connection):

    cursor = connection.cursor()

    # Create database
    cursor.execute(
        f"""
        CREATE DATABASE IF NOT EXISTS {DB_NAME}
        """
    )

    # Select database
    cursor.execute(
        f"""
        USE {DB_NAME}
        """
    )

    # Create table
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME}
        (

            id INT AUTO_INCREMENT PRIMARY KEY,

            city VARCHAR(100),

            country VARCHAR(10),

            latitude DOUBLE,

            longitude DOUBLE,

            temperature_c DOUBLE,

            feels_like_c DOUBLE,

            temp_min_c DOUBLE,

            temp_max_c DOUBLE,

            pressure_hpa INT,

            humidity_pct INT,

            visibility_m INT,

            wind_speed_mps DOUBLE,

            wind_deg INT,

            clouds_pct INT,

            weather_main VARCHAR(100),

            weather_description VARCHAR(200),

            recorded_at_ist DATETIME

        )
        """
    )

    connection.commit()

    cursor.close()

    print("Database and table ready!")


# =========================================================
# 6. INSERT DATA INTO MYSQL
# =========================================================

def insert_weather_data(connection, weather):

    cursor = connection.cursor()

    sql = f"""
        INSERT INTO {DB_NAME}.{TABLE_NAME}
        (
            city,
            country,
            latitude,
            longitude,
            temperature_c,
            feels_like_c,
            temp_min_c,
            temp_max_c,
            pressure_hpa,
            humidity_pct,
            visibility_m,
            wind_speed_mps,
            wind_deg,
            clouds_pct,
            weather_main,
            weather_description,
            recorded_at_ist
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
    """

    values = (

        weather["city"],

        weather["country"],

        weather["latitude"],

        weather["longitude"],

        weather["temperature_c"],

        weather["feels_like_c"],

        weather["temp_min_c"],

        weather["temp_max_c"],

        weather["pressure_hpa"],

        weather["humidity_pct"],

        weather["visibility_m"],

        weather["wind_speed_mps"],

        weather["wind_deg"],

        weather["clouds_pct"],

        weather["weather_main"],

        weather["weather_description"],

        weather["recorded_at_ist"]

    )

    cursor.execute(sql, values)

    connection.commit()

    cursor.close()

    print(
        "Inserted:",
        weather["recorded_at_ist"],
        "| Temp:",
        weather["temperature_c"],
        "°C",
        "| Humidity:",
        weather["humidity_pct"],
        "%",
        "| Lat:",
        weather["latitude"],
        "| Lon:",
        weather["longitude"]
    )


# =========================================================
# 7. LOAD MYSQL DATA INTO PANDAS
# =========================================================

def load_weather_data(connection):

    query = f"""
        SELECT *
        FROM {DB_NAME}.{TABLE_NAME}
        ORDER BY recorded_at_ist
    """

    cursor = connection.cursor(dictionary=True)

    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()

    df = pd.DataFrame(rows)

    return df


# =========================================================
# 8. CLEAN DATA
# =========================================================

def clean_weather_data(df):

    if df.empty:

        return df

    # Convert datetime
    df["recorded_at_ist"] = pd.to_datetime(
        df["recorded_at_ist"],
        errors="coerce"
    )

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Sort by time
    df = df.sort_values(
        "recorded_at_ist"
    )

    # Reset index
    df = df.reset_index(
        drop=True
    )

    return df


# =========================================================
# 9. DATA QUALITY CHECK
# =========================================================

def data_quality_check(df):

    print("\n===== DATA QUALITY CHECK =====")

    print(
        "Total records:",
        len(df)
    )

    print(
        "Total columns:",
        len(df.columns)
    )

    print(
        "Duplicate rows:",
        df.duplicated().sum()
    )

    print("\nMissing values:")

    print(
        df.isnull().sum()
    )


# =========================================================
# 10. BASIC ANALYSIS
# =========================================================

def weather_analysis(df):

    if df.empty:

        print("No data available.")

        return

    print("\n===== WEATHER ANALYSIS =====")

    # Temperature
    print("\nTemperature")

    print(
        "Minimum:",
        round(
            df["temperature_c"].min(),
            2
        ),
        "°C"
    )

    print(
        "Maximum:",
        round(
            df["temperature_c"].max(),
            2
        ),
        "°C"
    )

    print(
        "Average:",
        round(
            df["temperature_c"].mean(),
            2
        ),
        "°C"
    )

    # Humidity
    print("\nHumidity")

    print(
        "Minimum:",
        df["humidity_pct"].min(),
        "%"
    )

    print(
        "Maximum:",
        df["humidity_pct"].max(),
        "%"
    )

    print(
        "Average:",
        round(
            df["humidity_pct"].mean(),
            2
        ),
        "%"
    )

    # Wind
    print("\nWind Speed")

    print(
        "Minimum:",
        round(
            df["wind_speed_mps"].min(),
            2
        ),
        "m/s"
    )

    print(
        "Maximum:",
        round(
            df["wind_speed_mps"].max(),
            2
        ),
        "m/s"
    )

    print(
        "Average:",
        round(
            df["wind_speed_mps"].mean(),
            2
        ),
        "m/s"
    )

    # Weather conditions
    print("\nWeather Conditions")

    print(
        df["weather_main"].value_counts()
    )


# =========================================================
# 11. EXPORT TO EXCEL
# =========================================================

def export_to_excel(df):

    if df.empty:

        return

    df.to_excel(
        EXCEL_FILE,
        index=False
    )

    print(
        "Excel updated:",
        EXCEL_FILE
    )


# =========================================================
# 12. MAIN PROGRAM
# =========================================================

connection = None

try:

    # Check API key
    if not API_KEY:

        print(
            "ERROR: OPENWEATHER_API_KEY not found."
        )

        raise SystemExit

    # Connect MySQL
    connection = connect_database()

    print(
        "MySQL connected successfully!"
    )

    # Setup database
    setup_database(connection)

    # -----------------------------------------------------
    # CONTINUOUS DATA COLLECTION
    # -----------------------------------------------------

    while True:

        print("\n")
        print("=" * 55)

        print(
            "Fetching Madurai weather..."
        )

        print("=" * 55)

        # Fetch API data
        weather = fetch_weather_data()

        # Insert into MySQL
        insert_weather_data(
            connection,
            weather
        )

        # Load all data
        df = load_weather_data(
            connection
        )

        # Clean data
        df = clean_weather_data(
            df
        )

        # Excel
        export_to_excel(
            df
        )

        # Quality check
        data_quality_check(
            df
        )

        # Analysis
        weather_analysis(
            df
        )

        print("\n")
        print(
            f"Next update in {SLEEP_SECONDS} seconds..."
        )

        # Wait
        time.sleep(
            SLEEP_SECONDS
        )


# =========================================================
# ERROR HANDLING
# =========================================================

except requests.RequestException as e:

    print(
        "OpenWeather API Error:",
        e
    )

except Error as e:

    print(
        "MySQL Error:",
        e
    )

except KeyboardInterrupt:

    print(
        "\nData collection stopped."
    )

except Exception as e:

    print(
        "Unexpected Error:",
        e
    )

finally:

    if connection is not None:

        try:

            if connection.is_connected():

                connection.close()

                print(
                    "MySQL connection closed."
                )

        except Exception:

            pass