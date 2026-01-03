# Wind Turbine Efficiency Estimator (WIP)

Early-stage project for estimating wind turbine efficiency at a given geographic location using real meteorological data.

The goal is to combine weather data with basic wind-energy physics to evaluate how suitable a location is for wind power generation.

---

## Current state

This project is in an early development stage.

At the moment, it:
- Fetches hourly meteorological data from **OpenWeather One Call API 3.0**
- Parses wind and atmospheric parameters needed for further modeling

No energy or efficiency calculations are implemented yet.

---

## Planned functionality

The project is intended to:
- Convert wind data and turbine properties to estimated returns in value of the turbine at given points
- Compute air density from temperature and pressure
- Estimate wind power and turbine output
- Calculate energy production over time
- Evaluate site efficiency / capacity factor if WiterOK turbines

---

## Data source

- OpenWeather **One Call API 3.0**
- Hourly fields used:
  - wind speed
  - wind direction
  - temperature
  - pressure

---

## Setup

1. Create an OpenWeather API key with **One Call API 3.0** enabled
2. Store the key as an environment variable:
   ```bash
   export OPENWEATHER_API_KEY="your_key_here"
3. Install all dependencies and run the main script with:
    ```bash
    python main.py