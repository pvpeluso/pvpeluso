import pandas as pd
import pytest
from src.processor import remove_duplicates, filter_by_category, normalize_values


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "id": [1, 2, 2, 3],
        "value": [10, 20, 20, 30],
        "category": ["A", "B", "B", "C"],
    })


def test_remove_duplicates(sample_df):
    result = remove_duplicates(sample_df)
    assert len(result) == 3


def test_filter_by_category(sample_df):
    result = filter_by_category(sample_df, "B")
    assert len(result) == 2
    assert all(result["category"] == "B")


def test_normalize_values(sample_df):
    result = normalize_values(sample_df, "value")
    assert result["value"].min() == pytest.approx(0.0)
    assert result["value"].max() == pytest.approx(1.0)
