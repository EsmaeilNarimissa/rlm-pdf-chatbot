
---

<h1 align="center" style="font-size:2.8em">
<span>RLM PDF Chatbot</span>
</h1>

<p align="center" style="font-size:1.2em">
  A Streamlit-based PDF Question Answering interface powered by <a href="https://github.com/alexzhang13/rlm">Recursive Language Models (RLMs)</a>
</p>

<p align="center">
  <a href="https://arxiv.org/abs/2512.24601">RLM Paper</a> •
  <a href="https://alexzhang13.github.io/blog/2025/rlm/">RLM Blogpost</a> •
  <a href="https://alexzhang13.github.io/rlm/">RLM Documentation</a>
</p>

---

## 🎯 What is This?

This is a **fork of [alexzhang13/rlm](https://github.com/alexzhang13/rlm)** with:
- A **Streamlit PDF Chatbot UI** for asking questions about PDF documents
- **Bug fixes** to the core RLM framework
- **Multi-backend support** (OpenAI, Gemini, Ollama)

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
```

### 2. Set Up API Keys
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Run the PDF Chatbot
```bash
streamlit run ui/app.py
```

### 4. Upload a PDF and Ask Questions!

---

## ✨ Features

### PDF Chatbot Interface (`ui/`)
| Feature | Description |
|---------|-------------|
| **Drag-and-Drop PDF Upload** | Single or multiple PDF files |
| **Backend Selection** | OpenAI (GPT-5), Gemini (2.5), or Ollama (local) |
| **Chat Interface** | Persistent chat history with the RLM |
| **Anti-Hallucination** | Encourages document-based answers with citations |
| **Secure API Keys** | Auto-loads from `.env`, allows UI overrides |

### RLM Core Bug Fixes
| Bug | Fix |
|-----|-----|
| `FINAL()` parsing truncation | Balanced parenthesis counting algorithm |
| `FINAL_VAR()` parsing truncation | Same balanced parenthesis fix |
| `globals()/locals()` blocked | Enabled in `_SAFE_BUILTINS` |

---

## 📂 Project Structure

```
ui/                         # NEW: PDF Chatbot UI
├── app.py                  # Streamlit application
├── utils.py                # PDF extraction, RLM factory
└── logs/                   # Execution traces (created at runtime)

rlm/                        # RLM Core (with bug fixes)
├── core/                   # RLM engine
├── clients/                # API clients (OpenAI, Gemini, etc.)
├── environments/           # REPL sandboxes
│   └── local_repl.py       # Fixed: globals()/locals() enabled
└── utils/
    └── parsing.py          # Fixed: balanced parenthesis parsing
```

---

## 🔧 Configuration

### Environment Variables (`.env`)
```ini
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
```

### UI Settings
| Setting | Default | Description |
|---------|---------|-------------|
| `max_iterations` | 30 | Maximum RLM iterations per query |
| `verbose` | True | Show progress in terminal |
| `persistent` | True | Maintain REPL state between queries |

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Rate Limits (429)** | Switch from Gemini Free Tier to OpenAI or Ollama |
| **Slow Responses** | Large PDFs take time. Check terminal for verbose logs |
| **Truncated Answers** | Check `ui/logs/*.jsonl` for full RLM traces |
| **NoneType Errors** | Restart Streamlit server after code changes |

---

## 📖 About RLM (Recursive Language Models)

Recursive Language Models (RLMs) are a task-agnostic inference paradigm for language models (LMs) to handle near-infinite length contexts by enabling the LM to *programmatically* examine, decompose, and recursively call itself over its input.

RLMs replace the canonical `llm.completion(prompt, model)` call with a `rlm.completion(prompt, model)` call. RLMs offload the context as a variable in a REPL environment that the LM can interact with and launch sub-LM calls inside of.

### Citation
```bibtex
@misc{zhang2025recursivelanguagemodels,
      title={Recursive Language Models}, 
      author={Alex L. Zhang and Tim Kraska and Omar Khattab},
      year={2025},
      eprint={2512.24601},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2512.24601}, 
}
```

---

## 🔗 Links

- **Original RLM**: [github.com/alexzhang13/rlm](https://github.com/alexzhang13/rlm)
- **RLM Paper**: [arxiv.org/abs/2512.24601](https://arxiv.org/abs/2512.24601)
- **RLM Blogpost**: [alexzhang13.github.io/blog/2025/rlm](https://alexzhang13.github.io/blog/2025/rlm/)

---

## 📜 License

This project is a fork of [alexzhang13/rlm](https://github.com/alexzhang13/rlm). See the original repository for license details.
