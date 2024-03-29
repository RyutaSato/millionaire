from enum import StrEnum, Enum


class CardNumber(Enum):
    """define types of number of each card

    """
    NONE = 0
    ACE = 1
    DEUCE = 2
    TREY = 3
    CATER = 4
    CINQUE = 5
    SICE = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


class CardSuite(StrEnum):
    """define each suite type of card
    Examples:
        >>> clover = CardSuite.CLOVER
        >>> clover
        'cl'
    """
    JOKER = "jo"
    SPADE = "sp"
    CLOVER = "cl"
    DIAMOND = "di"
    HEART = "he"


if __name__ == '__main__':
    suite = CardSuite.CLOVER
    print(suite)
    # >> joker
