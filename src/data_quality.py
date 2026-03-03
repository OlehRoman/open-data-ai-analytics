import pandas as pd
from pathlib import Path
import sys
import os


def check_data_quality(df):
    """
    Performs basic data quality checks: missing values, duplicates, and anomalies.
    """
    report = {
        "total_records": len(df),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicates": int(df.duplicated().sum()),
        "negative_fares": int((df['fare_amount'] < 0).sum()) if 'fare_amount' in df.columns else "N/A",
        "zero_distance": int((df['trip_distance'] == 0).sum()) if 'trip_distance' in df.columns else "N/A",
        "data_types": {k: str(v) for k, v in df.dtypes.to_dict().items()}
    }
    return report


if __name__ == "__main__":
    # Resolve project root path
    # Path(__file__) is src/data_quality.py -> .parent is src/ -> .parent.parent is root
    base_dir = Path(__file__).resolve().parent.parent
    raw_dir = base_dir / "data" / "raw"
    data_file = raw_dir / "yellow_tripdata_2015-01.csv"

    # Ensure the directory exists inside the runner's workspace
    raw_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Check if the real dataset exists
        if not data_file.exists():
            print(f"Warning: Data file not found at {data_file}")
            print("Creating dummy data for CI/CD testing...")
            # Create a small sample so the script doesn't fail
            dummy_df = pd.DataFrame({
                'fare_amount': [10.5, -1.0, 15.0, 20.0, 0.0],
                'trip_distance': [2.5, 3.0, 0.0, 10.2, 5.0],
                'passenger_count': [1, 2, 1, 4, 1]
            })
            dummy_df.to_csv(data_file, index=False)

        print(f"Reading file: {data_file}")
        df = pd.read_csv(data_file)

        results = check_data_quality(df)

        print("\n--- Data Quality Report ---")
        for key, value in results.items():
            print(f"{key}: {value}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)