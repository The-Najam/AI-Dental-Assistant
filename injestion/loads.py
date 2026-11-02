from langchain_community.document_loaders import TextLoader, DirectoryLoader
from pathlib import Path
from config.setting import setting
from config.logger import logger
from langchain_core.documents import Document

# Validating Documents
def docs_validation_check(document):

    if not document:
        raise ValueError("No documents were loaded")

    for docs in document:
        if not isinstance(docs, Document):
            raise TypeError("Loaded item is not a LangChain Document")

        content = docs.page_content
        metadata = docs.metadata

        if not metadata:
            raise ValueError("Document metadata is empty")

        source = metadata.get("source", "<unknown source>")

        if not isinstance(content, str) or not content.strip():
            raise ValueError(f"Page content is empty for {source}")

# Loading Documents
def load_data():
    file_path = Path(setting.file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Knowledge-base path does not exist: {file_path}")
    if not file_path.is_dir():
        raise NotADirectoryError(f"Knowledge-base path is not a directory: {file_path}")

    expected_files = list(file_path.glob("*.txt"))

    try:
        loader = DirectoryLoader(
            path=file_path,
            glob="*.txt",
            loader_cls=lambda path: TextLoader(path, encoding="utf-8"),
        )
        docs = loader.load()
        if len(docs) != len(expected_files):
            raise ValueError(
                f"Loaded {len(docs)} documents but found {len(expected_files)} text files"
            )
        
        docs_validation_check(docs) # call validation function

        logger.info("All %s documents loaded and validated successfully", len(docs))
        return docs
    except Exception:
        logger.exception("Failed to load and validate documents")
        raise


if __name__ == "__main__":
    load_data()
            
