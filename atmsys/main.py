from typing import TypedDict

from .exceptions import (
    IncorrectMenuOption,
    InsufficientFunds,
    InvalidAmount,
    PinCodeAttemptsExceed,
)


# Максимальное количество попыток ввода пин-кода
MAX_PIN_INPUT_ATTEMPTS = 3

MENU = {
    1: {
        "description": "Проверить баланс"
    },
    2: {
        "description": "Снять деньги"
    },
    3: {
        "description": "Пополнить счёт"
    },
    4: {
        "description": "Выход"
    }
}

type Rubles = int
type PIN = str

class Card(TypedDict):
    pin: PIN
    balance: Rubles

type CardNumber = str
type Cards = dict[CardNumber, Card]

cards: Cards = {
    "3333444455556666": {
        "pin": "1234",
        "balance": 1_000
    },
    "1234567890123456": {
        "pin": "7777",
        "balance": 28_500
    }
}


def authenticate_user(cards: Cards, max_attempts: int) -> CardNumber:
    """
    Запрашивает у пользователя корректные номер карты и пин-код,
    пока они не будут введены. Максимальное количество попыток max_attempts.
    """
    user_card_number = input("Введите номер карты: ").replace(" ", "").strip()

    # Попытки ввода PIN
    attempts_remaining = max_attempts
    while attempts_remaining > 0:
        user_card_pin = input("Введите PIN: ").replace(" ", "").strip()
        if user_card_number in cards and cards[user_card_number]["pin"] == user_card_pin:
            print("PIN принят. Добро пожаловать!")
            return user_card_number
        else:
            attempts_remaining -= 1
            if attempts_remaining > 0:
                print("Неверный PIN. Осталось попыток:", attempts_remaining)
    else:
        raise PinCodeAttemptsExceed


def print_menu_items() -> None:
    """Выводит меню банкомата"""
    menu = [
        f"\n{get_separator()}\nВыберите операцию:"
    ]
    for menu_item_number, menu_item in MENU.items():
        menu.append(f"{menu_item_number} - {menu_item['description']}")
    print("\n".join(menu))


def get_menu_min_max_numbers() -> tuple[int, int]:
    """Возвращает min и max номера пунктов меню"""
    min_choice = min(MENU.keys())
    max_choice = max(MENU.keys())
    return min_choice, max_choice


def is_user_menu_item_choice_valid(user_menu_item_choice: str) -> bool:
    """
    Возвращает True, если пользователем выбран корректный пункт меню, иначе False
    """
    if not user_menu_item_choice.isdigit():
        return False
    min_choice_number, max_choice_number = get_menu_min_max_numbers()
    return min_choice_number <= int(user_menu_item_choice) <= max_choice_number


def get_user_menu_choice() -> int:
    """Запрашивает у пользователя пункт меню и возвращает его номер"""
    user_menu_item_choice = input("Введите номер операции: ")
    if not is_user_menu_item_choice_valid(user_menu_item_choice):
        raise IncorrectMenuOption
    return int(user_menu_item_choice)


def get_separator():
    return f"{'='*25}\n"


def print_balance(balance: Rubles) -> None:
    """Печатает баланс пользователя"""
    print("Ваш баланс:", balance, "руб.")


def withdraw(cards: Cards, card_number: CardNumber) -> int:
    """Снятие денег со счёта, возвращает новый баланс"""
    print("Сколько вы хотите снять?")
    amount = input("Введите сумму: ")
    balance = cards[card_number]["balance"]

    if not amount.isdigit():
        raise InvalidAmount("Ошибка ввода! Нужно ввести число.")

    amount = int(amount)

    if amount <= 0:
        raise InvalidAmount("Сумма должна быть больше нуля.")

    if amount > balance:
        raise InsufficientFunds
    else:
        balance -= amount

    cards[card_number]["balance"] = balance
    return balance


def deposit(cards: Cards, card_number: CardNumber) -> int:
    """Пополняет баланс, возвращает новый баланс"""
    print("Сколько вы хотите внести?")
    amount = input("Введите сумму: ")
    balance = cards[card_number]["balance"]

    if not amount.isdigit():
        raise InvalidAmount("Ошибка ввода! Нужно ввести число")

    amount = int(amount)

    if amount <= 0:
        raise InvalidAmount("Сумма должна быть больше нуля.")

    balance += amount
    cards[card_number]["balance"] = balance
    return balance


def bye():
    """Печатает сообщение пользователю при выходе из завершении работы банкомата"""
    print("Спасибо, что пользуетесь нашим банкоматом!")


def notify_about_incorrect_operation():
    """Выводит пользователю сообщение о некорректном вводе номера меню"""
    min_choice_number, max_choice_number = get_menu_min_max_numbers()
    print(f"Такой операции нет. Введите число от {min_choice_number} до {max_choice_number}.")


def main(cards: Cards):
    """Запускает приложение банкомата"""
    print("Добро пожаловать в банкомат!")

    try:
        user_card_number = authenticate_user(cards, MAX_PIN_INPUT_ATTEMPTS)
    except PinCodeAttemptsExceed:
        print("Карта заблокирована. Обратитесь в банк.")
        raise SystemExit

    while True:
        print_menu_items()

        try:
            user_menu_item_choice = get_user_menu_choice()
        except IncorrectMenuOption:
            min_choice_number, max_choice_number = get_menu_min_max_numbers()
            print(f"Ошибка ввода. Введите число от {min_choice_number} до {max_choice_number}.")
            continue

        print(get_separator())

        if user_menu_item_choice  == 1:
            # Проверка баланса
            print_balance(cards[user_card_number]["balance"])

        elif user_menu_item_choice  == 2:
            # Снятие денег
            try:
                new_balance = withdraw(cards, user_card_number)
                print_balance(new_balance)
            except InvalidAmount as e:
                print(e)
                continue
            except InsufficientFunds:
                print("Недостаточно средств на счёте")

        elif user_menu_item_choice == 3:
            # Пополнение счёта
            try:
                new_balance = deposit(cards, user_card_number)
                print_balance(new_balance)
            except InvalidAmount as e:
                print(e)

        elif user_menu_item_choice  == 4:
            bye()
            break

        else:
            notify_about_incorrect_operation()


if __name__ == "__main__":
    main(cards)
