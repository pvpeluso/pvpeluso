import pandas as pd
from pathlib import Path


DATA_DIR = Path(__file__).parent.parent / "data"


def load_csv(filename: str) -> pd.DataFrame:
    path = DATA_DIR / "raw" / filename
    return pd.read_csv(path)


def load_sample() -> pd.DataFrame:
    data = {
        "id": range(1, 11),
        "value": [10, 20, 15, 30, 25, 5, 40, 35, 50, 45],
        "category": ["A", "B", "A", "C", "B", "A", "C", "B", "C", "A"],
    }
    return pd.DataFrame(data)


def save_csv(df: pd.DataFrame, filename: str) -> None:
    path = DATA_DIR / "processed" / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
