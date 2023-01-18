from uuid import UUID

from millionaire.libs.match.card import Card
from millionaire.libs.match.cards import Cards


class Player:
    """
    Notes:
        self.passedはプライベート属性に変更予定です．
        各ターンのカードの選択はこのクラスが単独で行います．
    """
    def __init__(self, uuid: UUID, name: str):
        self.uuid = uuid
        self.name = name
        # self.connection_status = ???
        self.cards = Cards()
        self.passed = False

    def __len__(self):
        return self.cards.__len__()


    def play_cards(self, played_cards: list[Card] | None):
        """
        Args:
            played_cards:
                最新の場のカードのリスト，ない場合は None
        Returns:
            list: one of candidate cards sets
            empty list: DEPRECATED
            TODO: None: FUTURE REPLACE WITH []
        """
        if self.passed:
            return []
        candidate_cards_set = self.cards.lookfor_candidate_cards_set(played_cards)
        if candidate_cards_set:
            return candidate_cards_set[0]
        return []


if __name__ == '__main__':
    pass
