"""Enum 커스터마이징 - 메서드, 프로퍼티, __str__"""

from enum import Enum


class Planet(Enum):
    MERCURY = (3.303e+23, 2.4397e6)
    VENUS = (4.869e+24, 6.0518e6)
    EARTH = (5.976e+24, 6.37814e6)
    MARS = (6.421e+23, 3.3972e6)

    def __init__(self, mass: float, radius: float):
        self.mass = mass
        self.radius = radius

    @property
    def surface_gravity(self) -> float:
        """표면 중력 (m/s^2)"""
        G = 6.67300e-11
        return G * self.mass / (self.radius * self.radius)

    def weight_on(self, earth_weight: float) -> float:
        """지구 무게 기준으로 해당 행성에서의 무게를 계산한다."""
        return earth_weight * self.surface_gravity / Planet.EARTH.surface_gravity

    def __str__(self) -> str:
        return f"{self.name.capitalize()} (mass={self.mass:.2e}kg)"

    def __format__(self, format_spec: str) -> str:
        if format_spec == "short":
            return self.name.capitalize()
        return str(self)


class Season(Enum):
    SPRING = "spring"
    SUMMER = "summer"
    AUTUMN = "autumn"
    WINTER = "winter"

    @classmethod
    def from_month(cls, month: int) -> "Season":
        """월(1~12)을 기준으로 계절을 반환한다."""
        if month in (3, 4, 5):
            return cls.SPRING
        elif month in (6, 7, 8):
            return cls.SUMMER
        elif month in (9, 10, 11):
            return cls.AUTUMN
        else:
            return cls.WINTER
