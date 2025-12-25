from sentence_transformers import SentenceTransformer
from core.config import Config

class LocalEmbedder:
    def __init__(self):
        # تحميل الموديل على الـ GPU (cuda) مباشرة
        self.model = SentenceTransformer(
            Config.EMBEDDING_MODEL_NAME, 
            device=Config.DEVICE
        )
        print(f"[*] Local Embedder loaded on {Config.DEVICE}")

    def encode(self, text):
        # تحويل النص لمتجه (List of floats) ليتوافق مع ChromaDB
        return self.model.encode(text, convert_to_numpy=True).tolist()