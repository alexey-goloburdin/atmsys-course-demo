from .menu import UI


class ConsoleUI(UI):
    """Пользовательский интерфейс банкомата"""

    def show_message(self, message: str) -> None:
        """Показывает сообщение message пользователю"""
        print(message)

    def get_input(self, prompt: str) -> str:
        """Запрашивает данные у пользователя и возвращает их"""
        return input(prompt)

    def show_separator(self) -> None:
        """Показывает визуальный разделитель"""
        print(f"\n{'=' * 25}\n")


class GreenConsoleUI(UI):
    """Пользовательский интерфейс банкомата"""

    def show_message(self, message: str) -> None:
        """Показывает сообщение message пользователю"""
        print(f"\033[32m{message}\033[0m")

    def get_input(self, prompt: str) -> str:
        """Запрашивает данные у пользователя и возвращает их"""
        return input(f"\033[32m{prompt}\033[0m")

    def show_separator(self) -> None:
        """Показывает визуальный разделитель"""
        print(f"\033[32m\n{'=' * 25}\n\033[0m")


class RedConsoleUI(UI):
    """Консольный пользовательский интерфейс банкомата"""

    def show_message(self, message: str) -> None:
        """Показывает сообщение message пользователю"""
        print(f"\033[31m{message}\033[0m")

    def get_input(self, prompt: str) -> str:
        """Запрашивает данные у пользователя и возвращает их"""
        return input(f"\033[31m{prompt}\033[0m")

    def show_separator(self) -> None:
        """Показывает визуальный разделитель"""
        print(f"\n\033[31m{'=' * 25}\033[0m\n")
