# import necessary libraries
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

# Custom CSS for new layout
st.markdown("""
<style>
body {
    background-color: #f0f4f8;
    color: #222;
    font-family: 'Segoe UI', sans-serif;
}

/*section[data-testid="stSidebar"] {
    background: linear-gradient(to bottom right, #6366f1, #a78bfa);
    color: white;
}*/
            
section[data-testid="stSidebar"] {
background: linear-gradient(to bottom right, #a5b4fc, #ddd6fe); /* lighter purples */
color: #1f1f1f; /* dark gray text for contrast */
}

h1, h2, h3, h4 {
    color: #3b0764;
}

.stChatMessage {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 1rem;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    margin-bottom: 0.5rem;
}

.stChatMessage[data-testid="chat-message-user"] {
    background-color: #e0e7ff;
    align-self: flex-end;
}

.stChatMessage[data-testid="chat-message-ai"] {
    background-color: #ede9fe;
}
            
.stButton > button {
        background-color: #FFFFFF;  /* white*/
        color: black;               /* text color */
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
        /*border: 1px solid #555;*/
}
            
/* Chat input styling */
input[type="text"] {
    border-radius: 8px;
    border: 1px solid #ccc;
    padding: 0.5rem;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# Title and header
st.markdown("""
<div style='background: linear-gradient(to bottom right, #6366f1, #a78bfa); padding: 1rem 2rem; border-radius: 12px; color: white;'>
<h1 style='margin-bottom:0;'>💬 Gemini Chat Wizard</h1>
<p style='margin-top:0;'>Your magical coding assistant powered by LangChain + Gemini</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state for api_key and submission
if "api_key_submitted" not in st.session_state:
    st.session_state.api_key_submitted = False

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# Function to test gemini api key
def test_api_key_validity(api_key: str) -> bool:
    try:
        ChatGoogleGenerativeAI(model = "gemini-2.0-flash", api_key=api_key)
        return True
    except Exception as e:
        return False

# Sidebar configuration
with st.sidebar:
    st.header("✨ Settings")
    selected_model = st.selectbox("Choose a Model", ["gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-2.5-flash-preview-04-17", "gemini-2.5-flash-preview-05-20"], index=0)

    # Add slider for creativity
    creativity = st.slider("Creativity", 0.0, 1.0, 0.3)

    # Input for API Key (use `type="password"` to hide the key)
    api_key_input = st.text_input("Enter your Google API Key", type="password")

    # Submit button if API key is successfully submitted
    isSubmitted = st.button("Submit")

    # Submit button
    if isSubmitted:
        # Test api key
        isAuthenticated = test_api_key_validity(api_key_input)
        if isAuthenticated:
            st.session_state.api_key = api_key_input
            st.session_state.api_key_submitted = True
            st.success("API Key is authenticated.")
        else:
            st.warning("Please enter a valid API Key.")

    # Markdown statements
    st.markdown("""
    ---
    **Capabilities:**
    - 💻 Code Expert
    - 🪄 Prompt Engineering
    - 🐞 Debugging Genius
    - 🧠 Architecture Advisor

    Powered by [Gemini](https://gemini.google.com/) & [LangChain](https://python.langchain.com)
    Developed by [@aniketaangre](https://github.com/aniketangre)
    """)

# Set the environment variable for the Google API key
os.environ["GOOGLE_API_KEY"] = st.session_state.api_key
# os.environ["GOOGLE_API_KEY"] = str(os.getenv('GOOGLE_API_KEY'))
# os.environ["GOOGLE_API_KEY"] = api_key_input

# Global variable to hold the LLM instance
llm = None
def get_llm_instance():
    """
    Method to return the instance of LLM model globally
    :return: LLM instance
    """
    global llm 
    if llm is None:
        llm = ChatGoogleGenerativeAI(
            model = selected_model,
            stream = True,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            },
            creativity = creativity
        )
    return llm

# Function to get a response from llm model
def get_response(user_query, conversation_history):
    """
    Method to get the response from the LLM model
    :param user_query: User query
    :param conversation_history: Conversation history
    :return: LLM response for user query
    """
    prompt_template = f"""
    You are an expert AI coding assistant. Provide concise and correct solutions. Always respond in English. 
    Answer the following question considering the history of the conversation:

    Chat history: {{conversation_history}}
    
    User question: {{user_query}}
    """

    # Create prompt
    prompt = ChatPromptTemplate.from_template(template = prompt_template)
    llm = get_llm_instance()
    expression_language_chain = prompt | llm | StrOutputParser()

    # note: use  .invoke() method for non-streaming
    return expression_language_chain.stream(
        {
            "conversation_history": conversation_history,
            "user_query": user_query
         }
    )



# Initialize the messages key in streamlit session to store message history 
if "messages" not in st.session_state:
    # add greeting message o user
    st.session_state.messages = [
        AIMessage(content = "Hi! I'm Gemini. How can I help you code today? 💻")
    ]

# if there are messages already in session, write them on app
for message in st.session_state.messages:
    if isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)

# Pass user prompt to the llm
prompt = st.chat_input("Say Something")

if prompt is not None and prompt != "":
    # add the message to chat message container
    if not isinstance(st.session_state.messages[-1], HumanMessage):
        st.session_state.messages.append(HumanMessage(content=prompt))
        # display to the streamlit application
        message = st.chat_message("user")
        message.write(f"{prompt}")

    if not isinstance(st.session_state.messages[-1], AIMessage):
        with st.chat_message("assistant"):
            # use .write() method for non-streaming, which means .invoke() method in chain
            response = st.write_stream(get_response(prompt, st.session_state.messages))
        st.session_state.messages.append(AIMessage(content=response))

