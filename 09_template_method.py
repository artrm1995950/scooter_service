from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Any

# локальные исключения
class InvalidScooterError(ValueError):
    # неверные данные самоката
    pass

class RentalNotFoundError(LookupError):
    # аренда не найдена
    pass

class PermissionDeniedError(PermissionError):
    # нет прав пользователя
    pass

class RentalProcess(ABC):
    """
    Шаблонный метод для процесса аренды.
    Алгоритм rent_scooter:
      1) check_availability
      2) create_rental
      3) confirm_rental
    Подклассы реализуют шаги.
    """
    def rent_scooter(self, scooter_id: str, customer_id: str, hours: float) -> Dict[str, Any]:
        # проверяем доступность самоката
        self.check_availability(scooter_id)
        # создаем запись аренды
        rental = self.create_rental(scooter_id, customer_id, hours)
        # подтверждаем аренду
        self.confirm_rental(rental)
        # возвращаем результат
        return rental

    @abstractmethod
    def check_availability(self, scooter_id: str) -> None:
        # проверяем, что самокат можно арендовать
        raise NotImplementedError

    @abstractmethod
    def create_rental(self, scooter_id: str, customer_id: str, hours: float) -> Dict[str, Any]:
        # создаем объект аренды (словарь или модель)
        raise NotImplementedError

    @abstractmethod
    def confirm_rental(self, rental: Dict[str, Any]) -> None:
        # подтверждаем аренду (уведомление/оплата/печать бумаги)
        raise NotImplementedError

class OnlineRentalProcess(RentalProcess):
    # онлайн-процесс аренды
    def check_availability(self, scooter_id: str) -> None:
        # в реальности проверка в БД/кеше
        if not scooter_id:
            # отсутствие id — ошибка
            raise InvalidScooterError("Некорректный scooter_id.")

    def create_rental(self, scooter_id: str, customer_id: str, hours: float) -> Dict[str, Any]:
        # формируем запись для онлайн-аренды
        return {
            "rental_id": f"ONL-{scooter_id}-{customer_id}",
            "scooter_id": scooter_id,
            "customer_id": customer_id,
            "hours": hours,
            "channel": "online",
            "status": "created",
        }

    def confirm_rental(self, rental: Dict[str, Any]) -> None:
        # подтверждение онлайн (например, письмо/пуш)
        rental["status"] = "confirmed"

class OfflineRentalProcess(RentalProcess):
    # офлайн-процесс аренды (на стойке станции)
    def check_availability(self, scooter_id: str) -> None:
        # проверка доступности через локальный инвентарь станции
        if not scooter_id:
            # отсутствие id — ошибка
            raise InvalidScooterError("Некорректный scooter_id.")

    def create_rental(self, scooter_id: str, customer_id: str, hours: float) -> Dict[str, Any]:
        # формируем запись для офлайн-аренды
        return {
            "rental_id": f"OFF-{scooter_id}-{customer_id}",
            "scooter_id": scooter_id,
            "customer_id": customer_id,
            "hours": hours,
            "channel": "offline",
            "status": "created",
        }

    def confirm_rental(self, rental: Dict[str, Any]) -> None:
        # подтверждение офлайн (печать чека/подпись)
        rental["status"] = "confirmed"
