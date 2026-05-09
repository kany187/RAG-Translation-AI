RAG Translator AI is an intelligent Mbochi-French translation API powered by Retrieval-Augmented Generation (RAG).

It combines a vector database (Pinecone) with OpenAI's language models to provide accurate translations from a Mbochi-French dictionary. Unlike a simple lookup tool, it understands natural language questions and retrieves the most relevant dictionary content to generate clear, concise answers.

Key features:

Conversational API — users can ask multiple questions in a session with memory
Intelligent routing — filters off-topic questions automatically
RAG pipeline — retrieves relevant dictionary chunks before generating answers
Answer refinement — improves responses for clarity and conciseness
Tech stack:

FastAPI — REST API
LangGraph — conversational agent with stateful workflow
LangChain — document loading, chunking, embeddings
Pinecone — vector database for dictionary storage
OpenAI — embeddings (text-embedding-3-large) and LLM (gpt-4o)
Unstructured — PDF parsing with French language support
Use case: Preserving and making accessible the Mbochi language — a minority language from the Republic of Congo — by providing an AI-powered translation assistant grounded in an authoritative dictionar
