from __future__ import annotations
import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List

# локальные исключения
class InvalidScooterError(ValueError):
    # ошибка при валидации/загрузке самоката
    pass

# базовая модель с to_dict/from_dict
class Scooter(ABC):
    # базовый класс с сериализацией
    TYPE: str = "base"

    def __init__(self, scooter_id: str, model: str, battery_level: int, hourly_rate: float, is_available: bool = True):
        # приватные атрибуты
        self.__scooter_id = scooter_id
        self.__model = model
        self.__battery_level = battery_level
        self.__hourly_rate = hourly_rate
        self.__is_available = is_available

        # базовая валидация
        if not (0 <= self.__battery_level <= 100):
            # проверяем уровень заряда
            raise InvalidScooterError("Уровень заряда должен быть 0..100.")
        if self.__hourly_rate <= 0:
            # проверяем ставку
            raise InvalidScooterError("hourly_rate должен быть > 0.")

    # свойства для инкапсуляции
    @property
    def scooter_id(self) -> str: return self.__scooter_id
    @property
    def model(self) -> str: return self.__model
    @property
    def battery_level(self) -> int: return self.__battery_level
    @property
    def hourly_rate(self) -> float: return self.__hourly_rate
    @property
    def is_available(self) -> bool: return self.__is_available

    @abstractmethod
    def calculate_rental_cost(self, hours: float) -> float:
        # абстрактный метод расчета стоимости
        raise NotImplementedError

    def to_dict(self) -> Dict[str, Any]:
        # базовая сериализация + тип
        return {
            "type": self.TYPE,
            "scooter_id": self.scooter_id,
            "model": self.model,
            "battery_level": self.battery_level,
            "hourly_rate": self.hourly_rate,
            "is_available": self.is_available,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Scooter":
        # фабрика по type с маппингом на конкретные классы
        t = (data.get("type") or "").lower()
        # ищем подходящий класс
        klass = _TYPE_MAP.get(t)
        if klass is None:
            # неизвестный тип — ошибка
            raise InvalidScooterError(f"Неизвестный тип самоката: {data.get('type')!r}")
        # создаем экземпляр, пробрасывая доп. поля
        return klass._from_record(data)

class CityScooter(Scooter):
    # городской самокат
    TYPE = "city"

    def __init__(self, scooter_id: str, model: str, battery_level: int, hourly_rate: float, is_available: bool = True, max_speed: int = 25):
        super().__init__(scooter_id, model, battery_level, hourly_rate, is_available)
        self.max_speed = max_speed

    def calculate_rental_cost(self, hours: float) -> float:
        # линейная стоимость без скидок
        return self.hourly_rate * hours

    def to_dict(self) -> Dict[str, Any]:
        # расширяем базовую сериализацию
        d = super().to_dict()
        d["max_speed"] = self.max_speed
        return d

    @classmethod
    def _from_record(cls, d: Dict[str, Any]) -> "CityScooter":
        # восстанавливаем из словаря
        return cls(
            scooter_id=d["scooter_id"],
            model=d["model"],
            battery_level=d["battery_level"],
            hourly_rate=d["hourly_rate"],
            is_available=d.get("is_available", True),
            max_speed=d.get("max_speed", 25),
        )

class OffRoadScooter(Scooter):
    # внедорожный самокат
    TYPE = "off_road"

    def __init__(self, scooter_id: str, model: str, battery_level: int, hourly_rate: float, is_available: bool = True, tire_type: str = "all-terrain"):
        super().__init__(scooter_id, model, battery_level, hourly_rate, is_available)
        self.tire_type = tire_type

    def calculate_rental_cost(self, hours: float) -> float:
        # коэффициент 1.2 за внедорожность
        return self.hourly_rate * 1.2 * hours

    def to_dict(self) -> Dict[str, Any]:
        # расширяем базовую сериализацию
        d = super().to_dict()
        d["tire_type"] = self.tire_type
        return d

    @classmethod
    def _from_record(cls, d: Dict[str, Any]) -> "OffRoadScooter":
        # восстанавливаем из словаря
        return cls(
            scooter_id=d["scooter_id"],
            model=d["model"],
            battery_level=d["battery_level"],
            hourly_rate=d["hourly_rate"],
            is_available=d.get("is_available", True),
            tire_type=d.get("tire_type", "all-terrain"),
        )

class FoldableScooter(Scooter):
    # складной самокат
    TYPE = "foldable"

    def __init__(self, scooter_id: str, model: str, battery_level: int, hourly_rate: float, is_available: bool = True, weight: float = 12.0):
        super().__init__(scooter_id, model, battery_level, hourly_rate, is_available)
        self.weight = weight

    def calculate_rental_cost(self, hours: float) -> float:
        # скидка 10% при аренде от 4 часов
        base = self.hourly_rate * hours
        # если длительная аренда, применяем скидку
        return base * 0.9 if hours >= 4 else base

    def to_dict(self) -> Dict[str, Any]:
        # расширяем базовую сериализацию
        d = super().to_dict()
        d["weight"] = self.weight
        return d

    @classmethod
    def _from_record(cls, d: Dict[str, Any]) -> "FoldableScooter":
        # восстанавливаем из словаря
        return cls(
            scooter_id=d["scooter_id"],
            model=d["model"],
            battery_level=d["battery_level"],
            hourly_rate=d["hourly_rate"],
            is_available=d.get("is_available", True),
            weight=d.get("weight", 12.0),
        )

# маппинг типов на классы для from_dict
_TYPE_MAP = {
    CityScooter.TYPE: CityScooter,
    OffRoadScooter.TYPE: OffRoadScooter,
    FoldableScooter.TYPE: FoldableScooter,
}

def save_scooters_to_json(scooters: List[Scooter], path: str) -> None:
    # сериализуем список самокатов в JSON
    with open(path, "w", encoding="utf-8") as f:
        json.dump([s.to_dict() for s in scooters], f, ensure_ascii=False, indent=2)

def load_scooters_from_json(path: str) -> List[Scooter]:
    # загружаем список самокатов из JSON
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    # конструируем объекты из словарей
    return [Scooter.from_dict(item) for item in raw]
