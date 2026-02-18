import pandas as pd


def check_data_quality(df):

    report = {
        "total_records": len(df),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicates": df.duplicated().sum(),
        "negative_fares": (df['fare_amount'] < 0).sum(),
        "zero_distance": (df['trip_distance'] == 0).sum(),
        "data_types": df.dtypes.to_dict()
    }

    return report


if __name__ == "__main__":
    try:
        df = pd.read_csv("../data/raw/yellow_tripdata_2015-01.csv")
        results = check_data_quality(df)

        print("--- Звіт про якість даних ---")
        for key, value in results.items():
            print(f"{key}: {value}")
    except FileNotFoundError:
        print("Помилка: Файл не знайдено. Перевірте папку data/raw/")