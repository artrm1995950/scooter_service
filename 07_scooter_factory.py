from __future__ import annotations
from abc import ABC, abstractmethod

class InvalidScooterError(ValueError):
    pass

class Scooter(ABC):
    # базовый класс самоката для фабрики
    def __init__(self, scooter_id: str, model: str, hourly_rate: float):
        # приватные поля
        self.__scooter_id = scooter_id
        self.__model = model
        self.__hourly_rate = hourly_rate
        if hourly_rate <= 0:
            # почасовая ставка должна быть положительной
            raise InvalidScooterError("hourly_rate должен быть > 0.")

    @property
    def scooter_id(self) -> str:
        return self.__scooter_id

    @property
    def model(self) -> str:
        return self.__model

    @property
    def hourly_rate(self) -> float:
        return self.__hourly_rate

    @abstractmethod
    def calculate_rental_cost(self, hours: float) -> float:
        # абстрактный метод стоимости
        raise NotImplementedError

class CityScooter(Scooter):
    # городской самокат с  формулой
    def __init__(self, scooter_id: str, model: str, hourly_rate: float, max_speed: int = 25):
        super().__init__(scooter_id, model, hourly_rate)
        self.max_speed = max_speed

    def calculate_rental_cost(self, hours: float) -> float:
        # линейная стоимость без коэффициентов
        return self.hourly_rate * hours

class OffRoadScooter(Scooter):
    # внедорожный самокат с коэффициентом
    def __init__(self, scooter_id: str, model: str, hourly_rate: float, tire_type: str = "all-terrain"):
        super().__init__(scooter_id, model, hourly_rate)
        self.tire_type = tire_type

    def calculate_rental_cost(self, hours: float) -> float:
        # коэффициент 1.2 за внедорожность
        return self.hourly_rate * 1.2 * hours

class FoldableScooter(Scooter):
    # складной самокат со скидкой
    def __init__(self, scooter_id: str, model: str, hourly_rate: float, weight: float = 12.0):
        super().__init__(scooter_id, model, hourly_rate)
        self.weight = weight

    def calculate_rental_cost(self, hours: float) -> float:
        # скидка 10% при аренде от 4 часов
        base = self.hourly_rate * hours
        # если длительная аренда, применяем скидку
        return base * 0.9 if hours >= 4 else base

class ScooterFactory:
    # фабрика по созданию самокатов
    TYPES = {
        "city": CityScooter,
        "off_road": OffRoadScooter,
        "foldable": FoldableScooter,
    }

    @staticmethod
    def create_scooter(scooter_type: str, **kwargs) -> Scooter:
        # находим класс по ключу
        cls = ScooterFactory.TYPES.get(scooter_type.lower())
        if cls is None:
            # неизвестный тип — ошибка
            raise InvalidScooterError(f"Неизвестный тип самоката: {scooter_type!r}")
        # создаем экземпляр, пробрасывая именованные аргументы
        return cls(**kwargs)
