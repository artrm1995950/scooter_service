"""
Подкласс FoldableScooter (складной).
Переопределяет:
- calculate_rental_cost
- __str__
"""
from __future__ import annotations
from ..01_scooter import Scooter, InvalidScooterError  # базовый класс и исключение
from .mixins import LoggingMixin, NotificationMixin

class FoldableScooter(Scooter, LoggingMixin, NotificationMixin):
    # складной самокат с весом, скидка при долгой аренде
    def __init__(self, scooter_id: str, model: str, battery_level: int, hourly_rate: float, is_available: bool = True, weight: float = 12.0):
        super().__init__(scooter_id, model, battery_level, hourly_rate, is_available)
        self.weight = weight

    def calculate_rental_cost(self, hours: float) -> float:
        # базовая стоимость
        base = self.hourly_rate * hours
        # скидка 10% при аренде от 4 часов
        cost = base * 0.9 if hours >= 4 else base
        # логируем расчет стоимости
        self.log_action(f"Расчет (Foldable): {self.model} — {hours}ч -> {cost:.2f}")
        return cost

    def __str__(self) -> str:
        # выводим вес
        return f"Складной самокат: {self.model}, Вес: {self.weight} кг, Заряд: {self.battery_level}%"
