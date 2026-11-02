from langchain_core.documents import Document
from config.logger import logger


def data_validation(text):
    if not isinstance(text, Document):
        raise TypeError("Loaded item is not a LangChain Document")

    content = text.page_content
    metadata = text.metadata
    source = (
        metadata.get("source", "<unknown source>")
        if isinstance(metadata, dict)
        else "<unknown source>"
    )

    if not isinstance(content, str) or not content.strip():
        raise ValueError(f"Content belonging to {source} is empty")
    if not isinstance(metadata, dict) or not metadata:
        raise ValueError(f"Metadata is empty for {source}")
    if not content.lstrip().startswith("Q:"):
        raise ValueError(f"Missing Q: section marker in {source}")


def chunks_validation(chunks):
    if not chunks:
        raise ValueError("No chunks were created")

    seen_content = set()
    unique_chunks = []
    for chunk in chunks:
        if not isinstance(chunk, Document):
            raise TypeError("Generated chunk is not a LangChain Document")

        content = chunk.page_content
        metadata = chunk.metadata

        if not isinstance(content,str) or not content.strip():
            raise ValueError("Generated chunk content is empty")

        if not content.strip().startswith("Q:"):
            raise ValueError("Generated chunk is missing the Q: prefix")

        if content in seen_content:
            logger.warning(f"Duplicate chunk dropped : {content}")
            continue
        seen_content.add(content)
        unique_chunks.append(chunk)

        source = (
            metadata.get("source", "<unknown source>")
            if isinstance(metadata, dict)
            else "<unknown source>"
        )
        if not isinstance(metadata, dict) or not metadata.get("source"):
            raise ValueError(f"Generated chunk has no source metadata: {source}")

        if len(content.strip()) < 200:
            logger.warning("%s chunk is under 200 characters", source)

    chunks[:] = unique_chunks
    if not chunks:
        raise ValueError("No unique chunks remain after duplicate removal")

    logger.info("Total %s chunks created", len(chunks))
    logger.info("Chunks Validation Successfully Completed")


def data_chunking(docs):
    try:
        if not docs:
            raise ValueError("Documents list is empty")
        if not isinstance(docs, list):
            raise TypeError("Documents input must be a list")

        chunks = []
        for text in docs:
            data_validation(text)

            sections = text.page_content.split("\nQ:")
            for section in sections:
                section = section.strip()
                if not section:
                    continue
                chunks.append(
                    Document(
                        page_content="Q: " + section,
                        metadata=dict(text.metadata),
                    )
                )
        chunks_validation(chunks)
        logger.info("Chunks created successfully")
        return chunks
    except Exception:
        logger.exception("Chunks creation failed")
        raise
        


if __name__ == "__main__":
    docs = load_data()
    data_chunking(docs)
