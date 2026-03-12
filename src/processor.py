import pandas as pd


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates()


def filter_by_category(df: pd.DataFrame, category: str) -> pd.DataFrame:
    return df[df["category"] == category].reset_index(drop=True)


def normalize_values(df: pd.DataFrame, column: str) -> pd.DataFrame:
    df = df.copy()
    col_min = df[column].min()
    col_max = df[column].max()
    df[column] = (df[column] - col_min) / (col_max - col_min)
    return df


def add_summary_stats(df: pd.DataFrame, column: str) -> pd.DataFrame:
    df = df.copy()
    df["mean"] = df[column].mean()
    df["std"] = df[column].std()
    return df
