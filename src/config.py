from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOADS_DIR = BASE_DIR / "data" / "uploads"
CHROMA_DIR = BASE_DIR / "data" / "chroma"
MANIFEST_FILE = BASE_DIR / "data" / "manifest.json"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = "embeddinggemma:latest"
COHERE_API_KEY = "i8T8Mj2fmVvh8HwkvDrrYq10ypN1jSWbAJyAt1Hl"