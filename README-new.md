# RLM PDF Chatbot UI

A Streamlit-based PDF Question Answering interface powered by Recursive Language Models (RLMs).

## 🚀 Features

### Streamlit User Interface (`ui/app.py`)
- **Drag-and-Drop PDF Upload**: Single or multiple PDF files
- **Backend Selection**: OpenAI (GPT-5), Gemini (2.5), or Ollama (local)
- **Chat Interface**: Persistent chat history with the RLM
- **Secure API Keys**: Auto-loads from `.env`, allows UI overrides

### Robust PDF Processing (`ui/utils.py`)
- **PyMuPDF Integration**: Superior text extraction from complex layouts
- **Windows Compatibility**: `normalize_text()` handles Unicode encoding issues

### Anti-Hallucination Mode
- **Query Prefix**: `STRICT_QUERY_PREFIX` encourages document-based answers with citations
- ⚠️ Does NOT use `custom_system_prompt` (it replaces critical REPL instructions)

### Performance & Debugging
- **Safe Iterations**: `max_iterations=30` ensures complete answers
- **RLM Logging**: Execution traces saved to `ui/logs/*.jsonl`
- **Error Handling**: Graceful handling for API errors and rate limits

---

## 🐛 Bug Fixes (RLM Core)

### 1. FINAL() Parsing Bug
**File**: `rlm/utils/parsing.py`
- **Problem**: Regex `r"^\s*FINAL\((.*?)\)"` used non-greedy matching, truncating answers with parentheses like `FINAL(About RLMs (Recursive...)` → `"About RLMs "`
- **Fix**: Replaced with balanced parenthesis counting algorithm

### 2. FINAL_VAR() Parsing Bug  
**File**: `rlm/utils/parsing.py`
- **Problem**: Same non-greedy regex issue as FINAL()
- **Fix**: Applied same balanced parenthesis counting

### 3. custom_system_prompt Conflict
**File**: `ui/utils.py`
- **Problem**: `custom_system_prompt` in `RLM()` **replaces** the entire system prompt, removing REPL instructions (`FINAL()`, `llm_query()`, `context`)
- **Fix**: Use `STRICT_QUERY_PREFIX` prepended to `root_prompt` instead

### 4. globals()/locals() Blocked
**File**: `rlm/environments/local_repl.py`
- **Problem**: `_SAFE_BUILTINS` set `globals` and `locals` to `None`. Model code calling `globals()` threw `TypeError: 'NoneType' object is not callable`
- **Fix**: Enabled `globals` and `locals` in `_SAFE_BUILTINS` (safe in sandboxed namespace)

---

## ✅ Verified Working

**Backend**: GPT-5-mini | **Iterations**: 5 | **Time**: ~60s

```
Q: What is Figure 3 about?

A: Figure 3 is a cost comparison between RLMs and baseline methods.

   Caption: "Figure 3: Cost of RLM and baselines described in §2.2 
   plotted at the 25th, 50th, 75th, and 95th percentile of total 
   API cost. We observe comparable or even lower costs for RLMs at 
   the 50th percentile, but sharp increases at the tail end due to 
   potentially long RLM trajectories."
   
   The plot shows that median RLM runs are cheaper than base model 
   runs, but outliers can be significantly more expensive. RLMs are 
   up to 3x cheaper than summarization baselines.
```

---

## 📂 Setup & Usage

### Install Dependencies
```bash
uv pip install streamlit pymupdf python-dotenv
```

### Environment Variables (`.env`)
```ini
OPENAI_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```

### Run the App
```bash
streamlit run ui/app.py
```

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Rate Limits (429)** | Switch from Gemini Free Tier to OpenAI or Ollama |
| **Slow Responses** | Large PDFs take time. Check terminal for verbose logs |
| **Truncated Answers** | Check `ui/logs/*.jsonl` for full RLM traces |
| **NoneType Errors** | Ensure server was restarted after code changes |

---

## 📁 Directory Structure
```
ui/
├── app.py          # Streamlit application
├── utils.py        # PDF extraction, RLM factory, text normalization
└── logs/           # JSONL execution traces (created at runtime)

rlm/
├── utils/
│   └── parsing.py  # FINAL()/FINAL_VAR() parsing (fixed)
└── environments/
    └── local_repl.py  # REPL sandbox (globals/locals fix)
```

---

