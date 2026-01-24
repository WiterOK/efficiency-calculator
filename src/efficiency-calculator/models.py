import math
from enum import Enum
from dataclasses import dataclass

class TurbineType(Enum):
    HAWT = "Horizontal"
    VAWT = "Vertical"

@dataclass
class WindTurbine:
    name: str
    type: TurbineType
    hub_height: float
    cp: float
    nominal_speed: float
    cut_in: float = 3.0
    cut_out: float = 25.0
    radius: float = 0.0  # Для HAWT
    height: float = 0.0  # Для VAWT
    width: float = 0.0   # Для VAWT

    @property
    def area(self) -> float:
        if self.type == TurbineType.HAWT:
            return math.pi * self.radius ** 2
        return self.height * self.width