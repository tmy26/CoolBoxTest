from abc import ABC, abstractmethod


class Algorithms(ABC):
    """Abstract base class for sorting algorithm implementations."""

    @staticmethod
    @abstractmethod
    def merge_sort(data: list[dict], key: str, reverse: bool = False) -> list[dict]:
        """Perform a mergesort on a list of dictionaries."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def quick_sort(data: list[dict], key: str, reverse: bool = False) -> list[dict]:
        """Perform a quicksort on a list of dictionaries."""
        raise NotImplementedError
