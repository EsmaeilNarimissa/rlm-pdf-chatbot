"""
Utility functions for RLM PDF Chatbot UI.
"""
import unicodedata
import io
import os
import fitz  # pymupdf
from rlm import RLM
from rlm.logger import RLMLogger


def normalize_text(text: str) -> str:
    """
    Normalize Unicode text to ASCII-compatible characters.
    This fixes Windows encoding issues with special characters.
    """
    # Normalize Unicode (e.g., − to -)
    text = unicodedata.normalize("NFKC", text)
    
    # Replace common problematic characters
    replacements = {
        '\u2212': '-',  # Unicode minus sign
        '\u2013': '-',  # En dash
        '\u2014': '-',  # Em dash
        '\u2018': "'",  # Left single quote
        '\u2019': "'",  # Right single quote
        '\u201c': '"',  # Left double quote
        '\u201d': '"',  # Right double quote
        '\u2026': '...',  # Ellipsis
        '\u00a0': ' ',  # Non-breaking space
        '\u2217': '*',  # Asterisk operator
        '\u2022': '-',  # Bullet
        '\u00b7': '-',  # Middle dot
        '\u2192': '->',  # Right arrow
        '\u2190': '<-',  # Left arrow
        '\u2264': '<=',  # Less than or equal
        '\u2265': '>=',  # Greater than or equal
        '\u00d7': 'x',  # Multiplication sign
        '\u00f7': '/',  # Division sign
        '\u221a': 'sqrt',  # Square root
        '\u03b1': 'alpha',  # Greek alpha
        '\u03b2': 'beta',  # Greek beta
        '\u03b3': 'gamma',  # Greek gamma
        '\u03bb': 'lambda',  # Greek lambda
        '\u03c0': 'pi',  # Greek pi
        '\u03c3': 'sigma',  # Greek sigma
        '\u03bc': 'mu',  # Greek mu
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    
    # Final pass: encode to ASCII, replacing any remaining problematic chars
    text = text.encode('ascii', errors='replace').decode('ascii')
    
    return text


def extract_text_from_pdfs(uploaded_files) -> str:
    """
    Extracts text from a list of uploaded PDF files using PyMuPDF.
    Better handling of tables, complex layouts, and formatted text.

    Args:
        uploaded_files: List of Streamlit UploadedFile objects.

    Returns:
        Concatenated text from all PDFs.
    """
    all_text = []

    for file in uploaded_files:
        try:
            # Read file bytes
            file_bytes = file.read()
            file.seek(0)  # Reset for potential re-read

            # Open with PyMuPDF
            doc = fitz.open(stream=file_bytes, filetype="pdf")

            file_text = [f"\n{'='*60}\nFILE: {file.name}\n{'='*60}\n"]

            for page_num, page in enumerate(doc, start=1):
                # Extract text with better formatting preservation
                text = page.get_text("text")

                if text.strip():
                    file_text.append(f"\n--- Page {page_num} ---\n")
                    file_text.append(normalize_text(text))

            doc.close()
            all_text.append("".join(file_text))

        except Exception as e:
            all_text.append(f"\n[Error reading {file.name}: {e}]\n")

    return "\n".join(all_text)

# Anti-hallucination prefix to prepend to user questions
# NOTE: We do NOT use custom_system_prompt because it REPLACES the RLM's
# critical REPL instructions. Instead, we add this to the root_prompt.
# Keep it soft to allow conversational follow-ups.
STRICT_QUERY_PREFIX = """When answering, prefer information from the document in the context variable.
Cite specific passages when possible.

User question: """


def get_rlm(backend: str, model_name: str, api_key: str, base_url: str = None) -> RLM:
    """
    Factory function to create an RLM instance based on selected backend.

    Args:
        backend: One of "openai", "gemini", or "vllm" (for Ollama).
        model_name: The model name to use.
        api_key: API key for the backend.
        base_url: Base URL for vllm/Ollama backend.

    Returns:
        Configured RLM instance.
    """
    backend_kwargs = {"model_name": model_name}

    if backend == "vllm":  # Ollama
        backend_kwargs["base_url"] = base_url
        backend_kwargs["api_key"] = api_key if api_key else "ollama"
    elif backend == "openai":
        backend_kwargs["api_key"] = api_key
    elif backend == "gemini":
        backend_kwargs["api_key"] = api_key

    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)
    logger = RLMLogger(log_dir=log_dir)

    return RLM(
        backend=backend,
        backend_kwargs=backend_kwargs,
        environment="local",
        persistent=True,
        verbose=True,  # Enable to see progress in terminal
        max_iterations=30,  # Default value - ensures complete answers
        logger=logger,  # Save execution traces for debugging
        # NOTE: Do NOT use custom_system_prompt - it replaces critical REPL instructions!
        # NOTE: RLM's FINAL() regex has issues with parentheses in content - may truncate
    )
