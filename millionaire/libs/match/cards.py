from __future__ import annotations

from enum import Enum
from logging import getLogger
from random import shuffle
from copy import copy

from millionaire.libs.match.card import Card
from millionaire.libs.match.card_types import CardSuite, CardNumber

logger = getLogger(__name__)


class CardsRegularity(Enum):
    none = 0
    one = 1
    sequence = 2
    equal = 3
    empty = 4


class Cards:
    """このクラスの責任は，複数のCardクラスを保持し，CRUD管理することです．

    このクラスは，Cardクラスをvalueに持つ疑似Dictionaryとして動作します．
    要素は，なるべく高速に要素の抽出を行うために，ソート後のindexとstrをキーとしたdictionaryの両方を保持しています．
    したがって，探索がO(1)で動作します．が，挿入はindex指定の場合O(1), strをキーとする場合O(n)です．
    Args:
        cards(list[Card] | None): a list of Card class, otherwise, initialize empty list.
    """

    def __init__(self, cards: list[Card] = None, _regularity: CardsRegularity = CardsRegularity.none):
        if cards is None:
            cards = []
        self.__cards = {str(card): card for card in cards}
        self.__idx = [str(card) for card in sorted(cards)]
        self._regularity = _regularity

    def __iter__(self):
        self.__iter = self.__cards.values().__iter__()
        return self.__iter

    def __next__(self):
        return next(self.__iter)

    def __setitem__(self, key: str | int, card: Card):
        if not isinstance(card, Card):
            raise ValueError('the value must be `Card`')
        if isinstance(key, str):
            self.__cards[key] = card
            self.__idx.insert(self.__binary_search(card, 0, len(self.__idx)), str(card))
        elif isinstance(key, int):
            self.__idx.insert(key, str(card))
            self.__cards[str(card)] = card
        else:
            raise KeyError("the key must be `str` or `int`")

    def __getitem__(self, key: int | str | CardSuite | CardNumber | slice) -> Card | Cards:
        if isinstance(key, int):
            return self.__cards[self.__idx[key]]
        elif isinstance(key, CardSuite):
            return Cards([card for card in self if card.suite == key])
        elif isinstance(key, str):
            return self.__cards[key]
        elif isinstance(key, CardNumber):
            return Cards([card for card in self if card.number == key])
        elif isinstance(key, slice):
            start = key.start
            stop = key.stop if key.stop is not None else len(self)
            step = key.step if key.step is not None else 1
            return Cards([self[i] for i in range(start, stop, step)])
        else:
            raise KeyError("the key must be `str`, `int`, `CardSuite`, `CardNumber` or `slice`")

    def __delitem__(self, key: int | str | Card):
        if isinstance(key, int):
            del self.__cards[self.__idx.pop(key)]
        elif isinstance(key, str):
            del self.__cards[key]
            self.__idx.remove(key)
        elif isinstance(key, Card):
            del self.__cards[str(key)]
            self.__idx.remove(str(key))
        else:
            raise KeyError("the key must be `str`, `int` or `Card`")

    def __binary_search(self, card: Card, st: int, ed: int) -> int:
        if ed <= st:
            return st
        if card < self.__cards[self.__idx[(st + ed) // 2]]:
            return self.__binary_search(card, st, (st + ed) // 2)
        else:
            return self.__binary_search(card, (st + ed) // 2 + 1, ed)

    def __str__(self):
        return str([self[key] for key in self.__idx])

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other: Card | Cards):
        if isinstance(other, Card):
            if self._regularity == CardsRegularity.one:
                return self[0] == other
            else:
                raise ValueError(f"don't match type between {self._regularity}{type(other)}")
        elif isinstance(other, Cards):
            if self._regularity == other._regularity != CardsRegularity.none:
                if not len(self) == len(other):
                    return False
                match self._regularity:
                    case CardsRegularity.equal:
                        return self[0] == other[0]
                    case CardsRegularity.sequence:
                        return min(self) == min(other)
            else:
                raise ValueError(f"don't match type between {type(other)}")
        raise ValueError(f"{type(other)} is invalid. must be `Card` or `Cards` class")

    def __lt__(self, other):
        if isinstance(other, Card):
            if self._regularity == CardsRegularity.one:
                return self[0] < other
            else:
                raise ValueError(f"don't match type between {self._regularity}{type(other)}")
        elif isinstance(other, Cards):
            if self._regularity == other._regularity != CardsRegularity.none:
                if not len(self) == len(other):
                    return False
                match self._regularity:
                    case CardsRegularity.equal:
                        return self[0] < other[0]
                    case CardsRegularity.sequence:
                        return min(self) < min(other)
            else:
                raise ValueError(f"don't match type between {type(other)}")
        raise ValueError(f"{type(other)} is invalid. must be `Card` or `Cards` class")

    def __ne__(self, other):
        return not self.__eq__(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __len__(self):
        return len(self.__cards)

    def __bool__(self):
        return bool(self.__cards)

    def __contains__(self, item: Card | CardNumber | CardSuite | Cards) -> bool:
        if isinstance(item, str):
            return item in self.__cards
        elif isinstance(item, Card):
            return str(item) in self.__cards
        elif isinstance(item, CardNumber):
            for card in self:
                if card.number == item:
                    return True
        elif isinstance(item, CardSuite):
            for card in self:
                if card.suite == item:
                    return True
        elif isinstance(item, Cards):
            for each in item:
                if each not in self:
                    return False
            return True
        else:
            raise TypeError(f"'item' type in 'for item in ...' must be a instance of 'Card' class")

    def __add__(self, other: Card | Cards):
        cp_cards = copy(self)
        if isinstance(other, Card):
            cp_cards[str(other)] = other
            return cp_cards
        elif isinstance(other, Cards):
            for card in other:
                cp_cards.__cards[str(card)] = card
        else:
            raise ValueError(f"type {type(other)} is invalid")
        return cp_cards

    def __iadd__(self, other: Card | Cards):
        if isinstance(other, Card):
            self[str(other)] = other
        elif isinstance(other, Cards):
            for card in other:
                self[str(card)] = card
        else:
            raise ValueError(f"type {type(other)} is invalid")
        return self

    def __sub__(self, other):
        cp_cards = copy(self)
        if isinstance(other, Card):
            del self[other]
        elif isinstance(other, Cards):
            for card in other:
                del cp_cards[card]
        else:
            raise ValueError(f"type {type(other)} is invalid")
        return cp_cards

    def __isub__(self, other):
        if isinstance(other, Card):
            del self[other]
        elif isinstance(other, Cards):
            for card in other:
                del self[card]
        else:
            raise ValueError(f"type {type(other)} is invalid")
        return self

    def lookfor_one(self, played_card: Card = None) -> list[Cards]:
        return_list = []
        for card in self:
            if played_card is None or card > played_card:
                return_list.append(Cards([card], CardsRegularity.one))
        return return_list

    @staticmethod
    def is_sequence(cards: Cards) -> bool:
        """Cardsがsequenceかどうか判定します．

        既に_regularity属性にsequenceがある場合は即座にTrueを返します．
        noneの場合は，sequenceかどうか判定し結果を返します．
        それ以外の場合はFalseを返します．

        Args:
            cards (Cards): 判定するCardsクラスを指定．

        Returns:
            bool

        Notes:
            staticmethodのため，インスタンスでも引数に`self`が必要です．
        """
        if cards._regularity == CardsRegularity.none:
            if len(cards) < 3:
                return False
            for i in range(1, len(cards)):
                if not cards[i - 1] + 1 == cards[i]:
                    return False
            return True
        return cards._regularity == CardsRegularity.sequence

    @staticmethod
    def is_equal(cards: Cards) -> bool:
        """`Cards`が`equal`かどうか判定します．

        既に`_regularity`属性に`equal`がある場合は即座に`True`を返します．
        `none`の場合は，`equal`かどうか判定し結果を返します．
        それ以外の場合は`False`を返します．

        Args:
            cards (Cards): 判定するCardsクラスを指定．

        Returns:
            bool

        Notes:
            staticmethodのため，インスタンスでも引数に`self`が必要です．
        """
        if cards._regularity == CardsRegularity.none:
            if len(cards) < 2:
                return False
            f_card = cards[0]
            for card in cards:
                if not f_card == card:
                    return False
            return True
        return cards._regularity == CardsRegularity.equal

    @staticmethod
    def is_one(cards: Cards) -> bool:
        """`Cards`が`one`かどうか判定します．

        既に`_regularity`属性に`one`がある場合は即座に`True`を返します．
        `none`の場合は，len(1)の場合に`True`を返します．
        それ以外の場合は`False`を返します．

        Args:
            cards (Cards): 判定するCardsクラスを指定．

        Returns:
            bool

        Notes:
            staticmethodのため，インスタンスでも引数に`self`が必要です．
        """
        if cards._regularity == CardsRegularity.none:
            if len(cards) == 1:
                return True
            else:
                return False
        return cards._regularity == CardsRegularity.one

    def lookfor_sequence(self, played_cards: Cards = None) -> list[Cards]:
        """
        TODO: Need test
        Args:
            played_cards:

        Returns:

        """
        li = []
        if isinstance(played_cards, Cards):
            if not Cards.is_sequence(played_cards):
                ValueError(f"played_cards._regularity is {played_cards._regularity}. must be `sequence`")
            num = len(played_cards)
            min_card = played_cards[0]
        else:
            num = 0
            min_card = Card(suite=CardSuite.JOKER, number=CardNumber.NONE, _strength=-1)  # 3の強さが0
        for suite in CardSuite:
            cnt = 1
            # TODO: jokerがある場合の挙動をかく．
            same_suite_cards = self[suite]
            for i in range(1, len(same_suite_cards) + 1):
                if same_suite_cards[i - 1] > min_card and i != len(same_suite_cards) and same_suite_cards[i - 1] + 1 == \
                        same_suite_cards[i]:
                    cnt += 1
                else:
                    if cnt < 3:
                        cnt = 1
                        continue
                    if cnt >= 3 and (num == 0 or num == cnt):
                        li.append(Cards([card for card in same_suite_cards[i - 3:i]], CardsRegularity.sequence))
                    if cnt >= 4 and (num == 0 or num == cnt):
                        li.append(Cards([card for card in same_suite_cards[i - 4:i - 1]], CardsRegularity.sequence))
                        li.append(Cards([card for card in same_suite_cards[i - 4:i]], CardsRegularity.sequence))
                    if cnt >= 5 and (num == 0 or num == cnt):
                        li.append(Cards([card for card in same_suite_cards[i - 5:i - 2]], CardsRegularity.sequence))
                        li.append(Cards([card for card in same_suite_cards[i - 5:i - 1]], CardsRegularity.sequence))
                        li.append(Cards([card for card in same_suite_cards[i - 5:i]], CardsRegularity.sequence))
                    if cnt >= 6 and (num == 0 or num == cnt):
                        li.append(Cards([card for card in same_suite_cards[i - 6:i - 3]], CardsRegularity.sequence))
                        li.append(Cards([card for card in same_suite_cards[i - 6:i - 2]], CardsRegularity.sequence))
                        li.append(Cards([card for card in same_suite_cards[i - 6:i - 1]], CardsRegularity.sequence))
                        li.append(Cards([card for card in same_suite_cards[i - 6:i]], CardsRegularity.sequence))
                    cnt = 1
        return li

    def lookfor_equal(self, played_cards: Cards = None) -> list[Cards]:
        # TODO: Upgrade
        """

        Args:
            played_cards:

        Returns:

        """
        li = []
        idx = 0
        while idx < len(self) - 1:
            # 2枚同じランクのカードがある場合
            if self[idx] == self[idx + 1]:
                li.append(Cards([self[idx], self[idx + 1]], CardsRegularity.equal))
                # 3枚同じランクのカードがある場合
                if idx < len(self) - 2 and self[idx + 1] == self[idx + 2]:
                    li.append(Cards([self[idx + 1], self[idx + 2]], CardsRegularity.equal))
                    li.append(Cards([self[idx], self[idx + 2]], CardsRegularity.equal))
                    li.append(Cards([self[idx], self[idx + 1], self[idx + 2]], CardsRegularity.equal))
                    # 4枚同じランクのカードがある場合
                    if idx < len(self) - 3 and self[idx + 2] == self[idx + 3]:
                        li.append(Cards([self[idx], self[idx + 3]], CardsRegularity.equal))
                        li.append(Cards([self[idx + 1], self[idx + 3]], CardsRegularity.equal))
                        li.append(Cards([self[idx + 2], self[idx + 3]], CardsRegularity.equal))
                        li.append(Cards([self[idx], self[idx + 1], self[idx + 3]], CardsRegularity.equal))
                        li.append(Cards([self[idx + 1], self[idx + 2], self[idx + 3]], CardsRegularity.equal))
                        li.append(Cards([self[idx], self[idx + 2], self[idx + 3]], CardsRegularity.equal))
                        li.append(
                            Cards([self[idx], self[idx + 1], self[idx + 2], self[idx + 3]], CardsRegularity.equal))
                        idx += 4
                    else:
                        idx += 3
                else:
                    idx += 2
            else:
                idx += 1
        if played_cards is not None:
            li = [cards for cards in li if len(cards) == len(played_cards) and cards > played_cards]
        return li

    @classmethod
    def create_cards(cls, is_shuffle: bool = True, player_num: int = 4, joker_num: int = 2) -> tuple:
        """

        Args:
            player_num:
            is_shuffle:
            joker_num:

        Returns:

        """
        cards: list[Card] = []
        cards.extend([Card.from_str('jo0') for _ in range(joker_num)])
        for suite in CardSuite:
            if suite == CardSuite.JOKER:
                continue
            cards.extend([Card.from_str(f"{suite}{num}") for num in range(1, 14)])
        if is_shuffle:
            shuffle(cards)
        if player_num < 1:
            return tuple(cards)
        return tuple(Cards(cards[len(cards) * i // player_num: len(cards) * (i + 1) // player_num]) for i in
                     range(player_num))

    def lookfor_candidate_cards_set(self, played_cards: Cards = None) -> list[Cards]:
        """

        Args:
            played_cards:

        Returns:

        """
        if played_cards is None:
            candidate_cards_set = self.lookfor_sequence(played_cards)
            candidate_cards_set.extend(self.lookfor_equal(played_cards))
            candidate_cards_set.extend(self.lookfor_one())
            logger.info(f"played: {played_cards} candidate_set:{candidate_cards_set}")
        elif self.is_one(played_cards):
            candidate_cards_set = self.lookfor_one(played_cards[0])
        elif self.is_sequence(played_cards):
            candidate_cards_set = self.lookfor_sequence(played_cards)
        elif self.is_equal(played_cards):
            candidate_cards_set = self.lookfor_equal(played_cards)
        else:
            raise ValueError(f"cards don't match any pattern. played_cards: {played_cards}")
        return candidate_cards_set


if __name__ == "__main__":
    li = Cards([Card.from_str('sp2'), Card.from_str('sp1'), Card.from_str('he11')])
    print(li)
    str_li = ["he5", "sp8", "di3", "cl1", "di4", "di5"]
    for s in str_li:
        li[s] = Card.from_str(s)
        print(li)
    print(li[1:3])
    print([str(item) for item in li.lookfor_sequence()])
    print([str(item) for item in li.lookfor_equal()])
    print(li.lookfor_candidate_cards_set())
    assert Cards([Card.from_str("he5"), Card.from_str("di5")], CardsRegularity.equal) < Cards([Card.from_str("cl2"),
                                                                                               Card.from_str("sp2")],
                                                                                              CardsRegularity.equal)
    print(Cards.create_cards())
