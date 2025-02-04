import os

from dotenv import load_dotenv

load_dotenv()

KNOWLEDGE_BASE_PATH = os.getenv("KNOWLEDGE_BASE_PATH")
CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME")
CHROMA_HOST = os.getenv("CHROMA_HOST")
CHROMA_PORT = os.getenv("CHROMA_PORT")
FASTAPI_HOST = os.getenv("FASTAPI_HOST")
FASTAPI_PORT = os.getenv("FASTAPI_PORT")
