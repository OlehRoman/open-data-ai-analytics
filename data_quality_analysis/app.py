import os
import pandas as pd
from sqlalchemy import create_engine
import json
import time


def run_quality_check():
    db_url = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/project_db")
    engine = create_engine(db_url)

    # 👉 Універсальний шлях
    reports_dir = os.getenv("REPORTS_DIR", "reports")
    os.makedirs(reports_dir, exist_ok=True)

    report_path = os.path.join(reports_dir, "quality_report.json")

    print("--- Модуль data_quality_analysis стартував ---")

    df = None
    for i in range(10):
        try:
            df = pd.read_sql("SELECT * FROM raw_data", engine)
            print("Дані успішно зчитано з БД.")
            break
        except Exception:
            print(f"Спроба {i + 1}: Таблиця 'raw_data' ще не створена. Чекаємо...")
            time.sleep(5)

    if df is None:
        print("Помилка: Не вдалося отримати дані.")
        return

    report = {
        "total_rows": len(df),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicates_count": int(df.duplicated().sum()),
        "column_types": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    print(f"Звіт про якість збережено у {report_path}")


if __name__ == "__main__":
    run_quality_check()