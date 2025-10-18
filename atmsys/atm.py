from .bank_account import BankAccount
from .card_repository import CardRepository
from .exceptions import (
    ATMException,
    CardNotExists, 
    IncorrectMenuOption,
    InsufficientFunds,
    InvalidAmount,
    PinCodeAttemptsExceed 
)
from .menu import Menu
from .ui import ConsoleUI


MAX_PIN_INPUT_ATTEMPTS = 3


class ATM:
    """Управляющая логика банкомата"""

    def __init__(self,
                 card_repository: CardRepository,
                 ui: ConsoleUI,
                 menu: Menu,
                 max_pin_input_attempts: int=MAX_PIN_INPUT_ATTEMPTS):
        self._card_repository = card_repository
        self._ui = ui
        self._menu = menu
        self._max_pin_input_attempts = max_pin_input_attempts
        # Банковский аккаунт установится после прохождения аутентификации 
        self._bank_account: BankAccount  
    
    def run(self):
        """Запускает работу банкомата"""
        self._ui.show_message("Добро пожаловать в банкомат!")
        try:
            self._authenticate()
        except PinCodeAttemptsExceed:
            self._ui.show_message("Карта заблокирована. Обратитесь в банк.")
            raise SystemExit
        assert self._bank_account is not None
                
        while True:
            self._ui.show_separator()
            self._menu.show()

            try:
                user_menu_item_choice = self._menu.get_user_menu_choice()
            except IncorrectMenuOption:
                min_choice, max_choice = self._menu.get_menu_min_max_numbers()
                self._ui.show_message(f"Ошибка ввода. Введите число от "
                                      f"{min_choice} до {max_choice}.")
                continue

            self._ui.show_separator()
            try:
                self._menu.execute_item(user_menu_item_choice, self._bank_account)
            except InvalidAmount as e:
                self._ui.show_message(str(e))
            except InsufficientFunds:
                self._ui.show_message("Недостаточно средств для снятия со счёта")
            except CardNotExists:
                self._ui.show_message("Извините, карта не найдена")
            except ATMException:
                self._ui.show_message("Извините, что-то пошло не так")

    def _authenticate(self) -> bool:
        """
        Выполняет аутентификацию пользователя, запрашивая и проверяя номер
        карты и пин-код
        """
        user_card_number = (
            self._ui.get_input("Введите номер карты: ").replace(" ", "").strip()
        )

        attempts_remaining = self._max_pin_input_attempts
        while attempts_remaining > 0:
            user_card_pin = self._ui.get_input("Введите PIN: ").replace(" ", "").strip()
            bank_account = BankAccount(user_card_number, self._card_repository)

            if bank_account.is_pin_code_valid(user_card_pin):
                self._ui.show_message("PIN принят. Добро пожаловать!")
                self._bank_account = bank_account
                return True
            else:
                attempts_remaining -= 1
                if attempts_remaining > 0:
                    self._ui.show_message(f"Неверный PIN. Осталось попыток: "
                                          f"{attempts_remaining}")
        else:
            raise PinCodeAttemptsExceed