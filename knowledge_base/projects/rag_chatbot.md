## RAG-Based Chatbot Using LangChain, Qdrant & Hugging Face

### 🤖 Overview
This project is an advanced **RAG (Retrieval-Augmented Generation)** chatbot built using the **LangChain framework** — but with full control over custom components like vector storage and model selection. Instead of relying on built-in LangChain vector integrations, we implemented our own vector store using **Qdrant**, hosted via Docker containers. The chatbot is capable of understanding complex queries and generating context-aware responses by integrating multiple LLMs.

---

### 🛠️ Architecture & Components
- **LangChain**: Used for orchestrating the RAG pipeline — combining retrieval logic with generation modules.
- **Qdrant Vector DB**: Used as the core vector store. Hosted in a standalone **Docker container**, enabling flexibility and speed for vector search operations.
- **Embedding Model**: We used `sentence-transformers/all-mpnet-base-v2` from Hugging Face for converting text into 768-dimensional dense embeddings.
- **Similarity Metric**: Cosine similarity through Qdrant to match relevant chunks with the user query.
- **S3 Integration**: All textual documents were uploaded to an **AWS S3 bucket**, and automatically fetched by the LangChain retriever to generate embeddings and store them in Qdrant.

---

### 🧠 Language Models Used
The generation component of the RAG system leveraged multiple LLMs for robust and dynamic response generation:
- **Mistral 7B** (Hugging Face)
- **Claude (Anthropic)**
- **OpenAI GPT-3.5 Turbo (Paid API)**
- **OpenAI GPT-4 (Paid API)**

By integrating these diverse models, the chatbot could:
- Handle both long-form and precise answers
- Dynamically select model pipelines based on use case
- Deliver high-quality conversational outputs across various domains

---

### 🔄 Data Flow Summary
1. **Textual documents** → Uploaded to **S3 bucket**
2. **LangChain retriever** → Pulls and preprocesses text
3. **Embeddings** → Generated using `all-mpnet-base-v2`
4. **Qdrant** → Stores vectors and returns most relevant chunks via cosine similarity
5. **LLMs** → Use retrieved chunks to generate the final answer

---

### ✅ Summary
This RAG chatbot project demonstrates end-to-end mastery over retrieval pipelines, model integration, and real-time deployment. By bypassing LangChain's default vector tools and implementing **custom Qdrant integration**, the system achieves both scalability and control. The use of powerful LLMs such as GPT-4 and Mistral 7B further ensures the chatbot remains contextually aware and responsive to compl