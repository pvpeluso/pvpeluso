import pandas as pd
from src.analyzer import summary, group_stats


def test_summary():
    df = pd.DataFrame({"value": [1, 2, 3], "category": ["A", "B", "A"]})
    result = summary(df)
    assert result["rows"] == 3
    assert "value" in result["columns"]


def test_group_stats():
    df = pd.DataFrame({
        "value": [10, 20, 30],
        "category": ["A", "A", "B"],
    })
    result = group_stats(df, "category", "value")
    assert len(result) == 2
    a_row = result[result["category"] == "A"].iloc[0]
    assert a_row["mean"] == 15.0
    assert a_row["sum"] == 30.0
    assert a_row["count"] == 2
