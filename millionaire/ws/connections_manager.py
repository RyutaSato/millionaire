from logging import getLogger

logger = getLogger(__name__)


class ConnectionsManager:
    """
    Warnings:
        型アノテーションをしようすると，循環参照エラーが発生します．
        コーディングルールとして，型ヒントはSHOULDのため，この問題については以後検討です．
        https://qiita.com/simonritchie/items/753beac8598b15c01c3d
        https://zenn.dev/ganariya/articles/python-lazy-annotation
    """
    def __init__(self):
        self.__online: dict = dict()

    def add(self, client):
        logger.info(f"connections: added: {client.name}")
        self.__online[client.name] = client
        logger.info(f"connections: total: {len(self.__online)}")

    def remove(self, name):
        logger.info(f"connections: remove: {name}")
        del self.__online[name]
        logger.info(f"connections: total: {len(self.__online)}")


connections = ConnectionsManager()
