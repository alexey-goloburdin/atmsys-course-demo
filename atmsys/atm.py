from .bank_account import BankAccount, CardRepository
from .exceptions import (
    ATMException,
    CardNotExists, 
    IncorrectMenuOption,
    InsufficientFunds,
    InvalidAmount,
    PinCodeAttemptsExceed 
)
from .menu import Menu, UI
from .ui_messages import UiMessage


MAX_PIN_INPUT_ATTEMPTS = 3


class ATM:
    """Управляющая логика банкомата"""

    def __init__(self,
                 card_repository: CardRepository,
                 ui: UI,
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
        self._ui.show_message(UiMessage.GREETINGS)
        try:
            self._authenticate()
        except PinCodeAttemptsExceed:
            self._ui.show_message(UiMessage.CARD_BLOCKED)
            raise SystemExit
        assert self._bank_account is not None
                
        while True:
            self._ui.show_separator()
            self._menu.show()

            try:
                user_menu_item_choice = self._menu.get_user_menu_choice()
            except IncorrectMenuOption:
                min_choice, max_choice = self._menu.get_menu_min_max_numbers()
                self._ui.show_message(
                    UiMessage.INCORRECT_MENU_ITEM.format(
                        min_choice=min_choice, max_choice=max_choice
                    )
                )
                continue

            self._ui.show_separator()
            self._execute_menu_item(user_menu_item_choice)

    def _execute_menu_item(self, user_menu_item_choice: int) -> None:
        """Выполняет логику выбранного пользователем пунтка меню"""
        try:
            self._menu.execute_item(user_menu_item_choice, self._bank_account)
        except InvalidAmount as e:
            self._ui.show_message(str(e))
        except InsufficientFunds:
            self._ui.show_message(UiMessage.INSUFFICIENT_FUNDS)
        except CardNotExists:
            self._ui.show_message(UiMessage.CARD_NOT_EXISTS)
        except ATMException:
            self._ui.show_message(UiMessage.ATM_EXCEPTION)

    def _authenticate(self) -> bool:
        """
        Выполняет аутентификацию пользователя, запрашивая и проверяя номер
        карты и пин-код
        """
        user_card_number = (
            self._ui.get_input(UiMessage.INPUT_CARD_NUMBER).replace(" ", "").strip()
        )

        attempts_remaining = self._max_pin_input_attempts
        while attempts_remaining > 0:
            user_card_pin = self._ui.get_input(UiMessage.INPUT_CARD_PIN).replace(" ", "")\
                .strip()
            bank_account = BankAccount(user_card_number, self._card_repository)

            if bank_account.is_pin_code_valid(user_card_pin):
                self._ui.show_message(UiMessage.PIN_ACCEPTED)
                self._bank_account = bank_account
                return True
            else:
                attempts_remaining -= 1
                if attempts_remaining > 0:
                    self._ui.show_message(
                        UiMessage.INCORRECT_PIN.format(
                            attempts_remaining=attempts_remaining
                        )
                    )
        else:
            raise PinCodeAttemptsExceed

    def __repr__(self) -> str:
        return (
            f"""{self.__class__.__name__}(card_repository={self._card_repository!r}, ui={self._ui!r}, """
            f"""menu={self._menu!r}, max_pin_input_attempts={self._max_pin_input_attempts!r})"""
        )