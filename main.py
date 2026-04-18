import os
import sys
from typing import Literal, Optional

from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


# Allow importing the existing calculator modules (they live in src/efficiency-calculator).
MODULE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "efficiency-calculator")
sys.path.insert(0, MODULE_DIR)

import config as cfg  # noqa: E402
from physics import WindPhysics  # noqa: E402
from services import WeatherService  # noqa: E402


class CalculateRequest(BaseModel):
    value1: float = Field(..., ge=-90.0, le=90.0, description="Latitude")
    value2: float = Field(..., ge=-180.0, le=180.0, description="Longitude")
    year: int = Field(2023, ge=2000, le=2030)
    turbine: Literal["STANDARD_HAWT", "WITEROK"] = "STANDARD_HAWT"


app = FastAPI()


frontend_origin = os.getenv("FRONTEND_ORIGIN")
if frontend_origin:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[frontend_origin],
        allow_credentials=False,
        allow_methods=["POST", "OPTIONS"],
        allow_headers=["Content-Type", "X-Api-Key"],
    )
else:
    # If you haven't configured a frontend yet, keep CORS permissive.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
def root() -> dict:
    return {"ok": True}


@app.post("/api/calculate")
def calculate(payload: CalculateRequest, x_api_key: Optional[str] = Header(None)):
    required_api_key = os.getenv("API_KEY", "")
    if required_api_key:
        if not x_api_key or x_api_key != required_api_key:
            return JSONResponse(
                status_code=401,
                content={"error": "Unauthorized: invalid or missing X-Api-Key header"},
            )

    if not os.getenv("OPENWEATHER_API_KEY"):
        return JSONResponse(
            status_code=401,
            content={"error": "Missing OPENWEATHER_API_KEY"},
        )

    try:
        turbine = cfg.STANDARD_HAWT if payload.turbine == "STANDARD_HAWT" else cfg.WITEROK
        service = WeatherService(payload.value1, payload.value2, cfg.OpenWeatherAPIKey())
        physics = WindPhysics(cfg.ALPHA)

        elevation = service.get_elevation()
        weather_data = service.get_yearly_weather(payload.year)

        total_kwh = sum(
            physics.calculate_day_energy(record["wind_speed"], elevation, turbine)
            for record in weather_data
        )

        return {"result": round(float(total_kwh), 2)}
    except Exception as exc:
        return JSONResponse(status_code=500, content={"error": str(exc)})


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
