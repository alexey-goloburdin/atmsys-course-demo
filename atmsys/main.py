from atmsys.atm import ATM
from atmsys.card_repository import InMemoryCardRepository
from atmsys.ui import ConsoleUI
from atmsys.menu import (
    CheckBalanceMenuItem,
    DepositMenuItem,
    ExitMenuItem,
    WithdrawMenuItem,
    Menu
)


def main():
    ui = ConsoleUI()
    atm = ATM(
        card_repository=InMemoryCardRepository(),
        ui=ui,
        menu=Menu(items=[
            CheckBalanceMenuItem(),
            WithdrawMenuItem(),
            DepositMenuItem(),
            ExitMenuItem()
        ], ui=ui))
    atm.run()


if __name__ == "__main__":
    main()