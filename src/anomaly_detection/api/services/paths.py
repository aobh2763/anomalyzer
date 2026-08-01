from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent

LOGS_DIR = PROJECT_DIR / "storage/logs"
FEATURES_DIR = PROJECT_DIR / "storage/features"
TRANSFORMERS_DIR = PROJECT_DIR / "storage/transformers"
RESULTS_DIR = PROJECT_DIR / "storage/results"
