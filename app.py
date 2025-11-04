
import streamlit as st
from RAG_class import RAGPipeline
from initialize_database import initialize_database
import yaml

# Cargar configuración desde config.yaml
with open("config.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

# Inicializar la base de datos solo la primera vez
if "retriever" not in st.session_state:
    st.session_state.retriever = initialize_database(config)
    st.session_state.database_initialized = True
else:
    # Si ya está inicializada, usamos el retriever guardado
    retriever = st.session_state.retriever


# Crear instancia de la pipeline RAG
rag_pipeline = RAGPipeline(config)


st.title("Bienvenido al Asistente Virtual del Spa Castillo de Gorraiz 💆‍♀️")
st.markdown(
    """ 
    Relájate y déjate guiar por nuestro asistente virtual.  
    Estoy aquí para ayudarte a descubrir los tratamientos, circuitos y experiencias del **Spa del Castillo de Gorraiz**, un espacio de bienestar único en Navarra.

    ## **¿Qué puedo hacer por ti?**
    💦 **Descubre nuestros tratamientos →** Pregunta por masajes, rituales, circuitos termales o tratamientos faciales y corporales.

    🕯️ **Resuelve tus dudas →** Consulta precios, duración, recomendaciones o qué servicios combinan mejor según tus necesidades.

    🌿 **Planifica tu visita →** Te ayudaré a conocer las opciones disponibles para que disfrutes al máximo de tu experiencia en el spa.
    """
)
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hola 😊 Soy el asistente virtual del Spa Castillo de Gorraiz. "
            "Puedo contarte todo sobre nuestros tratamientos, circuitos termales y servicios de bienestar. "
            "¿Sobre qué te gustaría saber más hoy?"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
# Aceptar la entrada del usuario
# Cuando el usuario escribe una pregunta o mensaje el código llega aquí
if prompt := st.chat_input("Pregunta lo que quieras sobre nuestros servicios"):
    # Agregar mensaje del usuario al historial de chat
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = rag_pipeline.process_query(prompt)  # Usar el LLM para las consultas
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Mostrar mensaje del usuario en la interfaz
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Mostrar mensaje de la respuesta del asistente
    with st.chat_message("assistant"):
        st.markdown(response) 