import pytest
from api.algorithms import CustomAlgorithms

# Custom decorator
both_algorithms = pytest.mark.parametrize(
    "sort_func",
    [CustomAlgorithms.merge_sort, CustomAlgorithms.quick_sort],
)

@pytest.fixture
def sample_data():
    return [
        {"key": 3, "value": "A"},
        {"key": 1, "value": "B"},
        {"key": None, "value": "C"},
        {"key": 2, "value": "D"},
        {"key": None, "value": "E"},
    ]


class TestCustomAlgorithms:
    """Tests for CustomAlgorithms sorting methods."""

    @both_algorithms
    def test_sort_ascending_with_none_last(self, sort_func, sample_data):
        result = sort_func(sample_data, key="key", reverse=False)
        keys = [item["key"] for item in result]
        assert keys == [1, 2, 3, None, None]

    @both_algorithms
    def test_sort_descending_with_none_first(self, sort_func, sample_data):
        result = sort_func(sample_data, key="key", reverse=True)
        keys = [item["key"] for item in result]
        assert keys == [None, None, 3, 2, 1]

    @both_algorithms
    def test_empty_list_returns_empty(self, sort_func):
        assert sort_func([], key="key") == []

    @both_algorithms
    def test_only_one_item_returns_same(self, sort_func):
        data = [{"key": 42}]
        assert sort_func(data, key="key") == data

    @both_algorithms
    def test_descending_order_is_reverse_of_ascending(self, sort_func, sample_data):
        asc = sort_func(sample_data, key="key", reverse=False)
        desc = sort_func(sample_data, key="key", reverse=True)
        asc_keys = [x["key"] for x in asc if x["key"] is not None]
        desc_keys = [x["key"] for x in desc if x["key"] is not None]
        assert desc_keys == list(reversed(asc_keys))

    def test_merge_and_quikc_have_same_result(self, sample_data):
        merge_sorted = CustomAlgorithms.merge_sort(sample_data, key="key")
        quick_sorted = CustomAlgorithms.quick_sort(sample_data, key="key")
        assert [d["key"] for d in merge_sorted] == [d["key"] for d in quick_sorted]
