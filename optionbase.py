from typing_extensions import override
from Options import Range, Choice, OptionError

class ChoiceEx(Choice):
    random_value: int = -1

    @override
    @classmethod
    def from_text(cls, text: str) -> Choice:
        text = text.lower()
        if text == "random":
            return cls(cls.random_value)
        return super(ChoiceEx, cls).from_text(text)

class Weight(Range):
    range_start = 0
    range_end = 10
    weight_max = 100

    def __init__(self, value: int):
        if value < 0:
            raise OptionError(f"Option {self.__class__.__name__} cannot be negative!")
        elif value > self.weight_max:
            raise OptionError(f"Option {self.__class__.__name__} cannot be larger than {self.weight_max}!")
        self.value = value
