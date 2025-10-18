from .card_repository import CardRepository
from .exceptions import CardNotExists, InsufficientFunds
from .typedefs import Rubles, CardNumber, PIN


class BankAccount:
    """Работа с банковским счётом — пополнение баланса, снятие денег"""
    def __init__(self, card: CardNumber, card_repository: CardRepository):
        self._card = card
        self._card_repository = card_repository

    def withdraw(self, amount: Rubles) -> None:
        """Снимает amount рублей с баланса карты"""
        if self._card_repository.get_balance(self._card) < amount:
            raise InsufficientFunds
        self._card_repository.withdraw(self._card, amount)

    def deposit(self, amount: Rubles) -> None:
        """Пополняет баланс карты на amount рублей""" 
        self._card_repository.deposit(self._card, amount)
    
    def get_balance(self) -> int:
        """Возвращает баланс карты"""
        return self._card_repository.get_balance(self._card)

    def is_pin_code_valid(self, pin: PIN):
        """
        Возвращает True, если переданная карта найдена и её пин-код соответствует переданному,
        иначе возвращает False
        """
        try:
            return self._card_repository.is_card_pin_valid(self._card, pin)
        except CardNotExists:
            return False