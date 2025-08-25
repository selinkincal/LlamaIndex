import os
import qdrant_client
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex, StorageContext, SimpleDirectoryReader, Settings
from llama_index.embeddings.openai import OpenAIEmbedding


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY bulunamadı! .env dosyasını kontrol et.")
os.environ["OPENAI_API_KEY"] = api_key


class QdrantVS:
    def __init__(self, collection_id: str, config: dict):
        self.collection_id = collection_id
        self.config = config
        self.client = qdrant_client.QdrantClient(
            host=self.config.get("host", "localhost"),
            port=self.config.get("port", 6333)
        )

    def delete_collection(self) -> None:
        self.client.delete_collection(collection_name=self.collection_id)

    def get_vector_store(self) -> QdrantVectorStore:
        return QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_id
        )

    def create_index(self, nodes):
        vector_store = self.get_vector_store()
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        return VectorStoreIndex(nodes, storage_context=storage_context)
