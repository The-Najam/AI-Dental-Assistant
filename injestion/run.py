
from config.logger import logger
from injestion.loads import load_data
from injestion.parse import data_chunking
from injestion.index import chunks_embedding


def run_injestion():
    try:
        docs = load_data()
        chunks = data_chunking(docs)
        result = chunks_embedding(chunks)
        logger.info("Ingestion pipeline completed successfully")
        return result
    except Exception:
        logger.exception("Ingestion pipeline failed")
        raise



if __name__ == "__main__":
    run_injestion()