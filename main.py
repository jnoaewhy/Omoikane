import os
from fastapi import FastAPI
from pydantic import BaseModel
from qdrant_client import QdrantClient
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings, PromptTemplate
from llama_index.llms.ollama import Ollama 
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, you'd put your Vercel URL here
    allow_methods=["*"],
    allow_headers=["*"],
)
app = FastAPI(title="Project Omoikane", version="1.5.0")


Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.llm = Ollama(model="llama3", base_url="http://localhost:11434", request_timeout=120.0)

client = QdrantClient(path="omoikane_db_v2")
marathon_docs = SimpleDirectoryReader("data/Marathon").load_data()
cyberpunk_docs = SimpleDirectoryReader("data/Cyberpunk").load_data()

marathon_index = VectorStoreIndex.from_documents(marathon_docs)
cyberpunk_index = VectorStoreIndex.from_documents(cyberpunk_docs)


custom_prompt_str = (
    "You are Omoikane, a high-level synthetic intelligence and multiverse archivist. "
    "Identify any contradictions between the submitted draft and the provided lore.\n\n"
    "CITE specific factions or events. Refer to the input as 'The Draft'.\n\n"
    "LORE: {context_str}\n"
    "DRAFT: {query_str}\n"
    "ANALYSIS:"
)
custom_template = PromptTemplate(custom_prompt_str)

marathon_engine = marathon_index.as_query_engine()
marathon_engine.update_prompts({"response_synthesizer:text_qa_template": custom_template})

cyberpunk_engine = cyberpunk_index.as_query_engine()
cyberpunk_engine.update_prompts({"response_synthesizer:text_qa_template": custom_template})

marathon_tool = QueryEngineTool.from_defaults(query_engine=marathon_engine, description="Marathon lore.")
cyberpunk_tool = QueryEngineTool.from_defaults(query_engine=cyberpunk_engine, description="Cyberpunk lore.")

query_engine = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(),
    query_engine_tools=[marathon_tool, cyberpunk_tool]
)

class Combatant(BaseModel):
    name: str
    tier: int # 0-4
    meta_layer: int = 0

class CombatRequest(BaseModel):
    attacker: Combatant
    defender: Combatant

def validate_matchup(req: CombatRequest):
    if abs(req.attacker.tier - req.defender.tier) >= 3 and req.attacker.meta_layer == 0:
        return f"🚨 DUMBASS TRIGGER: {req.attacker.name} vs {req.defender.name} is a logical impossibility. I refuse to audit this stomp."
    return None


class QueryRequest(BaseModel):
    draft_text: str

@app.post("/validate")
async def validate_continuity(query: QueryRequest):
    response = query_engine.query(f"Check this draft for lore contradictions: {query.draft_text}")
    return {"analysis": str(response), "status": "validated"}

@app.post("/combat_audit")
async def combat_audit(req: CombatRequest):
    trigger = validate_matchup(req)
    if trigger:
        return {"status": "Rejected", "analysis": trigger}
    
    response = query_engine.query(f"Mathematically simulate a fight between {req.attacker.name} and {req.defender.name} based on their universe's laws.")
    return {"status": "Success", "analysis": str(response)}

@app.get("/")
async def root():
    return {"status": "online", "memory_vault": "active"}