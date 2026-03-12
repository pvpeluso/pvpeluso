import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


OUTPUT_DIR = Path(__file__).parent.parent / "data" / "processed"


def summary(df: pd.DataFrame) -> dict:
    return {
        "rows": len(df),
        "columns": list(df.columns),
        "numeric_stats": df.describe().to_dict(),
    }


def group_stats(df: pd.DataFrame, group_col: str, value_col: str) -> pd.DataFrame:
    return df.groupby(group_col)[value_col].agg(["mean", "sum", "count"]).reset_index()


def plot_distribution(df: pd.DataFrame, column: str, save: bool = False) -> None:
    fig, ax = plt.subplots()
    df[column].hist(ax=ax, bins=10)
    ax.set_title(f"Distribution of {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Frequency")

    if save:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        fig.savefig(OUTPUT_DIR / f"{column}_distribution.png")
    else:
        plt.show()

    plt.close(fig)
