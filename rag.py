"""
rag.py
------
Handles retrieval from ChromaDB and calls the DeepInfra
Meta-Llama API to generate answers.
"""

import os
import time
import requests
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_DIR = "./chroma_store"
API_URL = "https://api.deepinfra.com/v1/openai/chat/completions"
MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"


def get_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)


def retrieve_chunks(query, k=5):
    """Fetch top-5 relevant chunks for the query (Part B1)."""
    store = get_vectorstore()
    results = store.similarity_search(query, k=k)
    return [doc.page_content for doc in results]


SYSTEM_PROMPT = """You are a Senior Upwork API Consultant with deep expertise in the Upwork developer platform.
Your job is to answer developer questions accurately using ONLY the documentation context provided below.
Read the entire context carefully before answering.
If the answer is not found in the provided context, you must respond with exactly:
"I'm sorry, but the provided documentation does not contain that information."
Do not guess, do not make up information. Stay professional and concise."""


def ask_llm(query, chunks, api_key):
    """Call DeepInfra Llama API with retrieved context (Part B2)."""
    context = "\n\n---\n\n".join(chunks)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Context from Upwork API documentation:\n\n{context}\n\nDeveloper question: {query}"
        }
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
    """Full RAG pipeline: retrieve → prompt → respond."""
    chunks = retrieve_chunks(user_query)
    answer, latency = ask_llm(user_query, chunks, api_key)
    return answer, chunks, latency

