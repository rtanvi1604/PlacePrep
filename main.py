from sqlalchemy import JSON

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="llama3.2")

template = """
You are an expert placement coach helping engineering students 
prepare for technical and HR interviews at top tech companies.

Here are some relevant placement Q&As from our knowledge base 
to help you answer accurately:
{context}

Now answer this question from the student:
{question}

Your tasks:
1. Give a better model answer the candidate can learn from.
2. Suggest 2 follow-up questions an interviewer might ask next.

Guidelines:
- If the question is about interview topics, explain clearly with examples.
- If it's a DSA/technical topic, walk through the logic step by step.
- If the question is about resources/platforms, give specific recommendations and actionable advice.
- Always end with 1 follow-up tip the student can act on today.
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

print("🎯 Placement Guide AI Agent")
print("Ask me anything about placements, interviews, or tech concepts!")
print("Type 'q' to quit\n")

while True:
    question = input("Ask your question (q to quit): ")
    if question.lower() == "q":
        break

    relevant_docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    result = chain.invoke({
    "context": context,
    "question": question})

    print(f"\n 👩‍💼 Coach: {result} \n")
    print("_" * 60)