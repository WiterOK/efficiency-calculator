#!/usr/bin/env python3
"""CLI wrapper for the efficiency calculator.
Called by the PHP API; accepts lat/lon arguments and outputs a single JSON line.

Usage:
    python3 cli.py --lat 46.8483 --lon 31.0821 [--year 2023] [--turbine STANDARD_HAWT]

Output (stdout):
    {"result": 12345.67}

Errors are written as JSON to stderr and exit with code 1.
"""
import argparse
import json
import os
import sys

# Ensure local modules resolve correctly when called from outside the directory.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config as cfg  # noqa: E402 (after sys.path patch)
from physics import WindPhysics  # noqa: E402
from services import WeatherService  # noqa: E402

TURBINES = {
    "STANDARD_HAWT": cfg.STANDARD_HAWT,
    "WITEROK": cfg.WITEROK,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Wind turbine annual energy calculator")
    parser.add_argument("--lat",     type=float, required=True,
                        help="Latitude  (-90 … 90)")
    parser.add_argument("--lon",     type=float, required=True,
                        help="Longitude (-180 … 180)")
    parser.add_argument("--year",    type=int,   default=2023,
                        help="Year of historical data to use (default: 2023)")
    parser.add_argument("--turbine", type=str,   default="STANDARD_HAWT",
                        choices=list(TURBINES.keys()),
                        help="Turbine model (default: STANDARD_HAWT)")
    args = parser.parse_args()

    try:
        turbine  = TURBINES[args.turbine]
        api_key  = cfg.OpenWeatherAPIKey()

        if not api_key:
            raise RuntimeError(
                "Missing OPENWEATHER_API_KEY (server env var)."
            )

        service  = WeatherService(args.lat, args.lon, api_key)
        physics  = WindPhysics(cfg.ALPHA)

        elevation    = service.get_elevation()
        weather_data = service.get_yearly_weather(args.year)

        total_kwh = sum(
            physics.calculate_day_energy(record["wind_speed"], elevation, turbine)
            for record in weather_data
        )

        # Single JSON line to stdout — the only thing PHP reads.
        print(json.dumps({"result": round(total_kwh, 2)}))

    except Exception as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
