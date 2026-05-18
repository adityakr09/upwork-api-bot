# Technical Summary — Upwork API Support Bot

## What I Built
A chatbot that answers questions about the Upwork API using RAG (Retrieval-Augmented Generation).
It reads the API documentation PDF, breaks it into small pieces, stores them in a vector database,
and uses Meta-Llama to generate answers based only on that documentation.

---

## Difficulties I Faced

**Reading the PDF:**
The text extracted from the PDF sometimes had spacing issues.
I added a sanity check to print the total characters and a sample so I could verify it was read correctly.


**Splitting the text:** 
When I split the text into 500-character chunks, some code examples like curl commands were getting cut in half. I added a 50-character overlap so the next chunk always has a bit of the previous one — this keeps code snippets intact.

**Stopping hallucinations:** 
The LLM would sometimes answer from its own training data even if the documentation didn't have the answer. I fixed this by writing a strict system prompt that tells the model to only use the provided context and say sorry if the answer isn't there.

**API response time:** 
The DeepInfra API sometimes took a few seconds to respond. I added a latency display in the UI so the user can see how long it took.

**First run download:** 
The embedding model downloads about 90MB on the first run. This is expected and only happens once.

---

## How I Used LLMs 

- I used Claude to help me write and improve the system prompt.
- I looked up the correct LangChain syntax for saving ChromaDB to disk.
- The overall structure, logic, and decisions are mine — I used Claude the same way
  I would use Stack Overflow, just to look things up faster.

---

## Reasons I Am a Good Fit for the ProAnalyst AI Team

1. **I have already built similar projects.** 
My MedAgent CRM project uses LangGraph, FastAPI, and PostgreSQL and is currently live and deployed. I know how these systems work in practice, not just in theory.

2. **I work on the full project, not just one part.** 
I built the backend, the database,the AI logic, and the frontend for my projects. I do not need someone else to connect the pieces.

3. **I pick up new tools quickly.** 
I had not used DeepInfra before this assignment. I read the documentation, understood how the API works, and integrated it correctly .I can do the same with any new tool the team uses.