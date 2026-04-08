# Project Omoikane: The Narrative Truth Engine

**Omoikane** is an Agentic RAG (Retrieval-Augmented Generation) system designed to ensure narrative integrity and eliminate AI hallucinations in complex, high-density fictional universes. Built with a "Security-First" and "Fact-First" mindset, it acts as a synthetic archivist capable of auditing creative drafts against canonical lore in real-time.

##  Key Features

* **Agentic RAG Architecture**: Utilizes a `RouterQueryEngine` to dynamically navigate between disparate lore vaults (e.g., Marathon, Cyberpunk) based on semantic intent.
* **The "Dumbass Trigger"**: A pre-inference validation layer that identifies and rejects statistically impossible or logically inconsistent combat matchups before they consume compute resources.
* **Persistent Memory Vault**: Powered by a local **Qdrant** vector database to ensure zero-latency retrieval and 100% data persistence across sessions.
* **Multi-Interface Access**: Accessible via a high-performance **FastAPI** backend and a collaborative **Discord** bot interface.

##  Technical Stack

* **Brain**: Ollama (Llama 3)
* **Orchestration**: LlamaIndex
* **Vector Database**: Qdrant
* **API Framework**: FastAPI
* **Environment Management**: python-dotenv

##  Project Structure

* `main.py`: The core FastAPI application handling RAG routing and validation logic.
* `discord_bot.py`: The frontend interface for collaborative narrative auditing.
* `data/`: Persistent storage for canonical lore across multiple IPs.
* `demo/`: Preloaded "Truth Samples" for rapid system demonstration.

##  Quick Start

1. **Clone the repository.**
2. **Install dependencies**: `pip install -r requirements.txt`.
3. **Set up environment**: Copy `.env.example` to `.env` and add your `DISCORD_TOKEN`.
4. **Launch the engine**: 
   * Start API: `uvicorn main:app --reload`
   * Start Bot: `python discord_bot.py`

---
*Developed as a proof-of-concept for high-accuracy fact extraction and real-time AI-enabled collaborative interfaces.*

*This product is licensed under the MIT License - see the LICENSE  file for details.*
