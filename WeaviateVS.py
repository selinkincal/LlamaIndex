from typing import Sequence
from llama_index.core import BaseNode, VectorStoreIndex, StorageContext
from llama_index.core.vector_stores.types import MetadataFilter, MetadataFilters
from helpers.database_helpers import delete_data_source
from vector_protocol import VectorStoreProtocol

# Weaviate SDK
import weaviate
from llama_index.vector_stores.weaviate import WeaviateVectorStore
import os
from dotenv import load_dotenv

load_dotenv()

WEAVIATE_CONFIG = {
    "url": os.getenv("WEAVIATE_URL"),
    "api_key": os.getenv("WEAVIATE_API_KEY")
}


class WeaviateVS(VectorStoreProtocol):
    def __init__(self, collection_id: str, config: dict, embedded_dim: int = 1536):
       
        self.collection_id = collection_id
        self.config = config
        self.embedded_dim = embedded_dim

        # Weaviate client
        client_config = {"url": self.config["url"]}
        if "api_key" in self.config:
            client_config["auth_client_secret"] = weaviate.auth.AuthApiKey(api_key=self.config["api_key"])
        self.client = weaviate.Client(**client_config)

        # Koleksiyon (class) yoksa oluştur
        if not self.client.schema.contains({"class": self.collection_id}):
            class_obj = {
                "class": self.collection_id,
                "vectorizer": "none",  # LlamaIndex kullanacağı embedding
                "properties": [
                    {"name": "content", "dataType": ["text"]},
                    {"name": "data_source_id", "dataType": ["string"]},
                ],
            }
            self.client.schema.create_class(class_obj)

    def delete_collection(self) -> None:
        """Koleksiyonu Weaviate’den siler."""
        self.client.schema.delete_class(self.collection_id)

    def get_vector_store(self) -> WeaviateVectorStore:
        """Vector store instance döner."""
        return WeaviateVectorStore(
            weaviate_client=self.client,
            index_name=self.collection_id
        )

    def delete_data_source(self, data_source_id: str) -> None:
        """Belirli bir datasource’u koleksiyondan siler."""
        filters = [MetadataFilter(key="data_source_id", value=data_source_id)]
        vector_store = self.get_vector_store()
        vector_store.delete_nodes(filters=MetadataFilters(filters=filters))

        # Veritabanındaki datasource kaydını sil
        delete_data_source(data_source_id)
