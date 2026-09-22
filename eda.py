import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv()


# ==========================================
# 1. MYSQL CONFIGURATION
# ==========================================

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_NAME = "madurai_weather"
TABLE_NAME = "weather_records"

# ==========================================
# 2. CONNECT TO MYSQL
# ==========================================

connection = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

print("MySQL connected successfully!")


# ==========================================
# 3. LOAD DATA INTO PANDAS
# ==========================================

query = f"""
SELECT *
FROM {TABLE_NAME}
ORDER BY recorded_at_ist
"""

df = pd.read_sql(query, connection)

connection.close()

print("Data loaded successfully!")


# ==========================================
# 4. BASIC DATASET INFORMATION
# ==========================================

print("\n===================================")
print("DATASET INFORMATION")
print("===================================")

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nColumns:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)


# ==========================================
# 5. DATA CLEANING
# ==========================================

print("\n===================================")
print("DATA CLEANING")
print("===================================")

# Convert datetime
df["recorded_at_ist"] = pd.to_datetime(
    df["recorded_at_ist"],
    errors="coerce"
)

# Remove duplicate rows
duplicate_count = df.duplicated().sum()

print("Duplicate rows:", duplicate_count)

df = df.drop_duplicates()

# Check missing values
print("\nMissing values BEFORE cleaning:")

print(df.isnull().sum())

# Numeric columns
numeric_columns = [
    "latitude",
    "longitude",
    "temperature_c",
    "feels_like_c",
    "temp_min_c",
    "temp_max_c",
    "pressure_hpa",
    "humidity_pct",
    "visibility_m",
    "wind_speed_mps",
    "wind_deg",
    "clouds_pct"
]

# Convert numeric columns
for column in numeric_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

# Fill missing numeric values with median
for column in numeric_columns:

    if df[column].isnull().sum() > 0:

        df[column] = df[column].fillna(
            df[column].median()
        )

# Fill missing text values
text_columns = [
    "city",
    "country",
    "weather_main",
    "weather_description"
]

for column in text_columns:

    df[column] = df[column].fillna(
        "Unknown"
    )

print("\nMissing values AFTER cleaning:")

print(df.isnull().sum())


# ==========================================
# 6. CREATE DATE/TIME FEATURES
# ==========================================

df["date"] = df["recorded_at_ist"].dt.date

df["hour"] = df["recorded_at_ist"].dt.hour

df["minute"] = df["recorded_at_ist"].dt.minute

df["day_name"] = df["recorded_at_ist"].dt.day_name()


# ==========================================
# 7. OUTLIER CHECK
# ==========================================

print("\n===================================")
print("OUTLIER CHECK")
print("===================================")

Q1 = df["temperature_c"].quantile(0.25)

Q3 = df["temperature_c"].quantile(0.75)

IQR = Q3 - Q1

lower_limit = Q1 - 1.5 * IQR

upper_limit = Q3 + 1.5 * IQR

outliers = df[
    (df["temperature_c"] < lower_limit) |
    (df["temperature_c"] > upper_limit)
]

print(
    "Temperature outliers:",
    len(outliers)
)


# ==========================================
# 8. DESCRIPTIVE STATISTICS
# ==========================================

print("\n===================================")
print("DESCRIPTIVE STATISTICS")
print("===================================")

print(
    df[
        [
            "temperature_c",
            "humidity_pct",
            "pressure_hpa",
            "wind_speed_mps",
            "clouds_pct"
        ]
    ].describe()
)


# ==========================================
# 9. WEATHER CONDITION ANALYSIS
# ==========================================

print("\n===================================")
print("WEATHER CONDITIONS")
print("===================================")

weather_counts = df["weather_main"].value_counts()

print(weather_counts)


# ==========================================
# 10. TEMPERATURE ANALYSIS
# ==========================================

print("\n===================================")
print("TEMPERATURE ANALYSIS")
print("===================================")

