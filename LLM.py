
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from langsmith import traceable
from groq import Groq
import os

class LLM:
    def __init__(self, model_name):
        # Cargar el archivo .env
        load_dotenv()

        api_key = os.getenv("HF_API_KEY")
        if not api_key:
            raise ValueError("Por favor, establece la variable de entorno HF_API_KEY con tu token de Hugging Face.")
 
        # Cargar la configuración desde el archivo .env
        os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
        os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING")
        os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")
        
        self.model_name = model_name  # Obtener el modelo del YAML
        
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY"),
        )

    def generate_response(self, consulta_usuario, contexto_documentos):
        
        messages = [
            {"role": "system", "content": "Eres un asistente virtual experto en los servicios del Spa del Castillo de Gorraiz en Navarra."
            "Tu función es responder de manera no muy extensa preguntas sobre tratamientos, rituales, circuitos termales, horarios y recomendaciones del spa."
            "Evita inventar datos."
            }, 

            {"role": "user", "content": f"Consulta del usuario (importante): {consulta_usuario}"},
            {"role": "system", "content": f"Contexto relevante: {contexto_documentos} (útil solo si es necesario)"}
        ]

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            
        )
         
        return response.choices[0].message.content
    
    
    
