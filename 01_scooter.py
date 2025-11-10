from __future__ import annotations
from abc import ABC, abstractmethod

# валидация входных данных
class InvalidScooterError(ValueError):
    pass

class Scooter(ABC):
    def __init__(self, scooter_id: str, model: str, battery_level: int, hourly_rate: float, is_available: bool = True):
        # приватные атрибуты 
        self.__scooter_id = scooter_id
        self.__model = model
        self.__battery_level = battery_level
        self.__hourly_rate = hourly_rate
        self.__is_available = is_available

        # валидация с данных
        if not (0 <= self.__battery_level <= 100):
            # заряд от 0 до 100
            raise InvalidScooterError("Уровень заряда должен быть в диапазоне 0..100.")
        if self.__hourly_rate <= 0:
            raise InvalidScooterError("hourly_rate должен быть > 0.")

    # геттер для идентификатора
    @property
    def scooter_id(self) -> str:
        return self.__scooter_id

    # геттер/сеттер для модели
    @property
    def model(self) -> str:
        return self.__model

    @model.setter
    def model(self, value: str) -> None:
        if not value:
            raise InvalidScooterError("Модель не может быть пустой.")
        self.__model = value

    # геттер/сеттер для уровня заряда
    @property
    def battery_level(self) -> int:
        return self.__battery_level

    @battery_level.setter
    def battery_level(self, value: int) -> None:
        # уровень заряда должен быть от 0 до 100
        if not (0 <= value <= 100):
            raise InvalidScooterError("Уровень заряда должен быть 0..100.")
        self.__battery_level = value

    # геттер/сеттер для почасовой ставки
    @property
    def hourly_rate(self) -> float:
        return self.__hourly_rate

    @hourly_rate.setter
    def hourly_rate(self, value: float) -> None:
        # почасовая ставка должна быть положительной
        if value <= 0:
            raise InvalidScooterError("hourly_rate должен быть > 0.")
        self.__hourly_rate = value

    # геттер/сеттер доступности
    @property
    def is_available(self) -> bool:
        return self.__is_available

    @is_available.setter
    def is_available(self, value: bool) -> None:
        # приводим к bool для единообразия
        self.__is_available = bool(value)

    @abstractmethod
    def calculate_rental_cost(self, hours: float) -> float:
        # абстрактный метод для расчета стоимости аренды
        raise NotImplementedError

    def __str__(self) -> str:
        #  строковое представление объекта
        return f"Самокат: {self.model}, Заряд: {self.battery_level}%"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Scooter):
            return NotImplemented
        return (self.hourly_rate, self.battery_level, self.model) == (other.hourly_rate, other.battery_level, other.model)

    def __lt__(self, other: "Scooter") -> bool:
        # сравнние по ставке 
        if not isinstance(other, Scooter):
            return NotImplemented
        if self.hourly_rate != other.hourly_rate:
            return self.hourly_rate < other.hourly_rate
        # если ставки равны, сравниваем по заряду
        return self.battery_level < other.battery_level

    def __gt__(self, other: "Scooter") -> bool:
        if not isinstance(other, Scooter):
            return NotImplemented
        if self.hourly_rate != other.hourly_rate:
            return self.hourly_rate > other.hourly_rate
        # если ставки равны, сравниваем по заряду
        return self.battery_level > other.battery_level
