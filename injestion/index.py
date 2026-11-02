from uuid import uuid4

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from config.logger import logger
from config.setting import setting


def _validate_chunks(chunks):
    if not isinstance(chunks, list) or not chunks:
        raise ValueError("Chunks must be a non-empty list")

    for chunk in chunks:
        if not isinstance(chunk, Document):
            raise TypeError("Every chunk must be a LangChain Document")
        if not isinstance(chunk.page_content, str) or not chunk.page_content.strip():
            raise ValueError("Every chunk must contain non-empty text")
        if not isinstance(chunk.metadata, dict) or not chunk.metadata.get("source"):
            raise ValueError("Every chunk must contain source metadata")


def chunks_embedding(chunks):
    _validate_chunks(chunks)

    try:
        model = HuggingFaceEmbeddings(
            model_name=setting.embedding_model,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": False},
        )
        vector = model.embed_query(chunks[0].page_content)
        vector_size = len(vector)
        if vector_size <= 0:
            raise ValueError("Empty embedding generated")
        logger.info(
            "Embedding model created successfully with dimension %s",
            vector_size,
        )
    except Exception:
        logger.exception("Embedding model creation failed")
        raise

    if not setting.qdrant_url:
        raise ValueError("Qdrant URL is missing")
    if not setting.qdrant_api_key:
        raise ValueError("Qdrant API key is missing")
    if not setting.qdrant_collection_name:
        raise ValueError("Qdrant collection name is missing")

    collection = setting.qdrant_collection_name
    try:
        client = QdrantClient(
            url=setting.qdrant_url,
            api_key=setting.qdrant_api_key,
        )
        existing_names = {
            item.name for item in client.get_collections().collections
        }
        logger.info("Qdrant client connected successfully")
    except Exception:
        logger.exception("Qdrant client connection failed")
        raise

    try:
        if collection in existing_names:
            logger.warning("Replacing existing Qdrant collection %s", collection)
            client.delete_collection(collection_name=collection)

        client.create_collection(
            collection_name=collection,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )

        collection_info = client.get_collection(collection_name=collection)
        configured_size = collection_info.config.params.vectors.size
        if configured_size != vector_size:
            raise RuntimeError(
                f"Qdrant vector size {configured_size} does not match "
                f"embedding size {vector_size}"
            )

        ids = [str(uuid4()) for _ in chunks]
        if len(ids) != len(set(ids)):
            raise RuntimeError("Generated document IDs are not unique")

        vector_store = QdrantVectorStore(
            client=client,
            collection_name=collection,
            embedding=model,
        )
        vector_store.add_documents(documents=chunks, ids=ids)

        indexed_count = client.count(
            collection_name=collection,
            exact=True,
        ).count
        if indexed_count != len(chunks):
            raise RuntimeError(
                f"Indexed {indexed_count} chunks but expected {len(chunks)}"
            )

        search_results = vector_store.similarity_search(
            query=chunks[0].page_content,
            k=1,
        )
        if not search_results:
            raise RuntimeError("Post-index retrieval verification returned no results")

        logger.info(
            "Collection %s indexed successfully with %s chunks",
            collection,
            indexed_count,
        )
        return {
            "collection": collection,
            "chunks_indexed": indexed_count,
            "embedding_dimension": vector_size,
        }
    except Exception:
        logger.exception("Collection indexing failed")
        raise



if __name__ == "__main__":
    docs = load_data()
    chunks = data_chunking(docs)
    chunks_embedding(chunks)
