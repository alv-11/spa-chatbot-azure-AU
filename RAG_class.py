

from embeddings import Embeddings
from LLM import LLM
from retriever import Retriever


class RAGPipeline:
    def __init__(self, config):
        self.embeddings_model = Embeddings(config["models"]["embeddings"])
        self.retriever = Retriever(config["database"]["chroma_path"])
        self.llm = LLM(config["models"]["llm"])
        

    def process_query(self, query):

        # Transformar la query en texto natural a embedding
        query_embedding = self.embeddings_model.get_embedding(query)
        # Buscar en ChromaDB los K documentos más similares
        context = self.retriever.search(query_embedding, k=5)
        response =self.llm.generate_response(query, context)
        return response