from enum import StrEnum


class RuUiMessage(StrEnum):
    GREETINGS = "Добро пожаловать в банкомат!"
    CARD_BLOCKED = "Карта заблокирована. Обратитесь в банк."
    INCORRECT_MENU_ITEM = "Ошибка ввода. Введите число от {min_choice} до {max_choice}."
    INSUFFICIENT_FUNDS = "Недостаточно средств для снятия со счёта"
    CARD_NOT_EXISTS = "Извините, карта не найдена"
    ATM_EXCEPTION = "Извините, что-то пошло не так"
    PIN_ACCEPTED = "PIN принят. Добро пожаловать!"
    INCORRECT_PIN = "Неверный PIN. Осталось попыток: {attempts_remaining}"
    BALANCE = "Ваш баланс: {balance} руб."
    GOODBYE = "Спасибо, что пользуетесь нашим банкоматом!"

    AMOUNT_MUST_BE_POSITIVE = "Сумма должна быть больше нуля."
    AMOUNT_MUST_BE_DIGIT = "Ошибка ввода! Нужно ввести число."

    INPUT_CARD_NUMBER = "Введите номер карты: "
    INPUT_CARD_PIN = "Введите PIN: "
    HOW_MUCH_WITHDRAW_INPUT = "Сколько вы хотите снять?\nВведите сумму: "
    HOW_MUCH_DEPOSIT_INPUT = "Сколько вы хотите внести?\nВведите сумму: "

    MENU_NUMBER_INPUT = "Введите номер операции: "
    MENU_CHOOSE_ITEM = "Выберите операцию"
    MENU_GET_BALANCE_ITEM = "Проверить баланс"
    MENU_WITHDRAW_ITEM = "Снять деньги"
    MENU_DEPOSIT_ITEM = "Пополнить счёт"
    MENU_EXIT_ITEM = "Выход"


class EnUiMessage(StrEnum):
    GREETINGS = "Welcome to the ATM!"
    CARD_BLOCKED = "Your card has been blocked. Please contact your bank."
    INCORRECT_MENU_ITEM = (
        "Input error. Enter a number between {min_choice} and {max_choice}."
    )
    INSUFFICIENT_FUNDS = "Insufficient funds to withdraw from account"
    CARD_NOT_EXISTS = "Sorry, card not found"
    ATM_EXCEPTION = "Sorry, something went wrong"
    PIN_ACCEPTED = "PIN accepted. Welcome!"
    INCORRECT_PIN = "Incorrect PIN. Attempts remaining: {attempts_remaining}"
    BALANCE = "Your balance: {balance} rubles."
    GOODBYE = "Thank you for using our ATM!"

    AMOUNT_MUST_BE_POSITIVE = "The amount must be greater than zero."
    AMOUNT_MUST_BE_DIGIT = "Input error! You must enter a number."

    INPUT_CARD_NUMBER = "Enter the card number: "
    INPUT_CARD_PIN = "Enter the PIN: "
    HOW_MUCH_WITHDRAW_INPUT = "How much do you want to withdraw?\nEnter the amount: "
    HOW_MUCH_DEPOSIT_INPUT = "How much would you like to deposit?\nEnter the amount: "
    
    MENU_NUMBER_INPUT = "Enter the operation number: "
    MENU_CHOOSE_ITEM = "Select an operation"
    MENU_GET_BALANCE_ITEM = "Check your balance"
    MENU_WITHDRAW_ITEM = "Withdraw money"
    MENU_DEPOSIT_ITEM = "Top up your account"
    MENU_EXIT_ITEM = "Exit"


UiMessage = EnUiMessage