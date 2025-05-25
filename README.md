# Gemini Chat Wizard: In-Depth Documentation

## 🚀 Project Overview

The Gemini Chat Wizard is a sophisticated yet user-friendly web application designed to serve as a powerful AI coding assistant. Built with Python, it leverages the **Streamlit** framework for its interactive user interface and **LangChain** for its core logic, orchestrating communication with **Google's powerful Gemini family of models**.

This application is more than just a simple chatbot. It's a stateful assistant that maintains conversational context, allowing for follow-up questions and complex, multi-turn dialogues about code. It provides a secure way for users to input their API credentials and offers customization options for the AI's behavior. This document provides a comprehensive deep dive into its architecture, code, and functionality.

---

## ✨ Features Deep Dive

* **Interactive Chat Interface**: The application utilizes Streamlit's chat elements (`st.chat_message`, `st.chat_input`) to create a familiar and intuitive messaging experience. Custom CSS is injected to create a unique, modern, and polished look and feel.
* **Stateful Conversation**: The wizard remembers previous turns in the conversation. This is achieved by storing the entire message history in Streamlit's `session_state` and passing it to the language model with every new query.
* **Real-Time Streaming Responses**: To enhance user experience, the AI's response is streamed word-by-word in real-time. This is accomplished using the `.stream()` method in LangChain and Streamlit's `st.write_stream`, giving immediate feedback and making the application feel more responsive.
* **Selectable AI Models**: Users can choose from a curated list of Gemini models via a dropdown menu in the sidebar. [cite: 1] This allows them to balance between performance, cost, and capability depending on their needs. The available models are `gemini-2.0-flash`, `gemini-2.0-flash-lite`, `gemini-2.5-flash-preview-04-17`, and `gemini-2.5-flash-preview-05-20`. [cite: 1]
* **Adjustable Creativity**: A "Creativity" slider in the sidebar allows users to control the `temperature` of the AI model. [cite: 1] A lower value (e.g., 0.1) makes the output more deterministic and factual, which is ideal for precise coding tasks. A higher value (e.g., 0.9) encourages more creative and diverse responses.
* **Secure & Validated API Key Handling**: The application prompts for a Google API key using a password input field (`type="password"`) to obscure the entry. [cite: 1] The key is validated by attempting to initialize the LLM, providing immediate feedback to the user on its validity before it is used for chat operations. The key is stored securely in the `session_state` and is never exposed in the client-side code.

---

## 🛠️ Getting Started

Follow these instructions to set up and run the Gemini Chat Wizard on your local machine.

### Prerequisites

* **Python**: Version 3.7 or newer.
* **Google API Key**: You must have a valid Google API key with the Gemini API enabled. You can acquire one from the [Google AI Studio](https://aistudio.google.com/).
* **Virtual Environment (Recommended)**: It is a best practice to create a virtual environment to manage project dependencies and avoid conflicts.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

### Installation

1.  **Project Files**: Ensure you have the `app.py` file.
2.  **Dependencies**: Create a `requirements.txt` file with the following content[cite: 1]:
    ```txt
    langchain_google_genai
    langchain_core
    streamlit
    python-dotenv
    ```
3.  **Install from `requirements.txt`**: Use pip to install all the necessary packages.
    ```bash
    pip install -r requirements.txt
    ```

### Local Configuration

The application uses a `.env` file for easy management of the API key during local development, loaded by the `python-dotenv` library.

1.  **Create `.env` file**: In the same directory as `app.py`, create a file named `.env`.
2.  **Add API Key**: Add your Google API Key to this file. The application will use this as a fallback if one is not provided in the sidebar.
    ```
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
    ```

### Running the Application

With the environment activated and dependencies installed, start the Streamlit server.

```bash
streamlit run app.py