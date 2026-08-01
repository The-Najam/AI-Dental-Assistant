# importing Libraries
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
import glob
from pathlib import Path
from config.setting import setting
from uuid import uuid4
from config.logger import logger


# Loading the data
def load_data():
    file_path = Path(setting.file_path)
    try:
        # Loading the data
        loader = DirectoryLoader(
            path = file_path,
            glob="*.txt",
            loader_cls=lambda path: TextLoader(path, encoding="utf-8")
        )
        docs = loader.load()
        logger.info("Data Loaded Sucessfully !")
    except Exception as e:
        logger.error("Data Loading Failed !") 

    return docs

        
# Splitting the text

def data_chunking(docs):
    try:
        # Splitting the chunks based on Headers
        chunks = []
        for text in docs:
            splits = text.page_content.split("\nQ:")
            for split in splits:
                if split.strip():
                    chunks.append(Document(page_content="Q: " + split.strip()))
        
        logger.info("Chunks Created sucessfully!")
    except Exception as e:
        logger.critical("Chunking Falied !")

    return chunks


# EMbedding and Storing the chunks

def chunk_embedding(chunks):
    try:
        # model creation using Hugging Face
        model_kwargs = {"device": "cpu"}
        encode_kwargs = {"normalize_embeddings": False}
        model = HuggingFaceEmbeddings(
        model_name=setting.embedding_model,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
        )
        logger.info("Model Is Created")
    except Exception as e:
        logger.error("Model Creation Failed")
    try:
        # creating Qdrant Client
        client = QdrantClient(url=setting.qdrant_url, api_key=setting.qdrant_api_key)
        collection = setting.qdrant_collection_name
        collection_response = client.get_collections()
        existing_name = [c.name for c in collection_response.collections]
        logger.info("Client Created Sucessfully")
    except Exception as e:
        logger.critical("Client Creation Failed")

    

    try:
        if collection in existing_name:
            print(existing_name)
            logger.info("Collection Already Exist! %s")
            client.delete_collection(collection_name=setting.qdrant_collection_name)
        # creating collection
        client.create_collection(
            collection_name = setting.qdrant_collection_name,
            vectors_config = VectorParams(size=384, distance=Distance.COSINE),
            )
        # Storing the chunks
        vector_store = QdrantVectorStore(
            client = client,
            collection_name = setting.qdrant_collection_name,
            embedding = model
        )

        # upserting the chunks in vector db
        ids = [str(uuid4()) for _ in range(len(chunks))]
        vector_store.add_documents(documents=chunks, ids=ids)
        logger.info("Collection Created Successfully! %s")
    except Exception as e:
        logger.critical("Collection Creation Failed ! %s", e)
    


if __name__ == "__main__":
    docs = load_data()
    chunks = data_chunking(docs)
    chunk_embedding(chunks)
