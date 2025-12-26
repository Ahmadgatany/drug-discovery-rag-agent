from sentence_transformers import SentenceTransformer
from core.config import Config

class LocalEmbedder:
    def __init__(self):
        self.model = SentenceTransformer(
            Config.EMBEDDING_MODEL_NAME, 
            device=Config.DEVICE
        )
        print(f"[*] Local Embedder loaded on {Config.DEVICE}")

    def encode(self, text):
        # Convert the text into a vector (list of floats) to be compatible with ChromaDB
        return self.model.encode(text, convert_to_numpy=True).tolist()