## 🚀 Publishing to Your Own GitHub Repository

Follow these steps to maintain your own fork with the improvements.

### Step 1: Fork the Original Repository

1. Go to the original RLM repo: https://github.com/alexzhang13/rlm
2. Click the **"Fork"** button (top right)
3. Choose your GitHub account as the destination
4. This creates `https://github.com/YOUR_USERNAME/rlm`

### Step 2: Clone Your Fork Locally

```bash
# Clone your fork (not the original)
git clone https://github.com/YOUR_USERNAME/rlm.git
cd rlm
```

### Step 3: Copy Your Improved Files

Copy the modified files from your current working directory to the cloned repo:

```bash
# Files you modified (copy these from your working directory)
# Replace C:\Users\esmae\Desktop\RLM\CODE with your actual path

# Core bug fixes (RLM framework)
copy "C:\Users\esmae\Desktop\RLM\CODE\rlm\utils\parsing.py" .\rlm\utils\parsing.py
copy "C:\Users\esmae\Desktop\RLM\CODE\rlm\environments\local_repl.py" .\rlm\environments\local_repl.py

# New UI files
mkdir ui
copy "C:\Users\esmae\Desktop\RLM\CODE\ui\app.py" .\ui\app.py
copy "C:\Users\esmae\Desktop\RLM\CODE\ui\utils.py" .\ui\utils.py

# Updated dependencies (adds streamlit, pymupdf)
copy "C:\Users\esmae\Desktop\RLM\CODE\pyproject.toml" .\pyproject.toml

# Documentation and templates
copy "C:\Users\esmae\Desktop\RLM\CODE\README-new.md" .\README-new.md
copy "C:\Users\esmae\Desktop\RLM\CODE\.env.example" .\.env.example
```

### Step 4: Install Dependencies with UV

Since this project uses UV for dependency management:

```bash
# Sync dependencies (regenerates uv.lock with new packages)
uv sync

# Or if you don't have UV installed:
pip install uv
uv sync
```

### Step 5: Update .gitignore (if needed)

The original repo already has a `.gitignore`, but ensure these are included:

```bash
# Check if these are already in .gitignore, add if missing
echo ".env" >> .gitignore
echo "ui/logs/" >> .gitignore
```

### Step 6: Stage and Commit Your Changes

```bash
# Check what files changed
git status

# Stage all changes
git add .

# Commit with a descriptive message
git commit -m "feat: Add PDF Chatbot UI + fix RLM core bugs

New Features:
- Streamlit-based PDF Q&A interface (ui/app.py, ui/utils.py)
- Multi-backend support (OpenAI, Gemini, Ollama)
- Anti-hallucination mode with citation support
- RLM execution logging

Bug Fixes:
- Fix FINAL()/FINAL_VAR() parsing truncation (balanced parens)
- Fix globals()/locals() blocked in REPL sandbox
- Avoid custom_system_prompt replacing REPL instructions"
```

### Step 7: Push to Your Fork

```bash
git push origin main
```

### Step 8: (Optional) Keep Your Fork Updated

To sync with future updates from the original repo:

```bash
# Add the original repo as "upstream" (one-time setup)
git remote add upstream https://github.com/alexzhang13/rlm.git

# Fetch updates from original
git fetch upstream

# Merge upstream changes into your branch
git merge upstream/main

# Resolve any conflicts, then push
git push origin main
```

### Step 9: (Optional) Rename Your Fork

If you want to distinguish your version:

1. Go to your GitHub repo → **Settings** → **General**
2. Change the repository name (e.g., `rlm-pdf-chatbot`)
3. Update the clone URL if needed

---

## 📋 Summary of Changed Files

| File | Type | Description |
|------|------|-------------|
| `rlm/utils/parsing.py` | Bug Fix | Balanced parenthesis parsing for FINAL()/FINAL_VAR() |
| `rlm/environments/local_repl.py` | Bug Fix | Enabled globals()/locals() in REPL sandbox |
| `pyproject.toml` | Updated | Added streamlit, pymupdf dependencies |
| `ui/app.py` | New | Streamlit PDF chatbot interface |
| `ui/utils.py` | New | PDF extraction, RLM factory, text normalization |
| `README-new.md` | New | Documentation for all changes |
| `.env.example` | Template | API key template (safe to commit) |
| `.env` | Config | API keys (**DO NOT COMMIT**) |
