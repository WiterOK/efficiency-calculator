# Wind Turbine Efficiency Estimator (WIP)

Early-stage project for estimating wind turbine efficiency at a given geographic location using real meteorological data.

The goal is to combine weather data with basic wind-energy physics to evaluate how suitable a location is for wind power generation.

---

## Functionality and TODO

- [x] Base project structure
- [x] Separate API keys
- [x] Fetching meteorological data from OpenWeather API
- [x] Local data caching
- [x] Separate configuration file

- [ ] Define the data calculation process in kWh
- [ ] Express the calculation process as a single formula
- [ ] Implement the calculation process as a function (separate package)
- [ ] Build a basic UI
- [ ] Move all constants to `config.py`
- [ ] Research proper cache handling strategies
- [ ] Refactor UI to production-ready quality
- [ ] Expose logic via API / integrate based on team requirements
- [ ] Implement full report generation (PDF)
- [ ] Research instant payment methods for the website
- [ ] Make full report generation a paid feature

---

## Planned functionality

The project is intended to:
- Convert wind data and turbine properties to estimated turbine value at given locations
- Compute air density from temperature and pressure
- Estimate wind power and turbine output
- Calculate energy production over time
- Evaluate site efficiency / capacity factor for WiterOK turbines

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
