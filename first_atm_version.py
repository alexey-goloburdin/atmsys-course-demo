# Максимальное количество попыток ввода пин-кода
MAX_PIN_INPUT_ATTEMPTS = 3

# Карта, с которой работает банкомат — номер и PIN
CARD_NUMBER = "3333 4444 5555 6666".replace(" ", "")
CARD_PIN = "1234"
card_balance = 1000

print("Добро пожаловать в банкомат!")

user_card_number = input("Введите номер карты: ").replace(" ", "").strip()

# Попытки ввода PIN
attempts_remaining = MAX_PIN_INPUT_ATTEMPTS
while attempts_remaining > 0:
    user_card_pin = input("Введите PIN: ").replace(" ", "").strip()
    if user_card_number == CARD_NUMBER and user_card_pin == CARD_PIN:
        print("PIN принят. Добро пожаловать!")
        break
    else:
        attempts_remaining -= 1
        if attempts_remaining > 0:
            print("Неверный PIN. Осталось попыток:", attempts_remaining)
else:
    print("Карта заблокирована. Обратитесь в банк.")
    raise SystemExit

while True:
    print(f"\n{'='*25}\nВыберите операцию:")
    print("1 – Проверить баланс")
    print("2 – Снять деньги")
    print("3 – Пополнить счёт")
    print("4 – Выход")

    choice = input("Введите номер операции: ")

    # Проверка, что введено число 1-4
    if not choice.isdigit():
        print("Ошибка ввода. Введите число от 1 до 4.")
        continue

    choice = int(choice)
    print(f"{'='*25}\n")

    if choice == 1:
        # Проверка баланса
        print("Ваш баланс:", card_balance, "руб.")

    elif choice == 2:
        # Снятие денег
        amount = input("Сколько вы хотите снять? Введите сумму: ")

        if not amount.isdigit():
            print("Ошибка ввода! Нужно ввести число.")
            continue

        amount = int(amount)

        if amount <= 0:
            print("Сумма должна быть больше нуля.")
            continue

        if amount > card_balance:
            print("Недостаточно средств!")
        else:
            card_balance -= amount
            print("Снятие успешно. Ваш новый баланс:", card_balance, "руб.")

    elif choice == 3:
        # Пополнение счёта
        print("Сколько вы хотите внести?")
        amount = input("Введите сумму: ")

        if not amount.isdigit():
            print("Ошибка ввода! Нужно ввести число.")
            continue

        amount = int(amount)

        if amount <= 0:
            print("Сумма должна быть больше нуля.")
            continue

        card_balance += amount
        print("Пополнение успешно. Ваш новый баланс:", card_balance, "руб.")

    elif choice == 4:
        print("Спасибо, что пользуетесь нашим банкоматом!")
        break

    else:
        print("Такой операции нет. Введите число от 1 до 4.")