import enum


class LetterStatus(enum.Enum):
    ABSENT = 0
    PRESENT = 1
    CORRECT = 2
    UNCHECKED = 3
