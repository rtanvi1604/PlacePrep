from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
import os
import pandas as pd

df1 = pd.read_csv("dataset.csv", encoding='latin-1')
df2 = pd.read_csv("Software_Questions.csv", encoding='latin-1')

embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = "./chroma_langchain_db"
add_documents = not os.path.exists(db_location)

vector_store = Chroma(
    collection_name="placement_questions",
    embedding_function=embeddings,
    persist_directory=db_location
)

def truncate(text, max_chars=1000):      # ✅ prevents context overflow
    return str(text)[:max_chars] if pd.notna(text) else ""

if add_documents:
    documents = []

    for i, row in df1.iterrows():
        documents.append(Document(
            page_content=f"Q: {truncate(row['question'])}\nA: {truncate(row['answer'])}",
            metadata={"source": "dataset.csv"},
            id=str(i)
        ))

    offset = len(df1)
    for i, row in df2.iterrows():
        documents.append(Document(
            page_content=f"Q: {truncate(row['Question'])}\nA: {truncate(row['Answer'])}\nCategory: {row['Category']} | {row['Difficulty']}",
            metadata={"source": "Software_Questions.csv", "category": row['Category']},
            id=str(i + offset)
        ))

    vector_store.add_documents(documents)
    print(f"✅ Embedded {len(documents)} documents into vector store")

retriever = vector_store.as_retriever(search_kwargs={"k": 5})