# AI Research Agent (Ollama + Tavily + Custom AST Calculator)

An intelligent, autonomous AI Research Agent built in Python. The agent dynamically analyzes user intent to orchestrate local LLM inference (via Ollama), real-time web search (via Tavily API), and safe mathematical computation using Python's Abstract Syntax Tree (`ast`).

---

## 🌟 Key Features

- **Dynamic Tool Selection:** Uses an LLM-driven intent analyzer to dynamically decide whether to trigger Web Search, the Calculator, both tools, or answer directly without external tools.
- **Local Inference with Ollama:** Powered by `llama3.2` running locally via the Ollama application, eliminating LLM API costs and rate limits.
- **Safe Calculator Engine:** Uses AST parsing (`ast.parse`) instead of standard `eval()` to prevent code injection while gracefully handling invalid inputs and mathematical edge cases (e.g., division by zero).
- **Structured Report Synthesis:** Formats findings into standardized Markdown reports complete with executive summaries, cited source URLs, explicit labeling of hypothetical user figures, and limitations.

---

## 📁 Project Architecture & Flow

```text
               USER RESEARCH QUESTION
                         │
                         ▼
                  RESEARCH AGENT
                         │
                         ▼
                   LLM BRAIN
              (Analyze User Intent)
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
   [Needs Search?]             [Needs Calculation?]
        │  │                          │  │
       Yes No                        Yes No
        │  │                          │  │
        │  └──────────┐               │  └──────────┐
        ▼             │               ▼             │
   TAVILY SEARCH      │         AST CALCULATOR     │
       TOOL           │              TOOL           │
        │             │               │             │
        ▼             │               ▼             │
  Search Results      │        Calculated Output    │
        │             │               │             │
        └─────────────┼───────────────┴─────────────┘
                      │
                      ▼
            COMBINE EVIDENCE & STATE
                      │
                      ▼
             FINAL REPORT SYNTHESIS
                      │
                      ▼
            FINAL RESEARCH REPORT