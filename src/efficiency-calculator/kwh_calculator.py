from tqdm import tqdm
from apifetcher import load_from_cache, save_to_cache, GetMeteodata
from timestamps import NormalizeYear, GenerateUnixTimestamps
import config
import math

# =========================
# КОНФІГУРАЦІЯ
# =========================

LAT = config.LAT
LON = config.LON
YEAR = config.YEAR
R = config.R                      # радіус ротора (м)
API_KEY = config.OpenWeatherAPIKey()

H_HUB = 80.0                      # висота втулки (м) — стандартне значення
HEIGHT_ASL = 150.0                # TODO: тимчасово. Висота над рівнем моря (м), замінити API
CP = 0.4
ALPHA = 0.2
CUT_IN = 3.0
CUT_OUT = 25.0

AREA = math.pi * R**2


# =========================
# ФІЗИЧНІ ФУНКЦІЇ
# =========================

def air_density(height_asl_m: float) -> float:
    return 1.225 * math.exp(-height_asl_m / 8500.0)


def wind_speed_at_hub(v10: float) -> float:
    return v10 * (H_HUB / 10.0) ** ALPHA


def turbine_power(v10: float, height_asl_m: float) -> float:
    v = wind_speed_at_hub(v10)

    if v < CUT_IN or v > CUT_OUT:
        return 0.0

    rho = air_density(height_asl_m)
    return 0.5 * rho * AREA * CP * v**3


def energy_per_hour(v10: float, height_asl_m: float) -> float:
    return turbine_power(v10, height_asl_m) / 1000.0


def calculate_year_energy(data: list[dict], height_asl_m: float) -> float:
    """
    data: список словників з ключами 'ts', 'wind_speed'
    wind_speed — середня швидкість за добу (м/с)
    """

    total_energy = 0.0

    for entry in data:
        v10 = entry["wind_speed"]

        # енергія за 1 годину
        e_hour = energy_per_hour(v10, height_asl_m)

        # масштабування: 1 запис = 24 години
        total_energy += e_hour * 24

    return total_energy