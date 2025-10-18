from abc import ABC, abstractmethod
from typing import Sequence

from .bank_account import BankAccount
from .exceptions import InvalidAmount, InsufficientFunds, IncorrectMenuOption
from .ui import ConsoleUI


class MenuItem(ABC):
    """Абстрактный пункт меню банкомата"""
    def __init__(self, description: str):
        # Название пункта меню, которое будет выводиться пользователю
        self.description = description

    @abstractmethod
    def execute(self, bank_account: BankAccount, ui: ConsoleUI)  -> None:
        """Выполняет действие при выборе этого пункта меню"""
        pass


class CheckBalanceMenuItem(MenuItem):
    """Пункт меню — проверка баланса карты"""
    def __init__(self):
        super().__init__("Проверить баланс")

    def execute(self, bank_account: BankAccount, ui: ConsoleUI) -> None:
        """Показывает пользователю текущий баланс карты"""
        balance = bank_account.get_balance()
        ui.show_message(f"Ваш баланс: {balance} руб.")


class WithdrawMenuItem(MenuItem):
    """Пункт меню — списание денег с баланса карты"""
    def __init__(self):
        super().__init__("Снять деньги")

    def execute(self, bank_account: BankAccount, ui: ConsoleUI) -> None:
        """Выполняет снятие денег с баланса карты"""
        amount = ui.get_input("Сколько вы хотите снять?\nВведите сумму: ")
        balance = bank_account.get_balance()

        if not amount.isdigit():
            raise InvalidAmount("Ошибка ввода! Нужно ввести число.")

        amount = int(amount)

        if amount <= 0:
            raise InvalidAmount("Сумма должна быть больше нуля.")

        if amount > balance:
            raise InsufficientFunds

        bank_account.withdraw(amount)
        ui.show_message(f"Ваш баланс: {bank_account.get_balance()} руб.")


class DepositMenuItem(MenuItem):
    """Пункт меню — пополнение баланса карты"""
    def __init__(self):
        super().__init__("Пополнить счёт")

    def execute(self, bank_account: BankAccount, ui: ConsoleUI) -> None:
        """Выполняет пополнение баланса карты"""
        amount = ui.get_input("Сколько вы хотите внести?\nВведите сумму: ")

        if not amount.isdigit():
            raise InvalidAmount("Ошибка ввода! Нужно ввести число")

        amount = int(amount)

        if amount <= 0:
            raise InvalidAmount("Сумма должна быть больше нуля.")

        bank_account.deposit(amount)
        ui.show_message(f"Ваш баланс: {bank_account.get_balance()} руб.")


class ExitMenuItem(MenuItem):
    """Пункт меню — выход из меню банкомата"""
    def __init__(self):
        super().__init__("Выход")

    def execute(self, bank_account: BankAccount, ui: ConsoleUI) -> None:
        """Выполняет выход из меню банкомата"""
        ui.show_message("Спасибо, что пользуетесь нашим банкоматом!")
        raise SystemExit


class Menu:
    """Меню банкомата"""
    def __init__(self, items: Sequence[MenuItem], ui: ConsoleUI):
        self._items = items
        self._ui = ui

    def show(self) -> None:
        """Выводит список пунктов меню в UI"""
        menu = ["Выберите операцию:"]
        for menu_item_number, menu_item in enumerate(self._items, 1):
            menu.append(f"{menu_item_number} - {menu_item.description}")
        self._ui.show_message("\n".join(menu))

    def get_user_menu_choice(self) -> int:
        """Запрашивает у пользователя пункт меню и возвращает его номер"""
        user_menu_item_choice = self._ui.get_input("Введите номер операции: ")
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