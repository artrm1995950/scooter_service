"""
Интерфейсы сервиса аренды:
- Rentable: операции аренды
- Reportable: генерация отчетов
"""
from __future__ import annotations
from typing import Protocol, runtime_checkable, Dict, Any

@runtime_checkable
class Rentable(Protocol):
    # интерфейс аренды: возвращает детали операции
    def rent_scooter(self, scooter_id: str, customer_id: str, hours: float) -> Dict[str, Any]: ...

@runtime_checkable
class Reportable(Protocol):
    # интерфейс отчетности: возвращает текст отчета
    def generate_report(self) -> str: ...
