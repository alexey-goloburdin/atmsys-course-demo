from collections.abc import Sequence

from atmsys.menu import UI


class FakeUI(UI):
    def __init__(self, *, inputs: Sequence[str]):
        self.messages: list[str] = []
        self.separator = "SEPARATOR"
        self._input_index = -1
        self.inputs = inputs

    def show_message(self, message: str) -> None:
        self.messages.append(message)

    def get_input(self, prompt: str) -> str:
        self._input_index += 1
        return self.inputs[self._input_index]

    def show_separator(self) -> None:
        self.messages.append(self.separator)
