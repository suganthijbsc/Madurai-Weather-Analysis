# 🌦️ Madurai Real-Time Weather Analytics

## 📌 Project Overview

A real-time weather data analytics project that collects live weather data for Madurai using the OpenWeather API, stores the data in MySQL, performs data cleaning and exploratory data analysis using Python and Pandas, and presents interactive insights through a Power BI dashboard.

---

## 🎯 Objectives

- Collect real-time weather data using an API
- Store weather observations in MySQL
- Clean and preprocess the dataset using Pandas
- Perform exploratory data analysis
- Analyze temperature, humidity, wind speed and weather conditions
- Build an interactive Power BI dashboard
- Generate visual insights for weather monitoring

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Requests
- MySQL
- MySQL Connector
- Matplotlib
- Power BI
- Excel
- OpenWeather API

---

## 🔄 Project Workflow

OpenWeather API
↓
Python
↓
MySQL Database
↓
Pandas Data Cleaning
↓
Exploratory Data Analysis
↓
Excel Dataset
↓
Power BI Dashboard

---

## 📊 Dataset

The project contains 101 weather observations collected for Madurai.

### Main Features

- Temperature
- Feels Like Temperature
- Minimum Temperature
- Maximum Temperature
- Humidity
- Atmospheric Pressure
- Visibility
- Wind Speed
- Wind Direction
- Cloud Coverage
- Weather Condition
- Weather Description
- Latitude
- Longitude
- Recorded Timestamp

---

## 🧹 Data Cleaning

The following preprocessing steps were performed:

- Checked duplicate records
- Converted datetime fields
- Converted numeric columns to appropriate data types
- Checked missing values
- Filled missing numeric values where appropriate
- Filled missing text values
- Created date and time features
- Performed temperature outlier detection using IQR

---

## 🔎 Exploratory Data Analysis

### Temperature

- Minimum: 27.99 °C
- Maximum: 36.99 °C
- Average: 32.45 °C

### Humidity

- Minimum: 44%
- Maximum: 74%
- Average: 58.82%

### Wind Speed

- Minimum: 1.03 m/s
- Maximum: 7.20 m/s
- Average: 3.35 m/s

### Weather Conditions

- Clouds: 61 records
- Rain: 40 records

No duplicate records were identified, and no temperature outliers were detected using the IQR method.

---

## 📊 Power BI Dashboard

The dashboard provides:

- Latest Temperature
- Latest Humidity
- Latest Wind Speed
- Total Records
- Temperature Trend
- Humidity Trend
- Wind Speed Trend
- Weather Condition Distribution
- Temperature vs Humidity Analysis
- Current Weather Information
- Date/Time Filtering

---

## 📈 Key Insights

- The observed temperature ranged from 27.99 °C to 36.99 °C.
- Average recorded temperature was 32.45 °C.
- Cloudy conditions represented 61 of the 101 observations.
- Rain conditions represented 40 observations.
- Average humidity was 58.82%.
- Average wind speed was 3.35 m/s.
- No temperature outliers were detected in the collected dataset.

---

## 📁 Project Structure

Madurai_Weather_Analysis/

├── weather.py  
├── eda.py  
├── .env  
├── madurai_weather_cleaned.xlsx  
├── charts/  
│   ├── temperature_trend.png  
│   ├── humidity_trend.png  
│   ├── wind_speed_trend.png  
│   └── weather_conditions.png  
└── README.md

---

## 🚀 Future Improvements

- Add multiple cities
- Store data continuously using scheduled jobs
- Increase historical data collection
- Add weather forecasting
- Add automated Power BI refresh
- Deploy the pipeline to a cloud environment

---

## 👨‍💻 Skills Demonstrated

Python | Pandas | SQL | MySQL | API Integration | Data Cleaning | EDA | Data Visualization | Power BI | Excel