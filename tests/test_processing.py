from typing import Any, Dict, List
import pytest
from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_operations() -> List[Dict[str, Any]]:
    """Фикстура, возвращающая тестовый список банковских операций."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
        {"id": 2, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 3, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 4, "state": "PENDING", "date": "2024-03-11T02:26:18.671407"},
    ]


def test_filter_by_state_default(sample_operations: List[Dict[str, Any]]) -> None:
    """Тест фильтрации со статусом по умолчанию (EXECUTED)."""
    result = filter_by_state(sample_operations)
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


@pytest.mark.parametrize(
    "state, expected_count",
    [
        ("CANCELED", 1),
        ("PENDING", 1),
        ("NON_EXISTENT", 0),
    ],
)
def test_filter_by_state_parametrized(
    sample_operations: List[Dict[str, Any]], state: str, expected_count: int
) -> None:
    """Тест фильтрации для различных состояний."""
    result = filter_by_state(sample_operations, state=state)
    assert len(result) == expected_count


def test_sort_by_date_descending(sample_operations: List[Dict[str, Any]]) -> None:
    """Тест сортировки по дате по убыванию."""
    result = sort_by_date(sample_operations)
    assert result[0]["id"] == 1
    assert result[1]["id"] == 4
