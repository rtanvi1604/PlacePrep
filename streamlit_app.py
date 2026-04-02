import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

#Page config
st.set_page_config(
    page_title="PlacePrep · AI Placement Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

#Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&display=swap');
@media (prefers-color-scheme: dark) {
    .user-bubble {
        background: #1e293b;
    }
}
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

:root {
    --bg-color: var(--background-color);
    --text-color: var(--text-color);
    --secondary-bg: var(--secondary-background-color);
}            

.main { background: var(--bg-color); color: var(--text-color); }
.block-container { padding: 2rem 2.5rem; max-width: 860px; }

/* Sidebar */
section[data-testid="stSidebar"] {background: var(--secondary-bg) !important;}
section[data-testid="stSidebar"] .stRadio label { color: rgba(255,255,255,0.7) !important; }

/* Chat bubbles */
.user-bubble {
    background: #0f1b2d; color: #ffffff;
    padding: 12px 18px; border-radius: 16px 16px 4px 16px;
    margin: 8px 0; max-width: 75%; margin-left: auto;
    font-size: 14px; line-height: 1.6;
}
.coach-bubble {
    background: var(--secondary-bg);
    color: var(--text-color);
    padding: 14px 18px; border-radius: 16px 16px 16px 4px;
    margin: 8px 0; max-width: 85%;
    border: 1px solid rgba(128,128,128,0.2);
    border-left: 3px solid #c9a96e;
    font-size: 14px; line-height: 1.7;
}
.coach-label {
    font-size: 11px; color: #c9a96e;
    font-weight: 500; letter-spacing: 0.08em;
    text-transform: uppercase; margin-bottom: 6px;
}
.welcome-box {
    background: var(--secondary-bg);
    color: var(--text-color); border-radius: 16px;
    padding: 28px 32px; border-left: 3px solid #c9a96e;
    border: 1px solid rgba(0,0,0,0.06); margin-bottom: 20px;
}
.stTextInput > div > input, 
.stTextArea textarea {
    background: var(--secondary-bg) !important;
    color: var(--text-color) !important;
    border: 1px solid rgba(128,128,128,0.3) !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stButton > button {
    background: #0f1b2d !important;
    color: #ffffff !important; border-radius: 10px !important; border: none !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.5rem 1.5rem !important;
}
.stButton > button:hover { background: #243d5c !important; }
</style>
""", unsafe_allow_html=True)

#Model setup
@st.cache_resource
def load_chain():
    model = OllamaLLM(model="llama3.2")
    template = """
You are an expert placement coach helping engineering students 
prepare for technical and HR interviews at top tech companies.

Here are some relevant placement Q&As from the knowledge base:
{context}

Now answer this question from the student:
{question}

Guidelines:
- Explain clearly with examples.
- For DSA/technical topics, walk through logic step by step.
- For resources/platforms, give specific actionable recommendations.
- End with 1 concrete follow-up tip the student can act on today.
Also suggest 2 follow-up questions an interviewer might ask.
"""
    prompt = ChatPromptTemplate.from_template(template)
    return prompt | model

chain = load_chain()

#Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "question_count" not in st.session_state:
    st.session_state.question_count = 0

#Sidebar
with st.sidebar:
    st.markdown("### 🎯 PlacePrep")
    st.markdown("*AI Placement Coach*")
    st.divider()

    mode = st.radio("Mode", [
        "💡 Guide Me",
        "📝 Evaluate My Answer",
        "🎤 Mock Interview"
    ])

    st.divider()
    st.markdown("**Filter by Topic**")
    topic = st.selectbox("", [
        "All Topics", "DSA", "ML / AI", "System Design",
        "Database & SQL", "OOP", "HR & Behavioral",
        "Python", "OS & Networks"
    ], label_visibility="collapsed")

    st.divider()
    col1, col2 = st.columns(2)
    col1.metric("Questions", st.session_state.question_count)
    col2.metric("Mode", mode.split()[1])

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.session_state.question_count = 0
        st.rerun()

#Main area
st.markdown("""
<div class="welcome-box">
  <h2 style="font-family:'DM Serif Display',serif;font-size:22px;margin-bottom:8px;">
    Good to see you, Tanvi 👋
  </h2>
  <p style="color: var(--text-color); opacity: 0.7;font-size:14px;margin:0;">
    Ask a concept question, get your answer evaluated, or try a mock interview. 
    Powered by your local RAG pipeline with placement Q&As.
  </p>
</div>
""", unsafe_allow_html=True)

#Quick prompts
st.markdown("**Quick asks:**")
qcols = st.columns(3)
quick = [
    "Top DSA topics for Google",
    "Explain time complexity",
    "Tell me about yourself",
    "Overfitting vs underfitting",
    "What is a REST API?",
    "SQL vs NoSQL"
]
for i, q in enumerate(quick):
    if qcols[i % 3].button(q, key=f"qp_{i}"):
        st.session_state.messages.append({"role": "user", "content": q})
        with st.spinner("Coach is thinking..."):
            docs = retriever.invoke(q)
            context = "\n\n".join([doc.page_content for doc in docs])
            answer = chain.invoke({"context": context, "question": q})
        st.session_state.messages.append({"role": "coach", "content": answer})
        st.session_state.question_count += 1
        st.rerun()

st.divider()

#Chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="coach-bubble">
          <div class="coach-label">placement coach</div>
          {msg["content"].replace(chr(10), "<br>")}
        </div>''', unsafe_allow_html=True)

#Input area
st.markdown("---")

if "Evaluate" in mode:
    user_answer = st.text_area("Your answer (for evaluation):", placeholder="Type your answer here...", height=80, key="eval_ans")
else:
    user_answer = ""

question_input = st.text_input(
    "Ask your question:",
    placeholder="Type a question and press Enter...",
    key="q_input"
)

if st.button("Ask Coach →") and question_input.strip():
    q = question_input.strip()

# Build prompt based on mode
    if "Evaluate" in mode and user_answer.strip():
        full_q = f"""Interview Question: {q}

Student's Answer: {user_answer}

Evaluate this answer:
1. Score out of 10 with reasoning
2. What was strong
3. What was missing
4. A better model answer
5. Two follow-up questions"""
    elif "Mock" in mode:
        full_q = f"Ask me ONE realistic {topic} interview question for a software engineering role. Just ask the question, don't answer it."
    else:
        full_q = q

    st.session_state.messages.append({"role": "user", "content": q})

    with st.spinner("Coach is thinking..."):
        docs = retriever.invoke(q)
        context = "\n\n".join([doc.page_content for doc in docs])
        answer = chain.invoke({"context": context, "question": full_q})

    st.session_state.messages.append({"role": "coach", "content": answer})
    st.session_state.question_count += 1
    st.rerun()