from typing import Sequence
from llama_index.core import BaseNode, VectorStoreIndex, StorageContext
from llama_index.core.vector_stores.types import MetadataFilter, MetadataFilters
from helpers.database_helpers import delete_data_source
from vector_protocol import VectorStoreProtocol

import os
from dotenv import load_dotenv
import pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore

load_dotenv()

pinecone_config = {
    "api_key": os.getenv("PINECONE_API_KEY"),
    "environment": os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
}

class PineconeVS(VectorStoreProtocol):
    def __init__(self, collection_id: str, config: dict = pinecone_config, embedded_dim: int = 1536):
        self.collection_id = collection_id
        self.config = config
        self.embedded_dim = embedded_dim

        # Pinecone initialize
        pinecone.init(
            api_key=self.config["api_key"],
            environment=self.config.get("environment", "us-east-1")
        )
        self.client = pinecone

    def delete_collection(self) -> None:
        
        if self.collection_id in self.client.list_indexes():
            self.client.delete_index(self.collection_id)

    def get_vector_store(self) -> PineconeVectorStore:
       
        # Index yoksa oluştur
        if self.collection_id not in self.client.list_indexes():
            self.client.create_index(self.collection_id, dimension=self.embedded_dim)

        index = self.client.Index(self.collection_id)
        return PineconeVectorStore(pinecone_index=index)

    def delete_data_source(self, data_source_id: str) -> None:
        
        filters = [MetadataFilter(key="data_source_id", value=data_source_id)]
        vector_store = self.get_vector_store()
        vector_store.delete_nodes(filters=MetadataFilters(filters=filters))

        delete_data_source(data_source_id)

