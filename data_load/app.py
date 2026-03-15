import os
import pandas as pd
from sqlalchemy import create_engine
import time


def load_data():
    # 1. Отримуємо URL бази даних зі змінних оточення Docker
    # Формат: postgresql://user:password@db:5432/project_db
    db_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/project_db")
    csv_path = "/app/dataset/dataset.csv"

    print(f"--- Модуль data_load стартував ---")

    # Перевірка наявності файлу
    if not os.path.exists(csv_path):
        print(f"Помилка: Файл {csv_path} не знайдено!")
        return

    # Спроба підключення до БД (з невеликою затримкою, щоб БД встигла запуститися)
    engine = create_engine(db_url)

    for i in range(5):
        try:
            df = pd.read_csv(csv_path)
            # 2. Створення таблиці та завантаження (if_exists='replace' оновить дані)
            df.to_sql("raw_data", engine, if_exists="replace", index=False)
            print(f"Успішно завантажено {len(df)} рядків у таблицю 'raw_data'")
            break
        except Exception as e:
            print(f"Спроба {i + 1}: База ще не готова... чекаємо. ({e})")
            time.sleep(5)


if __name__ == "__main__":
    load_data()