print(
    "Minimum:",
    round(df["temperature_c"].min(), 2),
    "°C"
)

print(
    "Maximum:",
    round(df["temperature_c"].max(), 2),
    "°C"
)

print(
    "Average:",
    round(df["temperature_c"].mean(), 2),
    "°C"
)


# ==========================================
# 11. HUMIDITY ANALYSIS
# ==========================================

print("\n===================================")
print("HUMIDITY ANALYSIS")
print("===================================")

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
    round(df["humidity_pct"].mean(), 2),
    "%"
)


# ==========================================
# 12. WIND ANALYSIS
# ==========================================

print("\n===================================")
print("WIND ANALYSIS")
print("===================================")

print(
    "Minimum:",
    round(df["wind_speed_mps"].min(), 2),
    "m/s"
)

print(
    "Maximum:",
    round(df["wind_speed_mps"].max(), 2),
    "m/s"
)

print(
    "Average:",
    round(df["wind_speed_mps"].mean(), 2),
    "m/s"
)


# ==========================================
# 13. CORRELATION ANALYSIS
# ==========================================

print("\n===================================")
print("CORRELATION")
print("===================================")

correlation = df[
    [
        "temperature_c",
        "humidity_pct",
        "pressure_hpa",
        "wind_speed_mps",
        "clouds_pct"
    ]
].corr()

print(correlation)


# ==========================================
# 14. SAVE CLEANED DATA
# ==========================================

cleaned_file = "madurai_weather_cleaned.xlsx"

df.to_excel(
    cleaned_file,
    index=False
)

print(
    "\nCleaned dataset saved:",
    cleaned_file
)


# ==========================================
# 15. CREATE CHART FOLDER
# ==========================================

os.makedirs(
    "charts",
    exist_ok=True
)


# ==========================================
# 16. TEMPERATURE TREND
# ==========================================

plt.figure(figsize=(12, 5))

plt.plot(
    df["recorded_at_ist"],
    df["temperature_c"],
    marker="o"
)

plt.title(
    "Madurai Temperature Trend"
)

plt.xlabel(
    "Recorded Time"
)

plt.ylabel(
    "Temperature (°C)"
)

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "charts/temperature_trend.png",
    dpi=150
)

plt.close()


# ==========================================
# 17. HUMIDITY TREND
# ==========================================

plt.figure(figsize=(12, 5))

plt.plot(
    df["recorded_at_ist"],
    df["humidity_pct"],
    marker="o"
)

plt.title(
    "Madurai Humidity Trend"
)

plt.xlabel(
    "Recorded Time"
)

plt.ylabel(
    "Humidity (%)"
)

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "charts/humidity_trend.png",
    dpi=150
)

plt.close()


# ==========================================
# 18. WIND SPEED TREND
# ==========================================

plt.figure(figsize=(12, 5))

plt.plot(
    df["recorded_at_ist"],
    df["wind_speed_mps"],
    marker="o"
)

plt.title(
    "Madurai Wind Speed Trend"
)

plt.xlabel(
    "Recorded Time"
)

plt.ylabel(
    "Wind Speed (m/s)"
)

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "charts/wind_speed_trend.png",
    dpi=150
)

plt.close()


# ==========================================
# 19. WEATHER CONDITION COUNT
# ==========================================

weather_counts.plot(
    kind="bar",
    figsize=(8, 5)
)

plt.title(
    "Madurai Weather Conditions"
)

plt.xlabel(
    "Weather Condition"
)

plt.ylabel(
    "Number of Records"
)

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    "charts/weather_conditions.png",
    dpi=150
)

plt.close()


# ==========================================
# 20. FINAL OUTPUT
# ==========================================

print("\n===================================")
print("EDA COMPLETED SUCCESSFULLY")
print("===================================")

print(
    "Cleaned Excel:",
    cleaned_file
)

print(
    "Charts folder: charts/"
)

print(
    "Total cleaned records:",
    len(df)
)