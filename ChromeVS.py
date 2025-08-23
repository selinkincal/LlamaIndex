import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.schema import BaseNode
from typing import Sequence, List
from vector_protocol import VectorStoreProtocol  # Protocol dosyanı import ettim

class ChromaVS(VectorStoreProtocol):
    def __init__(self, collection_id: str, config: dict, embedded_dim: int = 1536):
     
        self.collection_id = collection_id
        self.config = config
        self.embedded_dim = embedded_dim
        self.remote_db = chromadb.HttpClient(
            host=self.config["host"],
            port=self.config["port"],
        )

    def check_collection(self) -> bool:
      
        try:
            collection = self.remote_db.get_or_create_collection(self.collection_id)
            # Chroma'da direkt sayma yok, örnek olarak sorgu yapabiliriz
            result = collection.query(query_embeddings=[0.0]*self.embedded_dim, n_results=1)
            return bool(result['ids'])  # En az 1 node varsa True
        except Exception:
            return False

    def delete_collection(self) -> None:
        
        self.remote_db.delete_collection(self.collection_id)

    def get_vector_store(self) -> ChromaVectorStore:
        
        collection = self.remote_db.get_or_create_collection(self.collection_id)
        return ChromaVectorStore(chroma_collection=collection)

    def delete_data_source(self, data_source_id: str) -> None:
      
        vector_store = self.get_vector_store()
        vector_store.delete_nodes(node_ids=[data_source_id])

    def create_index(self, nodes: Sequence[BaseNode]) -> VectorStoreIndex:
        
        vector_store = self.get_vector_store()
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        return VectorStoreIndex(nodes, storage_context=storage_context)

    def get_index(self) -> VectorStoreIndex:
        
        vector_store = self.get_vector_store()
        return VectorStoreIndex.from_vector_store(vector_store)

    def search(self, query_embedding: list, top_k: int = 5) -> List[BaseNode]:
        
        vector_store = self.get_vector_store()
        result = vector_store.query(query_embedding=query_embedding, similarity_top_k=top_k)
        return result.nodes

    def list_nodes(self, top_k: int = 100) -> List[BaseNode]:
        
        vector_store = self.get_vector_store()
        result = vector_store.query(query_embedding=[0.0]*self.embedded_dim, similarity_top_k=top_k)
        return result.nodes
