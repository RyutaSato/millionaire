from uuid import UUID

from millionaire.libs.match.card import Card
from millionaire.libs.match.cards import Cards


class Player:
    """
    Notes:
        self.passedはプライベート属性に変更予定です．
        各ターンのカードの選択はこのクラスが単独で行います．
    """

    def __init__(self, uuid: UUID, name: str, __ws=None,):
        self.__ws = __ws
        self.uuid = uuid
        self.name = name
        # self.connection_status = ???
        self.cards = Cards()
        self.passed = False

    def __len__(self):
        return self.cards.__len__()

    def play_cards(self, played_cards: Cards = None) -> Cards | None:
        """ played_cardsに基づいて，出せる候補の中から１つを返します．

        カードを出せる場合に，Cardsクラスのインスタンスを返します．
        返せない場合はNoneを返します．

        Args:
            played_cards(Cards):
                最新の場のカードのリスト，ない場合は None
        Returns:
            Cards: one of candidate cards sets
            None: means that the player selected pass operation
        """
        if self.passed:
            return None
        candidate_cards_set = self.cards.lookfor_candidate_cards_set(played_cards)
        if candidate_cards_set:
            return candidate_cards_set[0]
        return None


if __name__ == '__main__':
    pass
