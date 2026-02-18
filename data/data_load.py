from pathlib import Path
import kagglehub

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

path = kagglehub.dataset_download(
    "elemento/nyc-yellow-taxi-trip-data",
    path=str(RAW_DIR)
)

print("Downloaded to:", path)
