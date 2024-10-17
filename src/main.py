import os
import json
import streamlit as st
from groq import Groq

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Asistente Virtual Inteligente",
    page_icon="🤖",
    layout="centered"
)   

# Título principal de la aplicación
st.title("🤖 Asistente Virtual de Análisis de Datos")
st.markdown("### Aquí para resolver tus dudas sobre análisis de datos y guiarte en cada paso.")

# Establecer el directorio de trabajo y cargar la configuración
working_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(working_dir, "config.json")

# Cargar la API key de Groq
if os.path.exists(config_path):
    with open(config_path, "r") as f:
        config_data = json.load(f)
    GROQ_API_KEY = config_data.get("GROQ_API_KEY")
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY
else:
    st.error("El archivo config.json no existe. Por favor, crea este archivo y agrega tu GROQ_API_KEY.")

# Inicializar el cliente de Groq (Llama 3.1)
client = Groq()

# Cargar el contenido del archivo de conocimiento único
def cargar_contenido():
    data_dir = os.path.join(working_dir, "data")
    knowledge_file = os.path.join(data_dir, "informacion_completa.txt")
    if os.path.exists(knowledge_file):
        with open(knowledge_file, "r", encoding="utf-8") as file:
            contenido = file.read()
        return contenido.strip()
    else:
        st.error("El archivo informacion_completa.txt no existe en la carpeta 'data'.")
        return ""

# Cargar la base de conocimiento
knowledge_text = cargar_contenido()

# Definir el prompt inicial con el rol del asistente
prompt_inicial = """
Eres un asistente virtual de atención al cliente para un freelancer de análisis de datos. A lo largo de esta conversación, tu misión principal es guiar al usuario, resolver sus dudas y dirigirlo a agendar una videollamada con el equipo de ventas, de acuerdo a las siguientes pautas:

### [Contexto y Reglas Generales]
1. Responde únicamente utilizando la información de la base de conocimientos proporcionada. Tus respuestas deben estar sintetizadas.
2. Si no tienes una respuesta dentro de la base de conocimientos, responde amablemente: "No tengo esa información en este momento". No inventes información que no esté dentro de la base de conocimmientos (Esto es importante).
3. Mantén la conversación centrada en **temas de análisis de datos** y **servicios** ofrecidos por el freelancer.
4. **No** proporcionas presupuestos, descuentos ni recibes datos personales. Indica que estos temas se revisan durante la videollamada con el equipo de ventas.
5. No trabajamos con datos no estructurados, ni realizamos web scraping.
6. Si te solicitan información sobre precios, presenta la información en formato tabla. Los únicos precios que conoces son los de la base de conocimiento, no existen otros tipos de precios.
7. Si te solicitan información sobre entregables (productos por servicios) presenta la información en formato tabla.
8. Redirige cualquier consulta no relacionada a los servicios con un mensaje breve y regresa a temas de análisis de datos o a las siguientes categorías:
   - **Servicios**
   - **Pricing**
   - **Metodología de Trabajo**
   - **Flujo de Contratación**
   - **Términos y Condiciones**
   - **Modalidades de Contratación**
   - **Preguntas Frecuentes**

### [Estrategia de Conversación]
#### **Fase 1: Conciencia**
- **Objetivo:** Identificar los principales retos del usuario en cuanto a análisis de datos.
- **Acción:** Realiza una pregunta abierta para entender el problema principal (ejemplo: "¿Cuál es el mayor desafío que enfrenta con sus datos actualmente?").
- **Respuesta Ideal:** Basándote en su respuesta, menciona cuál de nuestros servicios puede abordar ese reto de manera específica.

#### **Fase 2: Consideración**
- **Objetivo:** Profundizar en sus necesidades con **dos preguntas específicas**.
- **Acción:** Realiza preguntas cortas enfocadas en:
   1. Entender la estructura de sus datos (¿Qué tipo de datos maneja actualmente?)
   2. Clarificar sus expectativas (¿Qué resultados esperas obtener con este análisis?)
- **Respuesta Ideal:** Resalta cómo nuestros servicios pueden alinearse con sus necesidades y ofrece una descripción breve de un servicio que podría encajar con su caso.

#### **Fase 3: Decisión**
- **Objetivo:** Guiar la conversación hacia agendar una videollamada como el próximo paso lógico.
- **Acción:** Sugiere la videollamada diciendo: "Puedo ayudarte a organizar una reunión con el equipo para revisar más a detalle tu situación y ofrecerte una propuesta personalizada. ¿Te gustaría agendar una videollamada?"
- **Respuesta Ideal:** Proporciona el enlace de **Calendly**: [Calendly](https://calendly.com/jimenezdata7/30min) y recuerda amablemente que solo el usuario puede agendar la llamada.

### [Estilo de Conversación]
1. Mantén un tono amigable, profesional y preciso.
2. Evita respuestas largas o complejas. Cada respuesta debe ser **corta, directa y sencilla**.
3. Si el usuario se desvía del tema, redirige la conversación con frases como: "Esa es una buena pregunta, pero me gustaría saber más sobre cómo podemos ayudarte con tus datos."
"""

# Inicializar el historial de chat y el estado del mensaje de bienvenida
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "mensaje_bienvenida_mostrado" not in st.session_state:
    st.session_state.mensaje_bienvenida_mostrado = False

# Mostrar mensaje de bienvenida solo si no ha sido mostrado antes
if not st.session_state.mensaje_bienvenida_mostrado:
    mensaje_bienvenida = """
    ¡Hola! Soy tu asistente virtual de análisis de datos. 😊
    
    Estoy aquí para ayudarte a descubrir cómo nuestros servicios pueden resolver tus desafíos con los datos y responder cualquier duda que tengas, como:

    - **Nuestros servicios** 📊
    - **Modalidades de Contratación** ⚖️
    - **Flujo de Contratación** 🤝
    - **Precios** 💰
    - **Productos entregados por servicio** 📬
    - **Metodología de Trabajo** 🔍
    - **Términos y Condiciones** 📑
    - **Preguntas Frecuentes** 🤔

    Si no estás seguro de qué servicio es el adecuado para ti, solo cuéntame en pocas palabras lo que necesitas y te recomendaré la mejor solución.    
    
    ¿Tienes alguna duda específica? ¡Estoy listo para guiarte! Y si ya sabes lo que buscas, puedo ayudarte a agendar una videollamada con nuestro equipo de ventas para afinar los detalles.

    ¡Dime, en qué puedo ayudarte hoy?

    _Nota: Los modelos de lenguaje son confiables, pero ocasionalmente pueden generar errores. Por favor, considere la información como una guía y no como un recurso oficial._

    """
    st.session_state.chat_history.append({"role": "assistant", "content": mensaje_bienvenida})
    st.session_state.mensaje_bienvenida_mostrado = True  # Marcar como mostrado

# Mostrar el historial de chat
for message in st.session_state.chat_history:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(message["content"])

# Campo de entrada para el usuario
user_input = st.chat_input("Escribe tu pregunta aquí...")

if user_input:
    # Mostrar el mensaje del usuario
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Construir el mensaje al modelo con el rol extendido y el conocimiento
    messages = [
        {"role": "system", "content": prompt_inicial},
        {"role": "system", "content": knowledge_text},
    ] + st.session_state.chat_history[-5:]  # Limitar el historial para no exceder el contexto

    # Obtener la respuesta del modelo
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        #max_tokens=500,
        temperature=0.3  # Ajuste de temperatura a un valor bajo para mantener respuestas más consistentes y controladas
    )
    assistant_response = response.choices[0].message.content.strip()

    # Mostrar la respuesta del asistente
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
