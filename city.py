"""
Подкласс CityScooter (городской).
Переопределяет:
- calculate_rental_cost
- __str__
"""
from __future__ import annotations
from typing import Final
from ..01_scooter import Scooter, InvalidScooterError  # базовый класс и исключение
from .mixins import LoggingMixin, NotificationMixin

class CityScooter(Scooter, LoggingMixin, NotificationMixin):
    # городской самокат с максимальной скоростью
    def __init__(self, scooter_id: str, model: str, battery_level: int, hourly_rate: float, is_available: bool = True, max_speed: int = 25):
        super().__init__(scooter_id, model, battery_level, hourly_rate, is_available)
        self.max_speed: Final[int] = max_speed

    def calculate_rental_cost(self, hours: float) -> float:
        # линейная стоимость без коэффициентов
        cost = self.hourly_rate * hours
        # логируем расчет для аудита
        self.log_action(f"Расчет (City): {self.model} — {hours}ч -> {cost:.2f}")
        return cost

    def __str__(self) -> str:
        # выводим тип и максимальную скорость
        return f"Городской самокат: {self.model}, Макс. скорость: {self.max_speed} км/ч, Заряд: {self.battery_level}%"
