from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from config.setting import setting
from config.logger import logger
from langchain_huggingface import HuggingFaceEmbeddings

try:
    model_kwargs = {"device": "cpu"}
    encode_kwargs = {"normalize_embeddings": False}
    model = HuggingFaceEmbeddings(
        model_name = setting.embedding_model,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs     
    )
    client = QdrantClient(url= setting.qdrant_url, api_key=setting.qdrant_api_key)
    logger.info("Model and Client Successfully Created!")
except Exception as e:
    logger.info("Model and Client Creation Failed at Retrieval Stage %s", e)



def retrieve_chunks(query):
    
    collection_name = setting.qdrant_collection_name

    try:
        vector_store = QdrantVectorStore(
            client = client,
            collection_name = collection_name,
            embedding = model
        )
        results = vector_store.similarity_search_with_score(
            query = query,
            k=setting.top_k
        )
        logger.info("Chunks Retrieved Successfully")
        print(results)
        return results
    except Exception as e:
        logger.info("Chunks Retrieval Failed! %s", e)




if __name__ == "__main__":


    retrieve_chunks(query)