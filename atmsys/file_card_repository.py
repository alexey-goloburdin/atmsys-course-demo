import json
from json.decoder import JSONDecodeError
from pathlib import Path

from .bank_account import CardRepository
from .exceptions import CardNotExists
from .typedefs import PIN, CardNumber, Cards, Rubles


class FileCardRepository(CardRepository):
    """Работа с хранилищем данных по картам"""

    def __init__(self, filename: str):
        self._filename = filename
        self._cards = self._load()

    def withdraw(self, card: CardNumber, amount: Rubles) -> None:
        """Снимает amount рублей с баланса карты с номером card"""
        self._check_card_exists(card)
        self._cards[card]["balance"] -= amount
        self._save()

    def deposit(self, card: CardNumber, amount: Rubles) -> None:
        """Пополняет баланс карты с номером card на amount рублей"""
        self._check_card_exists(card)
        self._cards[card]["balance"] += amount
        self._save()

    def get_balance(self, card: CardNumber) -> int:
        """Возвращает баланс карты по её номеру"""
        self._check_card_exists(card)
        return self._cards[card]["balance"]

    def is_card_pin_valid(self, card: CardNumber, pin: PIN) -> bool:
        """
        Возвращает True, если пин код соответствует карте.
        Если карты нет в хранилище, падает исключение CardNotExists
        """
        self._check_card_exists(card)
        return self._cards[card]["pin"] == pin

    def _check_card_exists(self, card: CardNumber) -> None:
        """
        Проверяет, что карта с переданным номером есть в хранилище,
        иначе возбуждает исключение
        """
        if card not in self._cards:
            raise CardNotExists

    def _load(self) -> Cards:
        Path(self._filename).touch(exist_ok=True)
        with open(self._filename) as f:
            try:
                return json.load(f)
            except JSONDecodeError:
                return {}

    def _save(self):
        with open(self._filename, "w") as f:
            return json.dump(self._cards, f)

    def __repr__(self):
        return f"{self.__class__.__name__}(filename={self._filename!r})"
