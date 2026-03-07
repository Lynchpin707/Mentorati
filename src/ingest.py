import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# 1. Configuration
DATA_PATH = "data/raw"
CHROMA_PATH = "database/spanish_grammar_db"

# Use a multilingual model so your English queries can find Spanish rules
# This runs locally on your M1 CPU/GPU
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

def build_vector_db():
    # LOAD: Get all text files from your raw data folder
    loader = DirectoryLoader(DATA_PATH, glob="*.txt", loader_cls=TextLoader)
    documents = loader.load()
    
    # TRANSFORM: Split text into meaningful chunks
    # We use a 1000-char window with 10% overlap to keep context intact
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Split {len(documents)} docs into {len(chunks)} chunks.")

    # STORE: Create or Update the persistent ChromaDB
    db = Chroma.from_documents(
        chunks, 
        embedding_model, 
        persist_directory=CHROMA_PATH
    )
    print(f"🚀 Saved {len(chunks)} chunks to {CHROMA_PATH}")

if __name__ == "__main__":
    build_vector_db()