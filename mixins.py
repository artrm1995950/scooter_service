"""
Миксины поведения:
- LoggingMixin: централизованное логирование действий
- NotificationMixin: отправка уведомлений (заглушка)
"""
from __future__ import annotations
from ._logging import logger

class LoggingMixin:
    # общий миксин логирования
    def log_action(self, message: str) -> None:
        # пишем сообщение в логгер подсистемы
        logger.info(message)

class NotificationMixin:
    # отправка уведомлений (заглушка)
    def send_notification(self, recipient: str, message: str) -> None:
        # выводим уведомление в лог для протоколирования
        logger.info(f"Уведомление -> {recipient}: {message}")
