from __future__ import annotations
from typing import List, Dict, Optional
from dataclasses import dataclass, field

# простые исключения локально, чтобы файл был автономным
class InvalidScooterError(ValueError):
    # ошибка некорректных данных самоката
    pass

@dataclass
class Location:
    """
    Класс Location для композиции со станцией.
    Поля:
      - city: город
      - address: адрес
      - latitude/longitude: координаты (опционально)
    """
    city: str
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    def to_dict(self) -> Dict[str, object]:
        # сериализация местоположения
        return {
            "city": self.city,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, object]) -> "Location":
        # десериализация местоположения
        return cls(
            city=str(d.get("city", "")),
            address=str(d.get("address", "")),
            latitude=d.get("latitude"),  # может быть None
            longitude=d.get("longitude"),
        )

@dataclass(order=False)
class RentalStation:
    """
    Станция аренды (агрегация самокатов).
    Поля:
      - station_id: идентификатор станции
      - capacity: максимальная вместимость
      - location_info: композиция с Location
      - scooters: список самокатов (агрегация, может быть пустым при создании)
    Методы:
      - add_scooter
      - remove_scooter
      - get_available_scooters
    Сравнение (__eq__, __lt__, __gt__):
      - сравниваем по коэффициенту заполнения (занято/вместимость), затем по capacity.
    """
    station_id: str
    capacity: int
    location_info: Location
    scooters: List[object] = field(default_factory=list)

    def add_scooter(self, scooter: object) -> None:
        # добавляем самокат, если есть место
        if len(self.scooters) >= self.capacity:
            # нет свободных слотов
            raise InvalidScooterError("Станция переполнена.")
        # добавляем объект самоката (агрегация, станция не владеет жизненным циклом)
        self.scooters.append(scooter)

    def remove_scooter(self, scooter_id: str) -> bool:
        # удаляем самокат по идентификатору
        for i, s in enumerate(self.scooters):
            # пытаемся прочитать атрибут scooter_id
            sid = getattr(s, "scooter_id", None)
            if sid == scooter_id:
                # удаляем элемент по индексу
                del self.scooters[i]
                return True
        # самокат не найден
        return False

    def get_available_scooters(self) -> List[object]:
        # фильтруем по признаку доступности
        result = []
        for s in self.scooters:
            # читаем атрибут is_available, по умолчанию считаем True
            available = getattr(s, "is_available", True)
            if available:
                result.append(s)
        return result

    def utilization(self) -> float:
        # коэффициент заполнения станции
        if self.capacity <= 0:
            # защита от деления на ноль
            return 0.0
        return len(self.scooters) / float(self.capacity)

    def __eq__(self, other: object) -> bool:
        # равенство по station_id для устойчивости
        if not isinstance(other, RentalStation):
            return NotImplemented
        return self.station_id == other.station_id

    def __lt__(self, other: "RentalStation") -> bool:
        # сначала сравним по коэффициенту заполнения, потом по вместимости
        if self.utilization() != other.utilization():
            return self.utilization() < other.utilization()
        # если одинаково, сравним по capacity
        return self.capacity < other.capacity

    def __gt__(self, other: "RentalStation") -> bool:
        # сначала сравним по коэффициенту заполнения, потом по вместимости
        if self.utilization() != other.utilization():
            return self.utilization() > other.utilization()
        # если одинаково, сравним по capacity
        return self.capacity > other.capacity
