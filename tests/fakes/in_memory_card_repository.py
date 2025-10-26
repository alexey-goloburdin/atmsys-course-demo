from atmsys.bank_account import CardRepository
from atmsys.exceptions import CardNotExists
from atmsys.typedefs import PIN, CardNumber, Cards, Rubles


class InMemoryCardRepository(CardRepository):
    """Работа с хранилищем данных по картам"""

    def __init__(self, cards: Cards):
        self._cards = cards

    def withdraw(self, card: CardNumber, amount: Rubles) -> None:
        """Снимает amount рублей с баланса карты с номером card"""
        self._check_card_exists(card)
        self._cards[card]["balance"] -= amount

    def deposit(self, card: CardNumber, amount: Rubles) -> None:
        """Пополняет баланс карты с номером card на amount рублей"""
        self._check_card_exists(card)
        self._cards[card]["balance"] += amount

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
