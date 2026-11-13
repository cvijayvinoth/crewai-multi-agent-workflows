# CrewAI Multi-Agent Workflows, Tools, Memory & RAG

A practical, runnable reference repository covering multi-agent orchestration patterns in **CrewAI**—built so anyone on the team can understand the architecture and run working examples in minutes.

---

## Core Concepts Covered

### 1. Multi-Step Workflows & Agent Collaboration
* **Sequential Pipelines:** Tasks execute linearly where downstream agents build on upstream results.
* **Explicit Context Passing (`context=[...]`):** Downstream tasks do not automatically see upstream outputs unless explicitly wired via the `context` parameter.
* **Role & Tool Separation:** Pairing a tool-equipped **Researcher** with a tool-free **Writer** prevents hallucination and enforces separation of concerns.

### 2. Process Types (`Process`)
| Process Type | How It Works | Best For |
| :--- | :--- | :--- |
| **`Process.sequential`** | Executes tasks strictly in list order (`Task 1 -> Task 2 -> Task 3`). | Predictable pipelines like research -> draft -> review. |
| **`Process.hierarchical`** | A `manager_llm` (or `manager_agent`) dynamically delegates tasks, reviews outputs, and requests revisions. | Complex projects needing managerial oversight and dynamic routing. |

### 3. Tools in CrewAI
* **Web Search Tools (`SerperDevTool`):** Connects agents to live Google search results for real-time facts.
* **File & Document Processing Tools (`FileReadTool`, `FileWriterTool`, `DirectoryReadTool`):** Lets agents inspect local files, parse logs/reports, and save deliverables to disk.
* **Custom Python Tools (`@tool` / `BaseTool`):** Wraps any Python function (APIs, calculators, database queries) with type hints and docstrings so the LLM knows when and how to invoke it.

### 4. Memory in CrewAI (Short-Term vs. Long-Term)
* **Short-Term Memory:** Tracks active context, intermediate tool outputs, and conversation state *within* a single `crew.kickoff()` execution.
* **Long-Term Memory:** Persists extracted facts, preferences, and insights *across separate runs* on disk so the crew improves over time.
* **Unified Memory (`memory=True`):** CrewAI's unified `Memory` engine automatically extracts, scores (recency + importance + relevance), and recalls prior context before each task.

### 5. Knowledge Sources & RAG
* **Knowledge Sources (`StringKnowledgeSource`, `TextFileKnowledgeSource`, PDF/CSV/JSON):** Pre-loads domain documents into vector storage (ChromaDB) so agents retrieve relevant chunks at runtime via automatic query rewriting.
* **Memory vs. Knowledge:** **Knowledge** is static reference material you provide upfront (company style guides, SOPs); **Memory** is dynamic experience the crew accumulates while working.

---

## Quickstart Setup

1. **Clone & enter the repo**
   ```bash
   git clone https://github.com/<your-username>/crewai-multi-agent-workflows.git
   cd crewai-multi-agent-workflows
   ```

2. **Create a virtual environment & install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Fill in your keys inside `.env`:
   ```env
   OPENAI_API_KEY=your_openai_key
   MODEL=openai/gpt-4o-mini
   SERPER_API_KEY=your_serper_key
   ```

4. **Run any example**
   ```bash
   python examples/01_sequential_newsletter.py
   python examples/02_hierarchical_process.py
   python examples/03_custom_and_file_tools.py
   python examples/04_memory_and_rag_knowledge.py
   ```
