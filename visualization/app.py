import os
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import time


def run_visualization():
    db_url = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/project_db")
    engine = create_engine(db_url)

    plots_path = "/app/static/plots"
    os.makedirs(plots_path, exist_ok=True)

    print("--- Модуль visualization стартував ---")

    df = None
    for i in range(15):
        try:
            df = pd.read_sql("SELECT * FROM raw_data", engine)
            if not df.empty:
                print("Дані для візуалізації отримано.")
                break
        except Exception:
            print(f"Спроба {i + 1}: Очікування таблиці 'raw_data'...")
            time.sleep(5)

    if df is None or df.empty:
        print("Помилка: Не вдалося отримати дані.")
        return

    sns.set_theme(style="whitegrid")

    numeric_df = df.select_dtypes(include=['number'])

    if numeric_df.empty or len(numeric_df.columns) < 2:
        print("Помилка: Недостатньо числових колонок для побудови обох графіків.")
        return

    col1 = numeric_df.columns[0]
    plt.figure(figsize=(10, 6))
    sns.histplot(data=numeric_df, x=col1, kde=True, color='skyblue')
    plt.title(f'Розподіл значень колоноки "{col1}"')
    plt.xlabel(col1)
    plt.ylabel('Частота')
    dist_plot_name = "dist_plot.png"
    plt.savefig(os.path.join(plots_path, dist_plot_name))
    plt.close()
    print(f"Графік 1 (Гістограма) збережено як {dist_plot_name}")

    if len(numeric_df.columns) >= 2:
        col2 = numeric_df.columns[1]
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=numeric_df, x=col1, y=col2, color='coral', alpha=0.7)
        plt.title(f'Взаємозв\'язок "{col1}" та "{col2}"')
        plt.xlabel(col1)
        plt.ylabel(col2)
        scatter_plot_name = "scatter_plot.png"
        plt.savefig(os.path.join(plots_path, scatter_plot_name))
        plt.close()
        print(f"Графік 2 (Діаграма розсіювання) збережено як {scatter_plot_name}")

    print(f"Усі графіки збережено у папку {plots_path}")


if __name__ == "__main__":
    run_visualization()