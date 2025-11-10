from __future__ import annotations
from functools import wraps

class PermissionDeniedError(PermissionError):
    # нет прав на выполнение операции
    pass

def check_permissions(required: str):
    """
    Декоратор проверки прав. Ожидается, что self.user или именованный аргумент user
    содержит атрибут roles: set[str].
    """
    def decorator(fn):
        # оборачиваем исходную функцию
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # пытаемся получить user из self или kwargs
            user = None
            if args:
                # берем self и читаем поле user
                self_obj = args[0]
                user = getattr(self_obj, "user", None)
            if user is None:
                # пытаемся взять из именованных аргументов
                user = kwargs.get("user")
            if user is None:
                # не найден контекст пользователя
                raise PermissionDeniedError("Пользователь не передан.")
            roles = getattr(user, "roles", set())
            # проверяем наличие требуемой роли
            if required not in roles:
                # недостаточно прав — ошибка
                raise PermissionDeniedError(f"Недостаточно прав: требуется роль '{required}'.")
            # если все ок — вызываем функцию
            return fn(*args, **kwargs)
        return wrapper
    return decorator
