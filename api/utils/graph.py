from api.utils.node import Node
from typing import Dict, List


class Graph:
    def __init__(self):
        """
        Инициализация графа.

        Хранит узлы графа в словаре с их идентификаторами.
        """
        self._nodes: Dict[int, Node] = {}

    def __iter__(self):
        """Позволяет итерировать по идентификаторам узлов в графе."""
        yield from self._nodes

    @property
    def ids(self) -> List[int]:
        """Возвращает список идентификаторов узлов в графе."""
        return list(self._nodes.keys())

    @property
    def count(self) -> int:
        """Возвращает количество узлов в графе."""
        return len(self._nodes)

    def add_node(self, node: Node) -> None:
        """
        Добавляет новый узел в граф.

        :param node: Узел для добавления.
        :raises Exception: Если узел с таким идентификатором уже существует.
        """
        if node.id in self._nodes:
            raise Exception('This id already exists')
        self._nodes[node.id] = node

    def get_node(self, id: int) -> Node:
        """
        Получает узел по идентификатору.

        :param id: Идентификатор узла.
        :raises Exception: Если узел с таким идентификатором не существует.
        :return: Узел с указанным идентификатором.
        """
        if id in self._nodes:
            return self._nodes[id]
        raise Exception('id does not exist')

    def delete_node(self, id: int) -> None:
        """
        Удаляет узел из графа и связанные с ним ребра.

        :param id: Идентификатор узла для удаления.
        :raises KeyError: Если узел с таким идентификатором не существует.
        """
        if id not in self._nodes:
            raise KeyError('Node with this id does not exist')
        del self._nodes[id]

    def add_edge(self, from_id: int, to_id: int, key: str) -> None:
        """
        Добавляет ребро между двумя узлами.

        :param from_id: Идентификатор узла, от которого ведет ребро.
        :param to_id: Идентификатор узла, к которому ведет ребро.
        :param key: Уникальный ключ для ребра.
        :raises KeyError: Если хотя бы один из узлов не существует.
        """
        if from_id not in self._nodes or to_id not in self._nodes:
            raise KeyError('Both nodes must exist to create an edge.')
        self._nodes[from_id].add_edge(to_id=to_id, key=key)

    def delete_edge(self, from_id: int, key: str) -> None:
        """
        Удаляет ребро из узла по ключу.

        :param from_id: Идентификатор узла, из которого удаляется ребро.
        :param key: Ключ ребра для удаления.
        :raises KeyError: Если узел с заданным идентификатором не существует.
        """
        if from_id not in self._nodes:
            raise KeyError('Node with this id does not exist.')
        self._nodes[from_id].remove_edge(key=key)

    def predict(self, id: int) -> Dict[str, int]:
        """
        Возвращает все ребра узла с указанным идентификатором.

        :param id: Идентификатор узла.
        :raises KeyError: Если узел с таким идентификатором не существует.
        :return: Словарь всех ребер узла.
        """
        if id not in self._nodes:
            raise KeyError('Node with this id does not exist.')
        return self._nodes[id].edges