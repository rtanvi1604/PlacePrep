# 🎯 PlacePrep – AI Placement Coach

PlacePrep is an AI-powered placement preparation assistant designed to help engineering students crack technical and HR interviews.

It uses a **Retrieval-Augmented Generation (RAG)** pipeline with a vector database and LLM to provide accurate, context-aware answers from a curated dataset of placement questions.

---

## 🚀 Features

- 💡 **Guide Me Mode** – Get structured answers for DSA, ML, OS, and HR questions  
- 📝 **Evaluate My Answer** – Get score, feedback, and model answers  
- 🎤 **Mock Interview Mode** – Practice real interview questions  
- 🔍 **RAG Pipeline** – Retrieves relevant Q&A from dataset using Chroma DB  
- ⚡ **Fast Local LLM (Ollama)** integration  
- 🎨 Clean and responsive Streamlit UI  

---

## 🧠 Tech Stack

- **Frontend:** Streamlit  
- **LLM:** Ollama (LLaMA 3.2)  
- **Embeddings:** mxbai-embed-large  
- **Vector DB:** ChromaDB  
- **Backend:** LangChain  

---

## 📁 Project Structure

```
PlacePrep
├── streamlit_app.py          # UI and app logic
├── main.py                   # CLI version
├── vector.py                 # RAG pipeline + embeddings
├── dataset.csv
├── Software_Questions.csv
├── requirements.txt
└── chroma_langchain_db/      # vector database
```

---

## ⚙️ Setup Instructions

1️⃣. **Clone the repository**
```bash
git clone https://github.com/your-username/placeprep-ai.git
cd placeprep-ai

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

2️⃣. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

3️⃣. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4️⃣. **Install & Run Ollama**
```bash
ollama run llama3.2
```

5️⃣. **Run the app**
```bash
streamlit run streamlit_app.py
```

### Example Queries
- **Explain time complexity with examples**
-  **Tell me about yourself**
-  **Overfitting vs underfitting**

---

## Demo Snaps

---

### 👩‍💻 Author
- **Tanvi R**
- **B.Tech AI & DS | Aspiring Data Scientist**
