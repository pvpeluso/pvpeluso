from src.data_loader import load_sample, save_csv
from src.processor import remove_duplicates, normalize_values, add_summary_stats
from src.analyzer import summary, group_stats, plot_distribution


def main():
    print("Loading data...")
    df = load_sample()
    print(f"Loaded {len(df)} rows\n")

    print("Processing data...")
    df = remove_duplicates(df)
    df = normalize_values(df, "value")
    df = add_summary_stats(df, "value")

    print("Analysis summary:")
    stats = summary(df)
    print(f"  Rows: {stats['rows']}")
    print(f"  Columns: {stats['columns']}\n")

    print("Group statistics by category:")
    group = group_stats(df, "category", "value")
    print(group.to_string(index=False))
    print()

    print("Saving processed data...")
    save_csv(df, "processed_data.csv")

    print("Saving distribution plot...")
    plot_distribution(df, "value", save=True)

    print("Done.")


if __name__ == "__main__":
    main()
