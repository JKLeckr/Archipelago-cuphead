from typing_extensions import override
import Options

class ChoiceEx(Options.Choice):
    random_value: int = -1

    @override
    @classmethod
    def from_text(cls, text: str) -> Options.Choice:
        text = text.lower()
        if text == "random":
            return cls(cls.random_value)
        return super(ChoiceEx, cls).from_text(text)

class Weight(Options.Range):
    range_start = 0
    range_end = 10
    weight_max = 100

    def __init__(self, value: int):
        if value < 0:
            raise Options.OptionError(f"Option {self.__class__.__name__} cannot be negative!")
        elif value > self.weight_max:
            raise Options.OptionError(f"Option {self.__class__.__name__} cannot be larger than {self.weight_max}!")
        self.value = value
