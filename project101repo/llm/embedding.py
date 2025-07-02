import pandas as pd
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Vector embedding and vector store using Hugging Face 
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import os

from langchain_huggingface import HuggingFaceEmbeddings

# File paths (as provided)
csv_files = [
    r"C:\Users\shrey\OneDrive\Desktop\Projects\Marketing MLOps\project101repo\data\raw\mlops_sample - fabdata.csv",
    r"C:\Users\shrey\OneDrive\Desktop\Projects\Marketing MLOps\project101repo\data\raw\mlops_sample - trends.csv"
]

# Step 1: Read and convert rows to Documents
doc = []
for file_path in csv_files:
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        doc.append(Document(page_content=str(row.to_dict())))

# Step 2: Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

docs = text_splitter.split_documents(doc)

# Step 3: Preview (first 2 chunks)
for d in docs[:2]:
    print(d.page_content)

#embedding
# 1. Setup Hugging Face embedding model
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"}  # Use 'cuda' if you have a GPU
)

# 2. Create FAISS vector store
print(f"\nCreating FAISS vector store with {len(docs)} documents...")
db = FAISS.from_documents(docs, embedding)

# 3. Persist FAISS index locally
db.save_local("faiss_index")
print(" Vector database saved to 'faiss_index'")

# 4. Test similarity search
print("\nTesting similarity search...")
results = db.similarity_search("What are the latest marketing trends?", k=2)
for i, doc in enumerate(results, 1):
    print(f"\nResult {i}:\n{doc.page_content}")