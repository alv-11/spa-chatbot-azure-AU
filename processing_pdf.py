import fitz  # PyMuPDF
import spacy

class PDFPreprocessor:
    def __init__(self, spacy_model, pdf_path):
        self.nlp = spacy.load(spacy_model)
        self.pdf_path = pdf_path

    def extraer_texto_pdf(self):
        texto = ""
        with fitz.open(self.pdf_path) as doc:
            for page in doc:
                texto += page.get_text()
        return texto
    # Para hacer Sliding Window Chunking
    #stride significa cuanto me muevo hacia la derecha con cada window_size es decir que el overlap es de 50
    def sliding_window_spacy(self,texto, window_size=100, stride=25):
        doc = self.nlp(texto)
        tokens = [token.text for token in doc if not token.is_space]
        chunks = []
        
        for i in range(0, len(tokens), stride):
            window = tokens[i:i + window_size]
            if not window:
                break
            chunk = " ".join(window)
            chunks.append(chunk)

            if i + window_size >= len(tokens):
                break
        
        return chunks 

