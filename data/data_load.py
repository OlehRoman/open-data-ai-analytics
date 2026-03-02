from pathlib import Path
import kagglehub
import sys

try:
    BASE_DIR = Path(__file__).resolve().parent
    RAW_DIR = BASE_DIR / "raw"
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    print("Починаю завантаження датасету...")
    path = kagglehub.dataset_download("elemento/nyc-yellow-taxi-trip-data")
    print("Downloaded to:", path)

except Exception as e:
    print(f"Помилка при завантаженні: {e}")
    sys.exit(1)