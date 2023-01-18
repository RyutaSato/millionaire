from logging import getLogger
from random import shuffle

from millionaire.libs.match.card import Card
from millionaire.libs.match.card_types import CardCmdKey, CardSuite, CardNumber
from millionaire.libs.match.settings import Settings

logger = getLogger(__name__)


class Cards:
    """このクラスの責任は，複数のCardクラスを保持し，CRUD管理することです．
    Args:
        cards(list[Card] | None): a list of Card class, otherwise, initialize empty list.
    """

    def __init__(self, cards: list = None):
        if cards is None:
            cards = []
        self._cards = {str(card): card for card in cards}
        self.__i = 0

    def __call__(self) -> list[Card]:
        return list(self._cards.values())

    def __len__(self):
        return len(self._cards)

    def __bool__(self):
        return bool(self._cards)

    def __setitem__(self, key: CardCmdKey, value):
        if key == CardCmdKey.ADD and isinstance(value, Card):
            self._cards[str(value)] = value
        else:
            KeyError("'key' type must be `CardCmdKey`")

    def __getitem__(self, item: str | Card | list[Card] | CardSuite | CardNumber) -> list:
        """

        Args:
            item:

        Warnings:
            返り値は，list[list[Card]]のみとします，list[Card]はバグであり，DEPRECATED です．
        """
        if isinstance(item, Card):
            return [card for card in self._cards if card > item]
        elif isinstance(item, list):
            if self.is_sequence(item):
                return self.lookfor_sequence(item)
            elif self.is_equal(item):
                return self.lookfor_equal(item)
            else:
                raise KeyError("'item' is invalid type of list. don't match `sequence` or `equal`")
        elif isinstance(item, CardNumber):
            return [card for card in self._cards if card.number == item]
        elif isinstance(item, CardSuite):
            return [card for card in self._cards if card.suite == item]
        else:
            raise KeyError("'item' type must be `Card` or `list[Card]`")

    def __delitem__(self, key: int | str | Card | CardNumber | CardSuite | list[Card]):
        if isinstance(key, CardNumber):
            self._cards = [card for card in self._cards if card.number != key]
        elif isinstance(key, CardSuite):
            self._cards = [card for card in self._cards if card.suite != key]
        elif isinstance(key, int):
            self._cards.pop(key)
        elif isinstance(key, str):
            self._cards.remove(Card.from_str(key))
        elif isinstance(key, Card):
            self._cards.remove(key)
        elif isinstance(key, list):
            for each in key:
                del self[each]
        else:
            raise TypeError(f"'card' type must be `int`, `str`, `Card`, `CardNumber` or `CardSuite`")

    def __contains__(self, item: Card | CardNumber | CardSuite | list[Card]) -> bool:
        if isinstance(item, Card):
            for card in self._cards:
                if card == item and card.suite == item.suite:
                    return True
        elif isinstance(item, CardNumber):
            for card in self._cards:
                if card.number == item:
                    return True
        elif isinstance(item, CardSuite):
            for card in self._cards:
                if card.suite == item:
                    return True
        elif isinstance(item, list):
            for each in item:
                if not isinstance(each, Card):
                    raise TypeError(f"'item' type in 'for item in ...' must be a list of 'Card' class")
                if each not in self:
                    return False
            return True
        elif hasattr(item, "cards"):
            return item.cards in self
        else:
            raise TypeError(f"'item' type in 'for item in ...' must be a instance of 'Card' class")
        return False

    @property
    def cards(self):
        """
        Notes:
            DEPRECATED
        Returns:
            a list of card
        """
        logger.warning("Cards.cards method is deprecated.")
        return self._cards

    def add(self, cards: Card | list[Card] | None):

        if isinstance(cards, Card):
            self._cards[str(cards)] = cards
        elif isinstance(cards, list) and cards:
            for c in cards:
                self.add(c)
        else:
            return

    def pop(self, __index: int = -1):
        return self._cards.pop(__index)

    def clear(self):
        li = self._cards.values()
        self._cards.clear()
        return li

    @staticmethod
    def is_one(cards):
        """

        Args:
            cards:

        Returns:

        """
        if isinstance(cards, Card) or (isinstance(cards, list) and len(cards) == 1 and isinstance(cards[0], Card)):
            return True
        return False

    def lookfor_one(self, card: Card = None) -> list[list[Card]]:
        """

        Args:
            card:

        Returns:

        """
        self._cards.sort()
        if card is None:
            return [[c] for c in self._cards]
        if card.suite in self:
            return [[c] for c in self[card.suite] if c > card]
        else:
            return [[c] for c in self._cards if c > card]

    @staticmethod
    def is_sequence(played_cards: list[Card]) -> bool:
        """

        Args:
            played_cards:

        Returns:

        """
        played_cards.sort()
        for i in range(1, len(played_cards)):
            if played_cards[i - 1].suite != played_cards[i].suite or played_cards[i - 1] + 1 != played_cards[i]:
                return False
        return len(played_cards) >= 3

    def lookfor_sequence(self, played_cards: list[Card] = None) -> list[list[Card]]:
        """

        Args:
            played_cards:

        Returns:

        """
        li = []
        if played_cards is not None and played_cards:
            num = len(played_cards)
            logger.debug(f"min(played_cards): {min(played_cards)} self[min(played_cards)]: {self[min(played_cards)]}")
            min_card = min(self[min(played_cards)]) if self[min(played_cards)] else Card(suite=CardSuite.JOKER,
                                                                                         number=CardNumber.NONE,
                                                                                         _strength=-1)
        else:
            num = 0
            min_card = Card(suite=CardSuite.JOKER, number=CardNumber.NONE, _strength=-1)  # 3の強さが0
        for suite in CardSuite:
            cnt = 1
            # TODO: jokerがある場合の挙動をかく．
            same_suite_cards = sorted(self[suite])
            for i in range(1, len(same_suite_cards) + 1):
                if same_suite_cards[i - 1] > min_card and i != len(same_suite_cards) and same_suite_cards[i - 1] + 1 == \
                        same_suite_cards[i]:
                    cnt += 1
                else:
                    if cnt < 3:
                        cnt = 1
                        continue
                    if cnt >= 3 and (num == 0 or num == cnt):
                        li.append([card for card in same_suite_cards[i - 3:i]])
                    if cnt >= 4 and (num == 0 or num == cnt):
                        li.append([card for card in same_suite_cards[i - 4:i - 1]])
                        li.append([card for card in same_suite_cards[i - 4:i]])
                    if cnt >= 5 and (num == 0 or num == cnt):
                        li.append([card for card in same_suite_cards[i - 5:i - 2]])
                        li.append([card for card in same_suite_cards[i - 5:i - 1]])
                        li.append([card for card in same_suite_cards[i - 5:i]])
                    if cnt >= 6 and (num == 0 or num == cnt):
                        li.append([card for card in same_suite_cards[i - 6:i - 3]])
                        li.append([card for card in same_suite_cards[i - 6:i - 2]])
                        li.append([card for card in same_suite_cards[i - 6:i - 1]])
                        li.append([card for card in same_suite_cards[i - 6:i]])
                    cnt = 1
        return li

    @staticmethod
    def is_equal(cards: list[Card]) -> bool:
        """

        Args:
            cards:

        Returns:

        """
        for i in range(len(cards) - 1):
            if cards[i] != cards[i + 1]:
                return False
        return True

    def lookfor_equal(self, played_cards: list[Card] = None) -> list[list[Card]]:
        """

        Args:
            played_cards:

        Returns:

        """
        li = []
        idx = 0
        self._cards.sort()
        while idx < len(self) - 1:
            # 2枚同じランクのカードがある場合
            if self._cards[idx] == self._cards[idx + 1]:
                li.append([self._cards[idx], self._cards[idx + 1]])
                # 3枚同じランクのカードがある場合
                if idx < len(self) - 2 and self._cards[idx + 1] == self._cards[idx + 2]:
                    li.append([self._cards[idx + 1], self._cards[idx + 2]])
                    li.append([self._cards[idx], self._cards[idx + 2]])
                    li.append([self._cards[idx], self._cards[idx + 1], self._cards[idx + 2]])
                    # 4枚同じランクのカードがある場合
                    if idx < len(self) - 3 and self._cards[idx + 2] == self._cards[idx + 3]:
                        li.append([self._cards[idx], self._cards[idx + 3]])
                        li.append([self._cards[idx + 1], self._cards[idx + 3]])
                        li.append([self._cards[idx + 2], self._cards[idx + 3]])
                        li.append([self._cards[idx], self._cards[idx + 1], self._cards[idx + 3]])
                        li.append([self._cards[idx + 1], self._cards[idx + 2], self._cards[idx + 3]])
                        li.append([self._cards[idx], self._cards[idx + 2], self._cards[idx + 3]])
                        li.append([self._cards[idx], self._cards[idx + 1], self._cards[idx + 2], self._cards[idx + 3]])
                        idx += 4
                    else:
                        idx += 3
                else:
                    idx += 2
            else:
                idx += 1
        if played_cards is not None:
            li = [c for c in li if len(c) == len(played_cards) and c[0] > played_cards[0]]
        return li

    @classmethod
    def create_cards(cls, is_shuffle: bool = True, joker_num: int = 2):
        """

        Args:
            is_shuffle:
            joker_num:

        Returns:

        """
        cards: list[Card] = []
        cards.extend([Card(suite=CardSuite("jo"), number=CardNumber(0)) for _ in range(joker_num)])
        for suite in CardSuite:
            if suite == CardSuite.JOKER:
                continue
            cards.extend([Card(CardSuite(suite), number=CardNumber(num)) for num in range(1, 14)])
        if is_shuffle:
            shuffle(cards)
        return cls(cards)

    def lookfor_candidate_cards_set(self, played_cards: list[Card] = None) -> list[list[Card]]:
        """

        Args:
            played_cards:

        Returns:

        """
        if played_cards is None or not played_cards:
            candidate_cards_set = self.lookfor_sequence(played_cards)
            tmp = self.lookfor_equal(played_cards)
            if tmp:
                candidate_cards_set.extend(tmp)
            tmp = self.lookfor_one()
            if tmp:
                candidate_cards_set.extend(tmp)
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
