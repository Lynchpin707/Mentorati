from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

CHROMA_PATH = "database/spanish_grammar_db"

# Initialize local Llama 3.1 via Ollama
model = ChatOllama(model="llama3.1", temperature=0)

# Multilingual embeddings (must match ingest script)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

PROMPT_TEMPLATE = """
You are a helpful Spanish Grammar Tutor. Use the following pieces of context 
to answer the user's question about Spanish grammar. 

If the context doesn't contain the answer, tell the user you don't know, 
but offer to explain based on your general knowledge.

---
CONTEXT:
{context}
---
QUESTION:
{question}

ANSWER (in English, but provide Spanish examples):
"""

def query_buddy(query_text):
    # 1. Search the DB
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    results = db.similarity_search_with_relevance_scores(query_text, k=3)

    # 2. Prepare Context
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # 3. Generate Answer
    response = model.invoke(prompt)
    
    # 4. Return answer + Sources (for your XAI interest!)
    sources = [doc.metadata.get("source", "Unknown") for doc, _score in results]
    return response.content, sources