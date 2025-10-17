from .abstract_algo_base import Algorithms


class CustomAlgorithms(Algorithms):
    """The implementation of the abstract Algorithms base class.

    This class provides custom sorting algorithms — currently Merge Sort and Quick Sort —
    with safe handling for `None` values and support for ascending or descending order.
    
    Methods
    _______
    merge_sort(data: list[dict], key: str, reverse: bool) -> list[dict]
        Performs a mergesort on a list of dictionaries with None-safe comparisons.
    quick_sort(data: list, key: str, reverse: bool = False) -> list
        Perform an quciksort on a list of dictionaries.

    """

    @staticmethod
    def merge_sort(data: list, key: str, reverse: bool = False) -> list:
        """Perform a mergesort on a list of dictionaries.
        
        :param data: The list of dictionaries to sort.
        :type data: list[dict]
        :param key: The dictionary key to sort by.
        :type key: str
        :param reverse: Sort descending if True; ascending otherwise.
        :type reverse: bool
        :return: A new list of dictionaries sorted by the given key.
        :rtype: list[dict]
        """
        if len(data) <= 1:
            return data

        mid = len(data) // 2
        left = CustomAlgorithms.merge_sort(data[:mid], key, reverse)
        right = CustomAlgorithms.merge_sort(data[mid:], key, reverse)

        result, i, j = [], 0, 0

        while i < len(left) and j < len(right):
            a = left[i].get(key)
            b = right[j].get(key)

            # Handle all None combinations safely
            if a is None and b is None:
                result.append(left[i])  # arbitrary consistent behavior
                i += 1
                continue
            if a is None:
                # None values go last in ascending, first in descending
                if reverse:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
                continue
            if b is None:
                if reverse:
                    result.append(right[j])
                    j += 1
                else:
                    result.append(left[i])
                    i += 1
                continue

            # Normal comparison
            if (a <= b and not reverse) or (a > b and reverse):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result


    @staticmethod
    def quick_sort(data: list, key: str, reverse: bool = False) -> list:
        """Perform quicksort on a list of dictionaries.
        
        :param data: The list of dictionaries to sort.
        :type data: list[dict]
        :param key: The dictionary key to sort by.
        :type key: str
        :param reverse: Sort descending if True; ascending otherwise.
        :type reverse: bool
        :return: A new list of dictionaries sorted by the given key.
        :rtype: list[dict]
        """
        if len(data) <= 1:
            return data

        pivot = data[len(data) // 2]
        pivot_value = pivot.get(key)

        # Helper: safe comparison that handles None values
        def compare(a, b):
            if a is None and b is None:
                return 0
            if a is None:
                return 1 if not reverse else -1  # None goes last in asc, first in desc
            if b is None:
                return -1 if not reverse else 1
            if a == b:
                return 0
            return -1 if (a < b and not reverse) or (a > b and reverse) else 1

        left = [item for item in data if compare(item.get(key), pivot_value) < 0]
        middle = [item for item in data if compare(item.get(key), pivot_value) == 0]
        right = [item for item in data if compare(item.get(key), pivot_value) > 0]

        return (
            CustomAlgorithms.quick_sort(left, key, reverse)
            + middle
            + CustomAlgorithms.quick_sort(right, key, reverse)
        )
