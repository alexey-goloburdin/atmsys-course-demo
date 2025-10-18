class ATMException(Exception):
    """Базовое исключение для банкомата"""
    pass


class PinCodeAttemptsExceed(ATMException):
    """Закончились попытки ввода пин-кода"""
    pass


class InvalidAmount(ATMException):
    """Некорректная сумма денег"""


class InsufficientFunds(ATMException):
    """Недостаточно средств для снятия со счёта"""


class IncorrectMenuOption(ATMException):
    """Выбран некорректный пункт меню"""


class CardNotExists(ATMException):
    """Некорректный номер карты, её нет в нашем хранилище"""