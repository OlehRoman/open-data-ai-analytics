import os
import pandas as pd
from sqlalchemy import create_engine
import json
import time


def run_research():
    db_url = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/project_db")
    engine = create_engine(db_url)

    # 👉 універсальний шлях
    reports_dir = os.getenv("REPORTS_DIR", "reports")
    os.makedirs(reports_dir, exist_ok=True)

    report_path = os.path.join(reports_dir, "research_report.json")

    print("--- Модуль data_research стартував ---")

    df = None
    for i in range(10):
        try:
            df = pd.read_sql("SELECT * FROM raw_data", engine)
            if not df.empty:
                print("Дані для дослідження отримано.")
                break
        except Exception:
            print(f"Спроба {i + 1}: Очікування таблиці 'raw_data'...")
            time.sleep(5)

    if df is None or df.empty:
        print("Помилка: Дані не знайдені.")
        return

    numeric_df = df.select_dtypes(include=['number'])

    if numeric_df.empty:
        stats = {"message": "У наборі даних немає числових колонок для аналізу."}
    else:
        stats = numeric_df.describe().to_dict()

    research_results = {
        "analysis_type": "Descriptive Statistics",
        "numeric_columns_analyzed": list(numeric_df.columns),
        "statistics": stats,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(research_results, f, indent=4, ensure_ascii=False)

    print(f"Статистичний звіт збережено у {report_path}")


if __name__ == "__main__":
    run_research()