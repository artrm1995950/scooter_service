"""
Логирование для подсистемы поведения самокатов.

Создает логгер "scooter.behavior" с двумя обработчиками:
- консоль
- файл scooter_behavior.log
"""
from __future__ import annotations
import logging

# создаем/получаем именованный логгер
logger = logging.getLogger("scooter.behavior")
logger.setLevel(logging.INFO)

# общий формат сообщений
_fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

# обработчик консоли
_console = logging.StreamHandler()
_console.setFormatter(_fmt)
_console.setLevel(logging.INFO)

# обработчик файла
_file = logging.FileHandler("scooter_behavior.log", encoding="utf-8")
_file.setFormatter(_fmt)
_file.setLevel(logging.INFO)

# добавляем обработчики один раз
if not logger.handlers:
    # сначала добавляем консоль
    logger.addHandler(_console)
    # затем файл
    logger.addHandler(_file)
