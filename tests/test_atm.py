from enum import Enum
from typing import Callable

import pytest
from fakes.in_memory_card_repository import InMemoryCardRepository
from fakes.ui import FakeUI

from atmsys.atm import ATM, UI
from atmsys.menu import (
    CheckBalanceMenuItem,
    DepositMenuItem,
    ExitMenuItem,
    Menu,
    WithdrawMenuItem,
)


class MenuCommand(str, Enum):
    GET_BALANCE = "1"
    WITHDRAW = "2"
    DEPOSIT = "3"
    EXIT = "4"


@pytest.fixture
def card_repo() -> InMemoryCardRepository:
    return InMemoryCardRepository({"1333444455556666": {"pin": "5678", "balance": 100}})


@pytest.fixture
def make_atm(card_repo: InMemoryCardRepository) -> Callable[[UI], ATM]:
    def _make_atm(ui: UI) -> ATM:
        return ATM(
            card_repository=card_repo,
            ui=ui,
            menu=Menu(
                items=[
                    CheckBalanceMenuItem(),
                    WithdrawMenuItem(),
                    DepositMenuItem(),
                    ExitMenuItem(),
                ],
                ui=ui,
            ),
            max_pin_input_attempts=2,
        )

    return _make_atm


def test_atm_authenticates_on_firts_attempt(
    make_atm: Callable[[UI], ATM],
):
    ui = FakeUI(inputs=("1333444455556666", "5678", MenuCommand.EXIT))
    sut = make_atm(ui)

    with pytest.raises(SystemExit):
        sut.run()

    assert "PIN принят. Добро пожаловать!" in ui.messages


def test_atm_authenticates_on_second_attempt(
    make_atm: Callable[[UI], ATM],
):
    ui = FakeUI(inputs=("1333444455556666", "0000", "5678", MenuCommand.EXIT))
    sut = make_atm(ui)

    with pytest.raises(SystemExit):
        sut.run()

    assert "PIN принят. Добро пожаловать!" in ui.messages


def test_atm_does_not_authenticate_after_attempts_ended(
    make_atm: Callable[[UI], ATM],
):
    ui = FakeUI(inputs=("1333444455556666", "0000", "1234"))
    sut = make_atm(ui)

    with pytest.raises(SystemExit):
        sut.run()

    assert "PIN принят. Добро пожаловать!" not in ui.messages
    assert "Карта заблокирована. Обратитесь в банк." in ui.messages


def test_atm_displays_correct_balance(
    make_atm: Callable[[UI], ATM],
):
    ui = FakeUI(
        inputs=("1333444455556666", "5678", MenuCommand.GET_BALANCE, MenuCommand.EXIT)
    )
    sut = make_atm(ui)

    with pytest.raises(SystemExit):
        sut.run()

    assert "Ваш баланс: 100 руб." in ui.messages


def test_atm_successful_withdraw(
    make_atm: Callable[[UI], ATM],
):
    # Начальный баланс 1000 руб, списываем 11 руб
    ui = FakeUI(
        inputs=(
            "1333444455556666",
            "5678",
            MenuCommand.WITHDRAW,
            "11",
            MenuCommand.EXIT,
        )
    )
    sut = make_atm(ui)

    with pytest.raises(SystemExit):
        sut.run()

    # Проверяем, что баланс теперь 89 руб
    ui = FakeUI(
        inputs=("1333444455556666", "5678", MenuCommand.GET_BALANCE, MenuCommand.EXIT)
    )
    sut = make_atm(ui)
    with pytest.raises(SystemExit):
        sut.run()
    assert "Ваш баланс: 89 руб." in ui.messages


def test_atm_does_not_withdraw_above_the_limit(
    make_atm: Callable[[UI], ATM],
):
    ui = FakeUI(
        inputs=(
            "1333444455556666",
            "5678",
            MenuCommand.WITHDRAW,
            "101",
            MenuCommand.EXIT,
        )
    )
    sut = make_atm(ui)

    with pytest.raises(SystemExit):
        sut.run()

    assert "Недостаточно средств для снятия со счёта" in ui.messages


def test_atm_does_not_withdraw_incorrect_amount(
    make_atm: Callable[[UI], ATM],
):
    # Начальный баланс 1000 руб, списываем некорректную сумму
    ui = FakeUI(
        inputs=(
            "1333444455556666",
            "5678",
            MenuCommand.WITHDRAW,
            "11.",  # некорректная сумма
            MenuCommand.EXIT,
        )
    )
    sut = make_atm(ui)

    with pytest.raises(SystemExit):
        sut.run()

    # Проверяем, что баланс остался прежним
    ui = FakeUI(
        inputs=("1333444455556666", "5678", MenuCommand.GET_BALANCE, MenuCommand.EXIT)
    )
    sut = make_atm(ui)
    with pytest.raises(SystemExit):
        sut.run()
    assert "Ваш баланс: 100 руб." in ui.messages


def test_atm_successful_deposit(
    make_atm: Callable[[UI], ATM],
):
    # Начальный баланс 1000 руб, пополняем на 115 руб
    ui = FakeUI(
        inputs=("1333444455556666", "5678", MenuCommand.DEPOSIT, "15", MenuCommand.EXIT)
    )
    sut = make_atm(ui)

    with pytest.raises(SystemExit):
        sut.run()

    # Проверяем, что система теперь выдаёт 115 руб
    ui = FakeUI(inputs=("1333444455556666", "5678", "1", "4"))
    sut = make_atm(ui)

    with pytest.raises(SystemExit):
        sut.run()

    ui = FakeUI(
        inputs=("1333444455556666", "5678", MenuCommand.GET_BALANCE, MenuCommand.EXIT)
    )
    sut = make_atm(ui)
    with pytest.raises(SystemExit):
        sut.run()
    assert "Ваш баланс: 115 руб." in ui.messages


def test_atm_does_not_deposit_incorrect_amount(
    make_atm: Callable[[UI], ATM],
):
    # Начальный баланс 1000 руб, пополняем на некорректную сумму
    ui = FakeUI(
        inputs=(
            "1333444455556666",
            "5678",
            MenuCommand.DEPOSIT,
            "15.",  # Некорректная сумма
            MenuCommand.EXIT,
        )
    )
    sut = make_atm(ui)

    with pytest.raises(SystemExit):
        sut.run()

    # Проверяем, что баланс остался прежним
    ui = FakeUI(inputs=("1333444455556666", "5678", "1", "4"))
    sut = make_atm(ui)

    with pytest.raises(SystemExit):
        sut.run()

    ui = FakeUI(
        inputs=("1333444455556666", "5678", MenuCommand.GET_BALANCE, MenuCommand.EXIT)
    )
    sut = make_atm(ui)
    with pytest.raises(SystemExit):
        sut.run()
    assert "Ваш баланс: 100 руб." in ui.messages