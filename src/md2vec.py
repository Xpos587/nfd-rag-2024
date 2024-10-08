import re
from typing import Dict, List

from sentence_transformer import SentenceTransformer


def preprocess_markdown(markdown_content: str) -> str:
    clean_content = markdown_content.lower()
    clean_content = re.sub(r"<!--.*?-->", "", clean_content, flags=re.DOTALL)
    clean_content = re.sub(r"[^\w\s.,;:?!-]", " ", clean_content)
    clean_content = re.sub(r"\s+", " ", clean_content).strip()
    return clean_content


def split_into_chunks(
    clean_content: str, chunk_size: int = 500
) -> List[Dict[str, str]]:
    sentences = re.split(r"(?<=[.!?])\s+", clean_content)
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        if current_length + len(sentence) > chunk_size and current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append(
                {
                    "text": chunk_text,
                    "start_index": clean_content.index(chunk_text),
                    "end_index": clean_content.index(chunk_text)
                    + len(chunk_text),
                }
            )
            current_chunk = []
            current_length = 0
        current_chunk.append(sentence)
        current_length += len(sentence)

    if current_chunk:
        chunk_text = " ".join(current_chunk)
        chunks.append(
            {
                "text": chunk_text,
                "start_index": clean_content.index(chunk_text),
                "end_index": clean_content.index(chunk_text) + len(chunk_text),
            }
        )

    return chunks


def create_embeddings(
    chunks: List[Dict[str, str]],
    model_name: str = "cointegrated/LaBSE-en-ru",
    batch_size: int = 8,
) -> List[List[float]]:
    model = SentenceTransformer(model_name)

    embeddings = []

    for start in range(0, len(chunks), batch_size):
        end = start + batch_size
        batch_chunks = [chunk["text"] for chunk in chunks[start:end]]
        batch_embeddings = model.encode(
            batch_chunks, batch_size=batch_size, show_progress_bar=True
        )
        embeddings.extend(batch_embeddings)

    return embeddings
