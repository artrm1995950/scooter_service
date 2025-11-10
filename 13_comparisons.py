from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

@dataclass(order=False)
class Rental:
    """
    Модель аренды с методами сравнения.
    Поля:
      - rental_id: идентификатор
      - customer_id: клиент
      - scooter_id: самокат
      - start: время начала
      - hours: длительность
      - cost: итоговая стоимость
    Сравнение:
      - __eq__: по rental_id
      - __lt__/__gt__: сначала по cost, затем по hours
    """
    rental_id: str
    customer_id: str
    scooter_id: str
    start: datetime
    hours: float
    cost: float

    def __eq__(self, other: object) -> bool:
        # равенство по идентификатору аренды
        if not isinstance(other, Rental):
            return NotImplemented
        return self.rental_id == other.rental_id

    def __lt__(self, other: "Rental") -> bool:
        # сначала сравним по итоговой стоимости, затем по длительности
        if self.cost != other.cost:
            return self.cost < other.cost
        # если стоимость равна, сравниваем по длительности
        return self.hours < other.hours

    def __gt__(self, other: "Rental") -> bool:
        # сначала сравним по итоговой стоимости, затем по длительности
        if self.cost != other.cost:
            return self.cost > other.cost
        # если стоимость равна, сравниваем по длительности
        return self.hours > other.hours
