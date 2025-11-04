from sentence_transformers import SentenceTransformer

class Embeddings:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)  # Cargar el modelo según config.yaml
    
    def get_embedding(self, text):
        return self.model.encode(text)  # Convertir texto a embedding