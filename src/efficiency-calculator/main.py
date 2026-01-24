import config
from services import WeatherService
from physics import WindPhysics

def main():
    weather_svc = WeatherService(config.LAT, config.LON, config.OpenWeatherAPIKey())
    physics = WindPhysics(config.ALPHA)
    
    asl = weather_svc.get_elevation()
    weather_data = weather_svc.get_yearly_weather(config.YEAR)
    
    # WITeRoK or STANDARD_HAWT
    turbine = config.STANDARD_HAWT
    total_kwh = sum(physics.calculate_day_energy(d["wind_speed"], asl, turbine) for d in weather_data)
    
    print(f"\n--- {turbine.name} Annual Report ---")
    print(f"Energy Production: {total_kwh:,.2f} kWh")
    print(f"Average Power: {(total_kwh/8760)*1000:.2f} Watts")
    
    speeds = [d["wind_speed"] for d in weather_data]
    
    print("-" * 30)
    if speeds:
        print(f"Min/Max wind speed: {min(speeds)} {max(speeds)}")
        print(f"Average wind speed: {sum(speeds)/len(speeds)}")
    
    print(f"Height: {asl} m")
    print(f"Days: {len(weather_data)}")

if __name__ == "__main__":
    main()