import chromadb

class Retriever:
    def __init__(self, db_path):
        self.client = chromadb.PersistentClient(db_path)
        self.collection = self.client.get_or_create_collection("RAG_pdf_tratamientos_del_spa")

    def insert_chunks(self, chunks,chunk_embeddings):
        for i, chunk in enumerate(chunks):
            
            self.collection.add(
                documents=[chunk], 
                embeddings=[chunk_embeddings[i]], 
                ids=[str(i)]
            )

    def search(self, query_embedding, k):
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=["documents", "embeddings"]
        )
        return results