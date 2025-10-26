from atmsys.atm import ATM
from atmsys.file_card_repository import FileCardRepository
from atmsys.menu import CheckBalanceMenuItem, DepositMenuItem, ExitMenuItem, Menu, WithdrawMenuItem
from atmsys.ui import GreenConsoleUI


def main():
    ui = GreenConsoleUI()
    atm = ATM(
        card_repository=FileCardRepository("cards.json"),
        ui=ui,
        menu=Menu(items=[CheckBalanceMenuItem(), WithdrawMenuItem(), DepositMenuItem(), ExitMenuItem()], ui=ui),
    )
    atm.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
