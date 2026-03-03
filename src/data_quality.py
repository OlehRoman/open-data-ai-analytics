import pandas as pd
from pathlib import Path
import sys


def check_data_quality(df):

    report = {
        "total_records": len(df),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicates": df.duplicated().sum(),
        "negative_fares": (df['fare_amount'] < 0).sum() if 'fare_amount' in df.columns else "N/A",
        "zero_distance": (df['trip_distance'] == 0).sum() if 'trip_distance' in df.columns else "N/A",
        "data_types": df.dtypes.to_dict()
    }
    return report


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    data_file = base_dir / "data" / "raw" / "yellow_tripdata_2015-01.csv"

    dummy_file = base_dir / "data" / "raw" / "sample_data.csv"

    try:
        target_path = data_file if data_file.exists() else dummy_file

        print(f"Reading file: {target_path}")
        df = pd.read_csv(target_path)

        results = check_data_quality(df)

        print("\n--- Data Quality Report ---")
        for key, value in results.items():
            print(f"{key}: {value}")

    except FileNotFoundError:
        print(f"Error: File not found at {data_file}")
        print("Make sure the data_load module ran successfully and the file is in data/raw/")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)