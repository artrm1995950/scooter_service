
class InvalidScooterError(ValueError):
    # ошибка некорректных данных самоката
    pass

class PermissionDeniedError(PermissionError):
    # ошибка отсутствия прав на выполнение операции
    pass

class RentalNotFoundError(LookupError):
    # ошибка отсутствия записи об аренде
    pass
