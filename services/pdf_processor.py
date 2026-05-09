from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

name = 'mbochi-francais-dict'

def prepare_pdf(file_path):
    #Load document with data parsed as individual elements
    loader = UnstructuredPDFLoader(file_path, 
            mode = 'elements',
            languages = ['fra'])
    docs = loader.load()

    #Split the loaded PDF into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000,
        chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)

    # Clean metadata - remove complex objects Pinecone can't store
    for chunk in chunks:
        chunk.metadata = {k: v for k, v in chunk.metadata.items()
                     if isinstance(v, (str, int, float, bool, list))}

    #Generate embeddings for the chunks using OpenAI's embedding model
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPEN_AI_KEY'],
        model='text-embedding-3-large')
    
    #Store the chunks and their embedding in Pine vector database
    db_pine = PineconeVectorStore.from_documents(chunks, embeddings, index_name=name)

    #Return the vector database
    return db_pine 
