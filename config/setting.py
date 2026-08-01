from pathlib import Path
from typing import ClassVar
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    gemini_api_key : str
    embedding_model : str = "all-MiniLM-L6-v2"
    gemini_model : str = "models/gemini-3.6-flash"
    top_k : int = 5
    knowledge_base_path : ClassVar[Path] = Path(__file__).parent.parent / "data"
    file_path : ClassVar[Path] = Path(__file__).parent.parent / "data"
    database_path: ClassVar[Path] = Path(__file__).parent.parent / "data/demo.db"
    qdrant_url: str
    qdrant_collection_name: str 
    qdrant_api_key : str
    client_email: str = Field(..., env="CLIENT_EMAIL")
    resend_api_key : str= Field(..., env="RESEND_API_KEY")



    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding= "utf-8"
    )


setting = Settings()





