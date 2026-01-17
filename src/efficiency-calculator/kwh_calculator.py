import math

def daily_energy_kwh(v, R, Cp=0.4, rho=1.225):
    if v < 3 or v > 25:
        return 0.0

    A = math.pi * R * R
    P = 0.5 * rho * A * Cp * v**3
    return (P / 1000) * 24


def calculate_year_energy(data, R, Cp=0.4):
    total_energy = 0.0

    for day in data:
        v = day["wind_speed"]
        total_energy += daily_energy_kwh(v, R, Cp)

    return total_energy
