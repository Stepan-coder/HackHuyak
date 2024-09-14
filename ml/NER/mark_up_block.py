import json
from NER.mark_up_type import *
from typing import List, Dict, Any


class MarkUpBlock:
    """
    Represents a block of text with associated markup type, start and end indices,
    and optional attachments.

    Attributes:
        text (str): The text content of the markup block.
        block_type (MarkUpType): The type of markup associated with this block.
        start (int): The starting index of the text block.
        end (int): The ending index of the text block.
        attachments (Dict[str, Any]): Additional data that can be associated with the markup block.
    """

    def __init__(self,
                 text: str,
                 block_type: MarkUpType,
                 start: int = 0,
                 end: int = 0,
                 attachments: Dict[str, Any] = {}):
        """
        Initializes a MarkUpBlock instance.

        Args:
            text (str): The text content of the markup block.
            block_type (MarkUpType): The type of markup.
            start (int, optional): The starting index. Defaults to 0.
            end (int, optional): The ending index. Defaults to 0.
            attachments (Dict[str, Any], optional): Additional data. Defaults to an empty dictionary.
        """
        self._text = text
        self._block_type = block_type
        self._start = start
        self._end = end
        self._attachments = attachments

    @property
    def text(self) -> str:
        """str: The text content of the markup block."""
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        """
        Sets the text content of the markup block.

        Args:
            text (str): The new text content.

        Raises:
            TypeError: If the provided text is not a string.
            ValueError: If the length of the text is less than or equal to zero.
        """
        if not isinstance(text, str):
            raise TypeError(f"Expected 'str', but got '{type(text).__name__}'")
        if len(text) <= 0:
            raise ValueError(f"The length of text should be greater than zero")
        self._text = text

    @property
    def block_type(self) -> MarkUpType:
        """MarkUpType: The type of markup associated with this block."""
        return self._block_type

    @block_type.setter
    def block_type(self, block_type: MarkUpType) -> None:
        """
        Sets the type of markup for this block.

        Args:
            block_type (MarkUpType): The new type of markup.

        Raises:
            TypeError: If the provided block_type is not an instance of MarkUpType.
        """
        if not isinstance(block_type, MarkUpType):
            raise TypeError(f"Expected 'MarkUpType', but got '{type(block_type).__name__}'")
        self._block_type = block_type

    @property
    def start(self) -> int:
        """int: The starting index of the text block."""
        return self._start

    @start.setter
    def start(self, start: int):
        """
        Sets the starting index of the text block.

        Args:
            start (int): The new starting index.

        Raises:
            TypeError: If the provided start index is not an integer.
            ValueError: If the start index is less than or equal to zero.
        """
        if not isinstance(start, int):
            raise TypeError(f"Expected 'int', but got '{type(start).__name__}'")
        if start < 0:  # Changed to allow starting index at 0
            raise ValueError(f"Start index should be greater than or equal to zero")
        self._start = start

    @property
    def end(self) -> int:
        """int: The ending index of the text block."""
        return self._end

    @end.setter
    def end(self, end: int):
        """
        Sets the ending index of the text block.

        Args:
            end (int): The new ending index.

        Raises:
            TypeError: If the provided end index is not an integer.
            ValueError: If the end index is less than or equal to zero.
        """
        if not isinstance(end, int):
            raise TypeError(f"Expected 'int', but got '{type(end).__name__}'")
        if end < 0:  # Changed to allow ending index at 0
            raise ValueError(f"End index should be greater than or equal to zero")
        self._end = end

    @property
    def attachments(self) -> Dict[str, Any]:
        """Dict[str, Any]: A dictionary containing additional data related to the markup block."""
        return self._attachments

    @attachments.setter
    def attachments(self, attachments: Dict[str, Any]) -> None:
        """
        Sets the attachments for the markup block.

        Args:
            attachments (Dict[str, Any]): The new attachments data.
        """
        self._attachments = attachments

    def to_json(self) -> json:
        """
        Converts the MarkUpBlock instance to a JSON serializable dictionary.

        Returns:
            dict: A dictionary representation of the markup block.
        """
        return {
            "text": self._text,
            "block_type": self._block_type.value,
            "start": self._start,
            "end": self._end,
            "attachments": self._attachments
        }
