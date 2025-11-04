from processing_pdf import PDFPreprocessor
from embeddings import Embeddings
from retriever import Retriever



# Inicializar la base de datos antes de arrancar Flask
def initialize_database(config):

    # Paso 1: Obtener oraciones procesadas
    preprocessor = PDFPreprocessor(config["preprocessing"]["spacy_model"],config["preprocessing"]["db_path"])
    texto_pdf = preprocessor.extraer_texto_pdf()
    import pdb;pdb.set_trace()

    # Paso 2: Crear chunks con sliding window
    chunks = preprocessor.sliding_window_spacy(
        texto=texto_pdf,
        window_size=100,  # tokens por chunk
        stride=25         # overlap entre chunks
    )
    import pdb;pdb.set_trace()

    # Paso 3: Generar embeddings para cada chunk
    embeddings_model = Embeddings(config["models"]["embeddings"])
    chunk_embeddings = [embeddings_model.get_embedding(chunk) for chunk in chunks]

    # Paso 4: Insertar en ChromaDB
    retriever = Retriever(config["database"]["chroma_path"])
    retriever.insert_chunks(chunks,chunk_embeddings)