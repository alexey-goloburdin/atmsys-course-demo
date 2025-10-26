from abc import ABC, abstractmethod
from typing import Sequence

from .bank_account import BankAccount
from .exceptions import InvalidAmount, InsufficientFunds, IncorrectMenuOption
from .ui_messages import UiMessage


class UI(ABC):
    """Пользовательский интерфейс банкомата"""
    @abstractmethod
    def show_message(self, message: str) -> None:
        """Показывает сообщение message пользователю"""
        ...

    @abstractmethod
    def get_input(self, prompt: str) -> str:
        """Запрашивает данные у пользователя и возвращает их"""
        ...

    @abstractmethod
    def show_separator(self) -> None:
        """Показывает визуальный разделитель"""
        ...


class MenuItem(ABC):
    """Абстрактный пункт меню банкомата"""
    def __init__(self, description: str):
        # Название пункта меню, которое будет выводиться пользователю
        self.description = description

    @abstractmethod
    def execute(self, bank_account: BankAccount, ui: UI)  -> None:
        """Выполняет действие при выборе этого пункта меню"""
        pass


class CheckBalanceMenuItem(MenuItem):
    """Пункт меню — проверка баланса карты"""
    def __init__(self):
        super().__init__(UiMessage.MENU_GET_BALANCE_ITEM)

    def execute(self, bank_account: BankAccount, ui: UI) -> None:
        """Показывает пользователю текущий баланс карты"""
        balance = bank_account.get_balance()
        ui.show_message(UiMessage.BALANCE.format(balance=balance))


class WithdrawMenuItem(MenuItem):
    """Пункт меню — списание денег с баланса карты"""
    def __init__(self):
        super().__init__(UiMessage.MENU_WITHDRAW_ITEM)

    def execute(self, bank_account: BankAccount, ui: UI) -> None:
        """Выполняет снятие денег с баланса карты"""
        amount = ui.get_input(UiMessage.HOW_MUCH_WITHDRAW_INPUT)
        balance = bank_account.get_balance()

        if not amount.isdigit():
            raise InvalidAmount(UiMessage.AMOUNT_MUST_BE_DIGIT)

        amount = int(amount)

        if amount <= 0:
            raise InvalidAmount(UiMessage.AMOUNT_MUST_BE_POSITIVE)

        if amount > balance:
            raise InsufficientFunds

        bank_account.withdraw(amount)
        ui.show_message(UiMessage.BALANCE.format(
            balance=bank_account.get_balance())
        )


class DepositMenuItem(MenuItem):
    """Пункт меню — пополнение баланса карты"""
    def __init__(self):
        super().__init__(UiMessage.MENU_DEPOSIT_ITEM)

    def execute(self, bank_account: BankAccount, ui: UI) -> None:
        """Выполняет пополнение баланса карты"""
        amount = ui.get_input(UiMessage.HOW_MUCH_DEPOSIT_INPUT)

        if not amount.isdigit():
            raise InvalidAmount(UiMessage.AMOUNT_MUST_BE_DIGIT)

        amount = int(amount)

        if amount <= 0:
            raise InvalidAmount(UiMessage.AMOUNT_MUST_BE_POSITIVE)

        bank_account.deposit(amount)
        ui.show_message(UiMessage.BALANCE.format(balance=bank_account.get_balance()))


class ExitMenuItem(MenuItem):
    """Пункт меню — выход из меню банкомата"""
    def __init__(self):
        super().__init__(UiMessage.MENU_EXIT_ITEM)

    def execute(self, bank_account: BankAccount, ui: UI) -> None:
        """Выполняет выход из меню банкомата"""
        ui.show_message(UiMessage.GOODBYE)
        raise SystemExit


class Menu:
    """Меню банкомата"""
    def __init__(self, items: Sequence[MenuItem], ui: UI):
        self._items = items
        self._ui = ui

    def show(self) -> None:
        """Выводит список пунктов меню в UI"""
        menu: list[str] = [UiMessage.MENU_CHOOSE_ITEM]
        for menu_item_number, menu_item in enumerate(self._items, 1):
            menu.append(f"{menu_item_number} - {menu_item.description}")
        self._ui.show_message("\n".join(menu))

    def get_user_menu_choice(self) -> int:
        """Запрашивает у пользователя пункт меню и возвращает его номер"""
        user_menu_item_choice = self._ui.get_input(UiMessage.MENU_NUMBER_INPUT)
        if not self._is_user_menu_item_choice_valid(user_menu_item_choice):
            raise IncorrectMenuOption
        return int(user_menu_item_choice)

    def get_menu_min_max_numbers(self) -> tuple[int, int]:
        """Возвращает min и max номера пунктов меню"""
        min_choice = 1
        max_choice = len(self._items)
        return min_choice, max_choice

    def execute_item(self, user_menu_item_choice: int, bank_account: BankAccount) -> None:
        """Выполняет логику пункта меню под номером number, нумерация начинается с единицы"""
        self._items[user_menu_item_choice - 1].execute(bank_account, self._ui)

    def _is_user_menu_item_choice_valid(self, user_menu_item_choice: str) -> bool:
        """
        Возвращает True, если пользователем выбран корректный пункт меню, иначе False
        """
        if not user_menu_item_choice.isdigit():
            return False
        min_choice_number, max_choice_number = self.get_menu_min_max_numbers()
        return min_choice_number <= int(user_menu_item_choice) <= max_choice_number