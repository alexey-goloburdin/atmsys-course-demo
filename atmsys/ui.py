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
        print(f"\n{'='*25}\n")