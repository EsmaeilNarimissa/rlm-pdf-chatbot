"""
RLM PDF Chatbot - Streamlit Application

A chat interface for querying PDFs using Recursive Language Models.
Supports OpenAI, Gemini, and Ollama backends.
"""
import os
import streamlit as st
from dotenv import load_dotenv
from utils import extract_text_from_pdfs, get_rlm, STRICT_QUERY_PREFIX

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment (can be overridden in UI)
DEFAULT_OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")
DEFAULT_GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

# --- Page Configuration ---
st.set_page_config(
    page_title="RLM PDF Chat",
    page_icon="📄",
    layout="wide",
)

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "rlm_instance" not in st.session_state:
    st.session_state.rlm_instance = None
if "pdf_context" not in st.session_state:
    st.session_state.pdf_context = None
if "context_loaded" not in st.session_state:
    st.session_state.context_loaded = False

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Configuration")

    # Backend Selection
    backend_display = st.selectbox(
        "Backend",
        ["OpenAI", "Gemini", "Ollama"],
        help="Select the LLM backend to use."
    )

    # Map display name to RLM backend name
    backend_map = {
        "OpenAI": "openai",
        "Gemini": "gemini",
        "Ollama": "vllm",
    }
    backend = backend_map[backend_display]

    # Model Selection based on backend
    if backend_display == "OpenAI":
        model_name = st.selectbox(
            "Model",
            ["gpt-5.1", "gpt-5-mini", "gpt-5-nano", "gpt-4o", "gpt-4-turbo"],
            index=1,  # Default to gpt-5-mini (Reader)
            help="GPT-5 series recommended for RLM."
        )
        if DEFAULT_OPENAI_KEY:
            st.success("✓ API Key loaded from .env")
            api_key = DEFAULT_OPENAI_KEY
            with st.expander("Override API Key"):
                override_key = st.text_input("Enter different key", type="password", key="openai_override")
                if override_key:
                    api_key = override_key
        else:
            api_key = st.text_input("OpenAI API Key", type="password")
        base_url = None

    elif backend_display == "Gemini":
        model_name = st.selectbox(
            "Model",
            ["gemini-2.5-pro", "gemini-2.5-flash-lite", "gemini-2.0-flash"],
            index=1,  # Default to flash-lite (Reader)
            help="Gemini 2.5 series recommended for RLM."
        )
        if DEFAULT_GEMINI_KEY:
            st.success("✓ API Key loaded from .env")
            api_key = DEFAULT_GEMINI_KEY
            with st.expander("Override API Key"):
                override_key = st.text_input("Enter different key", type="password", key="gemini_override")
                if override_key:
                    api_key = override_key
        else:
            api_key = st.text_input("Gemini API Key", type="password")
        base_url = None

    else:  # Ollama
        base_url = st.text_input(
            "Ollama Base URL",
            value="http://localhost:11434/v1",
            help="URL of your local Ollama server."
        )
        model_name = st.text_input(
            "Model Name",
            value="llama3",
            help="Enter the Ollama model name (e.g., llama3, mistral, qwen2)."
        )
        api_key = st.text_input(
            "API Key (optional)",
            value="ollama",
            type="password",
            help="Usually not required for local Ollama."
        )

    st.divider()

    # PDF Upload
    st.subheader("📄 Upload PDFs")
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type="pdf",
        accept_multiple_files=True,
        help="Upload one or more PDF files to query."
    )

    # Process PDFs Button
    if st.button("🚀 Load PDFs & Initialize", type="primary", use_container_width=True):
        if not uploaded_files:
            st.error("Please upload at least one PDF file.")
        elif not api_key and backend_display != "Ollama":
            st.error(f"Please enter your {backend_display} API Key.")
        else:
            with st.spinner("Extracting text from PDFs..."):
                pdf_text = extract_text_from_pdfs(uploaded_files)
                st.session_state.pdf_context = pdf_text

            with st.spinner("Initializing RLM..."):
                try:
                    rlm = get_rlm(backend, model_name, api_key, base_url)
                    st.session_state.rlm_instance = rlm
                    st.session_state.context_loaded = True
                    st.session_state.messages = []  # Reset chat history
                    st.success(f"✅ Loaded {len(uploaded_files)} PDF(s) with {len(pdf_text):,} characters.")
                except Exception as e:
                    st.error(f"Failed to initialize RLM: {e}")

    # Status indicator
    if st.session_state.context_loaded:
        st.success("Context loaded. Ready to chat!")
    else:
        st.info("Upload PDFs and click 'Load' to start.")

# --- Main Chat Interface ---
st.title("📚 RLM PDF Chatbot")
st.caption("Ask questions about your uploaded PDFs using Recursive Language Models.")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about your PDFs..."):
    if not st.session_state.context_loaded:
        st.error("Please load PDFs first using the sidebar.")
    else:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get RLM response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    rlm = st.session_state.rlm_instance
                    context = st.session_state.pdf_context

                    # Call RLM completion with strict prefix for anti-hallucination
                    full_prompt = STRICT_QUERY_PREFIX + prompt
                    response = rlm.completion(
                        prompt=context,
                        root_prompt=full_prompt
                    )

                    answer = response.response
                    if answer is None:
                        answer = "I could not generate a response. The document may not contain relevant information for this question, or the model encountered an issue."
                    
                    st.markdown(answer)

                    # Add assistant message to history
                    st.session_state.messages.append({"role": "assistant", "content": answer})

                except Exception as e:
                    error_msg = f"Error: {e}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
