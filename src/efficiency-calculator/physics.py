import math
from models import WindTurbine

class WindPhysics:
    def __init__(self, alpha: float):
        self.alpha = alpha

    def air_density(self, height_asl: float) -> float:
        return 1.225 * math.exp(-height_asl / 8500.0)

    def wind_at_hub(self, v10: float, hub_height: float) -> float:
        if v10 <= 0 or hub_height <= 0: return 0.0
        return v10 * (hub_height / 10.0) ** self.alpha

    def calculate_day_energy(self, v10: float, height_asl: float, turbine: WindTurbine) -> float:
        v = self.wind_at_hub(v10, turbine.hub_height)
        if v < turbine.cut_in or v > turbine.cut_out:
            return 0.0
        
        v_eff = min(v, turbine.nominal_speed)
        rho = self.air_density(height_asl)
        
        power_watts = 0.5 * rho * turbine.area * turbine.cp * (v_eff ** 3)
        return (power_watts / 1000.0) * 24