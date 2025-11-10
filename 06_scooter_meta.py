from __future__ import annotations
from abc import ABC, abstractmethod

class InvalidScooterError(ValueError):
    pass

class ScooterMeta(type):
    registry: dict[str, type["Scooter"]] = {}

    def __new__(mcls, name, bases, namespace, **kwargs):
        # создаем класс 
        cls = super().__new__(mcls, name, bases, namespace)
        # регистрируем  реальные подклассы Scooter
        if name != "Scooter" and any(isinstance(base, ScooterMeta) for base in bases):
            # ключ реестра — имя класса в нижнем регистре или заданный ключ
            key = namespace.get("REGISTRY_KEY", name.lower())
            # сохраняем ссылку на класс в реестре
            ScooterMeta.registry[key] = cls
        return cls

class Scooter(ABC, metaclass=ScooterMeta):
    # абстрактный класс самоката с минимальным набором полей
    def __init__(self, scooter_id: str, model: str, hourly_rate: float):
        # приватные атрибуты
        self.__scooter_id = scooter_id
        self.__model = model
        self.__hourly_rate = hourly_rate
        #  валидация
        if hourly_rate <= 0:
            # ставка должна быть положительной
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
        # абстрактный метод расчета стоимости
        raise NotImplementedError

# пример подкласса
class CityScooter(Scooter):
    def calculate_rental_cost(self, hours: float) -> float:
        return self.hourly_rate * hours

# второй подкласс  собственным ключом
class OffRoadScooter(Scooter):
    REGISTRY_KEY = "off_road"

    def calculate_rental_cost(self, hours: float) -> float:
        # коэф за внедорожность
        return self.hourly_rate * 1.2 * hours

def get_scooter_class(type_key: str) -> type[Scooter] | None:
    # возвращаем класс по ключу из реестра
    return ScooterMeta.registry.get(type_key.lower())
