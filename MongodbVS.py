from typing import Sequence
from vector_protocol import VectorStoreProtocol
from llama_index.core import BaseNode, VectorStoreIndex, StorageContext
from helpers.database_helpers import delete_data_source
from llama_index.vector_stores.mongodb import MongoVectorStore
import os
from dotenv import load_dotenv

load_dotenv()

mongo_config = {
    "uri": os.getenv("MONGO_URI"),
    "db_name": os.getenv("MONGO_DB_NAME", "llama_pdf_arsivi")
}

class MongoVS(VectorStoreProtocol):
    def __init__(self, collection_id: str, config: dict = mongo_config, embedded_dim: int = 1536):
        self.collection_id = collection_id
        self.config = config
        self.embedded_dim = embedded_dim

        # MongoVectorStore client
        self.client = MongoVectorStore(
            uri=self.config["uri"],
            db_name=self.config["db_name"],
            collection_name=self.collection_id,
            embedding_dim=self.embedded_dim
        )

    def delete_collection(self) -> None:
       
        self.client.client[self.client.db_name].drop_collection(self.collection_id)

    def get_vector_store(self) -> MongoVectorStore:
        
        return self.client

    def delete_data_source(self, data_source_id: str) -> None:
        """
        Belirli bir data source'u MongoDB koleksiyonundan siler.
        """
        collection = self.get_vector_store()
        collection.delete_many({"data_source_id": data_source_id})
        delete_data_source(data_source_id)