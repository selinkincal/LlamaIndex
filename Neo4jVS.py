import os
from dotenv import load_dotenv
from typing import Sequence
from llama_index.core import BaseNode, VectorStoreIndex, StorageContext
from llama_index_vector_stores_neo4jvector import Neo4jVectorStore  # ✅ Doğru
from vector_protocol import VectorStoreProtocol

load_dotenv()

neo4j_config = {
    "uri": os.getenv("NEO4J_URI"),
    "username": os.getenv("NEO4J_USERNAME"),
    "password": os.getenv("NEO4J_PASSWORD"),
    "database": os.getenv("NEO4J_DATABASE", "neo4j")
}

class Neo4jVS(VectorStoreProtocol):
    def __init__(self, collection_id: str, config: dict = neo4j_config, embed_dim: int = 1536):
        
        self.collection_id = collection_id
        self.config = config
        self.embed_dim = embed_dim

        # Neo4j Vector Store client
        self.client = Neo4jVectorStore(
            url=self.config["uri"],
            username=self.config["username"],
            password=self.config["password"],
            database=self.config["database"],
            index_name=f"vector_index_{self.collection_id}"   #otomatik index oluşturulacak
        )

    def delete_collection(self) -> None:
       
        self.client.delete_index()

    def get_vector_store(self) -> Neo4jVectorStore:
      
        return self.client

    