from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from config.setting import setting
from config.logger import logger
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

try:
    model = HuggingFaceEmbeddings(
        model_name = setting.embedding_model,
        model_kwargs= {"device": "cpu"},
        encode_kwargs= {"normalize_embeddings": False}
    )
    vector = model.embed_query("Test Sentence")

    if not vector:
        raise RuntimeError("Embedding Model Creation Failed!")
    vector_size = len(vector)
    if vector_size <= 0:
        raise ValueError("Empty embedding generated")
    logger.info(
        "Embedding model created successfully with dimension %s",
        vector_size,
    )

    if not setting.qdrant_api_key:
        raise ValueError("Qdrant API key is Missing")

    if not setting.qdrant_url:
        raise ValueError("Qdrant Url Configuration Missing!")
    
    client = QdrantClient(url= setting.qdrant_url, api_key=setting.qdrant_api_key)
    logger.info("Model and Client Successfully Created!")
except Exception as e:
    raise RuntimeError(
        f"Model and client creation failed at retrieval stage: {e}"
    ) from e



def retrieval_result_validation(results):
    if not isinstance(results,list) or not results:
        raise ValueError("Retrieval chunks are empty or have an invalid type")

    for result in results:
        if (
            not isinstance(result, tuple)
            or len(result) != 2
            or not result
        ):
            raise TypeError(
                f"Retrieved chunk has an invalid type or is empty: {result}"
            )

        document, similarity_score = result
        if not isinstance(document, Document):
            raise TypeError(
                f"Retrieved item is not a Document: {document}"
            )

        content = document.page_content
        metadata = document.metadata

        if not isinstance(content, str):
            raise TypeError(
                "Retrieved document content must be a string"
            )
        if not content.strip():
            raise ValueError("Retrieved document content cannot be empty")
        if not isinstance(similarity_score, float):
            raise TypeError(
                "Similarity score must be a float"
            )


def retrieve_chunks(query):
    try:
        collection_name = setting.qdrant_collection_name

        if not isinstance(query, str):
            raise TypeError("Query must be a string")
        if not query.strip():
            raise ValueError("Query cannot be empty")

        if not isinstance(setting.top_k, int):
            raise TypeError("Top K must be an integer")
        if setting.top_k < 1:
            raise ValueError("Top K must be at least 1")

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
        retrieval_result_validation(results)
        return results
    except Exception as e:
        raise RuntimeError(f"Chunks retrieval failed: {e}") from e




if __name__ == "__main__":

    query = "What dental services you're offering?"
    retrieve_chunks(query)