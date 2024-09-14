import json
from typing import Any, Dict


class Node:
    def __init__(self, id: int, attachment: str = None):
        """
        Инициализация узла.

        :param id: Уникальный идентификатор узла (неотрицательное целое число).
        :param attachment: Дополнительная информация узла (строка или None).
        """
        self.id = id
        self._edges: Dict[str, int] = {}
        self.attachment = attachment

    @property
    def id(self) -> int:
        """Возвращает уникальный идентификатор узла."""
        return self._id

    @id.setter
    def id(self, value: int):
        """
        Устанавливает уникальный идентификатор узла.

        :param value: Уникальный идентификатор (неотрицательное целое число).
        :raises ValueError: Если идентификатор не является неотрицательным целым числом.
        """
        if not isinstance(value, int) or value < 0:
            raise ValueError(f"Field 'id' should be a non-negative integer, but got {type(value).__name__}")
        self._id = value

    @property
    def edges(self) -> Dict[str, int]:
        """Возвращает уникальный идентификатор узла."""
        return self._edges

    @property
    def attachment(self) -> str:
        """Возвращает дополнительную информацию узла."""
        return self._attachment

    @attachment.setter
    def attachment(self, value: str) -> None:
        """
        Устанавливает дополнительную информацию узла.

        :param value: Дополнительная информация (строка или None).
        :raises ValueError: Если значение не строка и не None.
        """
        if value is not None and not isinstance(value, str):
            raise ValueError(f"Field 'attachment' should be a string or None, but got {type(value).__name__}")
        self._attachment = value

    def add_edge(self, to_id: int, key: str) -> None:
        """
        Добавляет ребро к узлу.

        :param to_id: Идентификатор узла, к которому ведет ребро (неотрицательное целое число).
        :param key: Ключ для ребра (строка).
        :raises KeyError: Если ключ уже существует.
        :raises ValueError: Если to_id не является неотрицательным целым числом или если key не строка.
        """
        if key in self._edges:
            raise KeyError(f"The key '{key}' already exists!")
        if not isinstance(to_id, int) or to_id < 0:
            raise ValueError(f"The 'to_id' should be a non-negative integer, but got {type(to_id).__name__}")
        if not isinstance(key, str):
            raise ValueError(f"The 'key' should be a string, but got {type(key).__name__}")
        self._edges[key] = to_id

    def remove_edge(self, key: str) -> None:
        """
        Удаляет ребро из узла по ключу.

        :param key: Ключ ребра для удаления (строка).
        :raises KeyError: Если ключ не существует.
        """
        if key not in self._edges:
            raise KeyError(f"The key '{key}' does not exist!")
        del self._edges[key]

    def to_json(self) -> Dict[str, Any]:
        """
        Преобразует узел в JSON-совместимый словарь.

        :return: Словарь, представляющий узел, включая идентификатор, дополнительную информацию и ребра.
        """
        return {
            'id': self.id,
            'attachment': self.attachment,
            'edges': self._edges.copy()
        }