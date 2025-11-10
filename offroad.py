"""
Подкласс OffRoadScooter (внедорожный).
Переопределяет:
- calculate_rental_cost
- __str__
"""
from __future__ import annotations
from ..01_scooter import Scooter, InvalidScooterError  # базовый класс и исключение
from .mixins import LoggingMixin, NotificationMixin

class OffRoadScooter(Scooter, LoggingMixin, NotificationMixin):
    # внедорожный самокат с типом шин
    def __init__(self, scooter_id: str, model: str, battery_level: int, hourly_rate: float, is_available: bool = True, tire_type: str = "all-terrain"):
        super().__init__(scooter_id, model, battery_level, hourly_rate, is_available)
        self.tire_type = tire_type

    def calculate_rental_cost(self, hours: float) -> float:
        # коэффициент 1.2 за внедорожность
        cost = self.hourly_rate * 1.2 * hours
        # логируем расчет стоимости
        self.log_action(f"Расчет (OffRoad): {self.model} — {hours}ч -> {cost:.2f}")
        return cost

    def __str__(self) -> str:
        # выводим тип шин
        return f"Внедорожный самокат: {self.model}, Шины: {self.tire_type}, Заряд: {self.battery_level}%"
