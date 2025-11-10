from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any

# локальные исключения
class PermissionDeniedError(PermissionError):
    # нет прав для утверждения изменений
    pass

@dataclass
class ChangeRequest:
    """
    Запрос на изменение аренды.
    Поля:
      - rental_id: идентификатор аренды
      - severity: степень изменения (0..100)
      - cost_delta: изменение стоимости (в у.е., может быть отрицательным)
      - notes: пояснения
    """
    rental_id: str
    severity: int
    cost_delta: float
    notes: str = ""

class Handler:
    # базовый обработчик цепочки
    def __init__(self, next_handler: Optional["Handler"] = None):
        # ссылка на следующий обработчик
        self._next = next_handler

    def set_next(self, handler: "Handler") -> "Handler":
        # настраиваем следующий узел
        self._next = handler
        return handler

    def handle(self, request: ChangeRequest) -> Dict[str, Any]:
        # базовая реализация пробрасывает дальше
        if self._next:
            # передаем запрос по цепочке
            return self._next.handle(request)
        # если некому обрабатывать, возвращаем отказ
        return {"approved": False, "by": None, "reason": "Не обработано."}

class StationOperator(Handler):
    # оператор станции: одобряет мелкие изменения
    def handle(self, request: ChangeRequest) -> Dict[str, Any]:
        # правило: может одобрить, если severity <= 20 и abs(cost_delta) <= 10
        if request.severity <= 20 and abs(request.cost_delta) <= 10:
            # одобряем на уровне оператора
            return {"approved": True, "by": "StationOperator", "notes": request.notes}
        # иначе передаем дальше
        return super().handle(request)

class Manager(Handler):
    # менеджер: одобряет умеренные изменения
    def handle(self, request: ChangeRequest) -> Dict[str, Any]:
        # правило: может одобрить, если severity <= 50 и abs(cost_delta) <= 50
        if request.severity <= 50 and abs(request.cost_delta) <= 50:
            # одобряем на уровне менеджера
            return {"approved": True, "by": "Manager", "notes": request.notes}
        # иначе передаем дальше
        return super().handle(request)

class Admin(Handler):
    # администратор: может одобрить любые изменения
    def handle(self, request: ChangeRequest) -> Dict[str, Any]:
        # правило: администратор одобряет всё
        return {"approved": True, "by": "Admin", "notes": request.notes}
