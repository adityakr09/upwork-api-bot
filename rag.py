"""
rag.py
------
Handles retrieval from ChromaDB and calls the DeepInfra
Meta-Llama API to generate answers.
"""

import time
import requests
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_DIR = "./chroma_store"
API_URL = "https://api.deepinfra.com/v1/openai/chat/completions"
MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"

EXTRA_CONTEXT = """
Client Credentials Grant is available for enterprise accounts only.
It is designed for server-to-server scenarios only.
It must NOT be used to access a specific user's private data such as private contract details.
To access private contract details, Authorization Code Grant with user consent is required.
OAuth access token TTL is 24 hours (86400 seconds).
Refresh token TTL is 2 weeks since its last usage.
"""

def get_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)

def retrieve_chunks(query, k=5):
    store = get_vectorstore()
    results = store.similarity_search(query, k=k)
    seen = set()
    unique = []
    for doc in results:
        if doc.page_content not in seen:
            seen.add(doc.page_content)
            unique.append(doc.page_content)
    return unique

SYSTEM_PROMPT = """You are a Senior Upwork API Consultant.
Answer the developer's question using ONLY the context provided below.
If the answer is not found in the provided context, respond with exactly:
"I'm sorry, but the provided documentation does not contain that information."
Do not guess. Be concise and direct."""

def ask_llm(query, chunks, api_key):
    context = EXTRA_CONTEXT + "\n\n---\n\n" + "\n\n---\n\n".join(chunks)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context from Upwork API documentation:\n\n{context}\n\nDeveloper question: {query}"}
    ]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": 512,
        "temperature": 0.1
    }
    start = time.time()
    response = requests.post(API_URL, headers=headers, json=payload)
    latency = round(time.time() - start, 2)
    response.raise_for_status()
    answer = response.json()["choices"][0]["message"]["content"]
    return answer, latency

def query_rag(user_query, api_key):
    chunks = retrieve_chunks(user_query)
    answer, latency = ask_llm(user_query, chunks, api_key)
    return answer, chunks, latency