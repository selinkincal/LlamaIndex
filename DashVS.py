from vector_protocol import VectorStoreProtocol
from llama_index.core import BaseNode, VectorStoreIndex, StorageContext
from llama_index.core.vector_stores.types import MetadataFilter, MetadataFilters
from helpers.database_helpers import delete_data_source
from dashvector import Client as DashClient
from llama_index.vector_stores.dashvector.base import DashVectorStore

class DashVS(VectorStoreProtocol):
    def __init__(self, collection_id: str, config: dict, embded_dim: int = 1536):
       
        self.collection_id = collection_id
        self.config = config
        self.embedded_dim = embded_dim
        
        self.client = DashClient(api_key=self.config["api_key"])

        # loleksiyonu oluştur veya al
        self.collection = self.client.get(self.collection_id)
        if not self.collection:
            self.client.create(self.collection_id, dimension=self.embedded_dim)
            self.collection = self.client.get(self.collection_id)

        self.vector_store = DashVectorStore(self.collection)

    def delete_collection(self) -> None:
       
        self.client.delete(self.collection_id)

    def get_vector_store(self) -> DashVectorStore:
       
        return self.vector_store

    def delete_data_source(self, data_source_id: str) -> None:
   
        # Dash üzerindeki node'ları sil
        filters = [MetadataFilter(key="data_source_id", value=data_source_id)]
        nodes_to_delete = self.vector_store.query(filters=filters)
        for node in nodes_to_delete:
            self.vector_store.delete(ref_doc_id=node.node_id)

        # Veritabanındaki datasource kaydını sil
        delete_data_source(data_source_id)
