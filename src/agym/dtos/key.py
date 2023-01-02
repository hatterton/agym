from dataclasses import dataclass
from enum import Enum, auto


class KeyCode(Enum):
    # letters
    LETTER = auto()
    A = auto()
    B = auto()
    C = auto()
    D = auto()
    E = auto()
    F = auto()
    G = auto()
    H = auto()
    I = auto()
    J = auto()
    K = auto()
    L = auto()
    M = auto()
    N = auto()
    O = auto()
    P = auto()
    Q = auto()
    R = auto()
    S = auto()
    T = auto()
    U = auto()
    V = auto()
    W = auto()
    X = auto()
    Y = auto()
    Z = auto()

    # digits
    DIGIT = auto()
    D0 = auto()
    D1 = auto()
    D2 = auto()
    D3 = auto()
    D4 = auto()
    D5 = auto()
    D6 = auto()
    D7 = auto()
    D8 = auto()
    D9 = auto()

    # punctuations
    PUNCTUATION = auto()
    COMMA = auto()
    PERIOD = auto()
    MINUS = auto()
    PLUS = auto()
    COLON = auto()
    SEMICOLON = auto()
    LEFTPAREN = auto()
    RIGHTPAREN = auto()
    SLASH = auto()
    QUESTION = auto()
    EXCLAIM = auto()
    QUOTE = auto()
    DOUBLE_QUOTE = auto()

    # arrows
    LEFT_ARROW = auto()
    RIGHT_ARROW = auto()
    UP_ARROW = auto()
    DOWN_ARROW = auto()

    # controls
    SHIFT = auto()
    CONTROL = auto()

    # other
    SPACE = auto()
    BACKSPACE = auto()
    ESCAPE = auto()


@dataclass
class Key:
    code: KeyCode
    unicode: str
