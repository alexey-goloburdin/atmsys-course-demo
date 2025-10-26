from abc import ABC, abstractmethod
from .exceptions import CardNotExists, InsufficientFunds
from .typedefs import Rubles, CardNumber, PIN


class CardRepository(ABC):
    @abstractmethod
    def withdraw(self, card: CardNumber, amount: Rubles) -> None:
        """Снимает amount рублей с баланса карты с номером card"""
        pass
    
    @abstractmethod
    def deposit(self, card: CardNumber, amount: Rubles) -> None:
        """Пополняет баланс карты с номером card на amount рублей""" 
        pass
    
    @abstractmethod
    def get_balance(self, card: CardNumber) -> int:
        """Возвращает баланс карты по её номеру"""
        pass
    
    @abstractmethod
    def is_card_pin_valid(self, card: CardNumber, pin: PIN) -> bool:
        """
        Возвращает True, если пин код соответствует карте.
        Если карты нет в хранилище, падает исключение CardNotExists
        """
        pass


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
    
    def __repr__(self) -> str:
        return (
            f"""{self.__class__.__name__}(card={self._card!r}, """
            f"""card_repository={self._card_repository!r})"""
        )