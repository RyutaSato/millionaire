from dataclasses import dataclass
import re

from millionaire.libs.match.card_types import CardSuite, CardNumber

#  TODO: settings.pyに移動予定
SUITE_LIST = ["jo", "sp", "cl", "di", "he"]
MAX_STRENGTH = 100
REGEX_CARD = r"^(jo|sp|cl|di|he)(0|1|2|3|4|5|6|7|8|9|10|11|12|13)$"
pattern = re.compile(REGEX_CARD)


def set_strength(number: int) -> int:
    """
    Warnings:
        このメソッドは，プロトタイプが完成するまでの間有効とします．
        その後は，カードごとの拡張性を高めるため，Cards classで自動的に決定されます．
    Args:
        number:

    Returns:

    """
    if 0 < number < 14:
        return (number + 10) % 13
    return MAX_STRENGTH


@dataclass(frozen=True)
class Card:
    """このクラスの責任は，Card固有の変数の値を定義することです．

    Args:
        suite: CardSuite
        number: CardNumber
        _strength: int
    Examples:
        >>>card = Card(CardSuite('sp'), CardNumber.KING)
        >>>print(card)
        'sp13'
    """

    suite: CardSuite
    number: CardNumber
    _strength: int

    def __str__(self):
        return f"{self.suite.value}{self.number.value}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Card):
            raise ValueError(f"{type(other)} is invalid")
        return self._strength == other._strength

    def __lt__(self, other):
        if not isinstance(other, Card):
            raise ValueError(f"{type(other)} is invalid")
        return self._strength < other._strength

    def __ne__(self, other):
        return not self.__eq__(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __add__(self, other):
        if not isinstance(other, int):
            ValueError("'__add__' method must be integer")
        return Card(suite=self.suite, number=self.number, _strength=self._strength + other)

    def __hash__(self):
        return hash(self.__str__())

    @classmethod
    def from_str(cls, string: str):
        """Validate `string` and returns a card class.
        Args:
            string (str): The string must be one of "jo", "sp", "cl", "di" and "he", and a number from 0 to 13.
        Returns:
            Card: return a Card instance. if `num` is `0`, Card._strength is allocated to MAX_STRENGTH.
        Raises:
            ValueError: If `string` doesn't match any patterns.
        """
        if pattern.match(string) is None:
            print(string)
            raise ValueError("string doesn't match any patterns")
        su, num = pattern.match(string).groups()
        return cls(suite=CardSuite(su),
                   number=CardNumber(int(num)),
                   _strength=set_strength(int(num))
                   )


if __name__ == "__main__":
    print(pattern.match("sp1").groups())
    card = Card.from_str("sp1")
    print(card)
