import os
from typing import Sequence
from vector_protocol import VectorStoreProtocol, VectorStoreIndex, BaseNode, StorageContext, MetadataFilter, MetadataFilters
from couchbase.cluster import Cluster, ClusterOptions
from couchbase.auth import PasswordAuthenticator
from couchbase.collection import Collection

class CouchbaseVS(VectorStoreProtocol):
    def __init__(self, collection_id: str, embedded_dim: int = 1536):
    
        self.collection_id = collection_id
        self.embedded_dim = embedded_dim

        COUCHBASE_URL = os.getenv("COUCHBASE_URL")
        COUCHBASE_USER = os.getenv("COUCHBASE_USER")
        COUCHBASE_PASSWORD = os.getenv("COUCHBASE_PASSWORD")
        COUCHBASE_BUCKET = os.getenv("COUCHBASE_BUCKET")

        self.cluster = Cluster(
            COUCHBASE_URL,
            ClusterOptions(PasswordAuthenticator(COUCHBASE_USER, COUCHBASE_PASSWORD))
        )
        self.bucket = self.cluster.bucket(COUCHBASE_BUCKET)
        self.collection: Collection = self.bucket.default_collection()

    def delete_collection(self) -> None:
        query = f'DELETE FROM `{self.bucket.name}` WHERE collection_id = $collection_id'
        self.cluster.query(query, {"collection_id": self.collection_id}).execute()

    def get_vector_store(self) -> "CouchbaseVectorStore":
        return CouchbaseVectorStore(self.collection, self.collection_id)


class CouchbaseVectorStore:
    
    def __init__(self, collection: Collection, collection_id: str):
        self.collection = collection
        self.collection_id = collection_id

    def add_nodes(self, nodes: Sequence[BaseNode]):
        for node in nodes:
            doc_id = node.id
            self.collection.upsert(doc_id, {
                "collection_id": self.collection_id,
                "embedding": node.embedding,
                "text": node.text,
                "metadata": getattr(node, "metadata", {})
            })

    def delete_nodes(self, filters: MetadataFilters):
        
        for f in filters.filters:
            query = f'DELETE FROM `{self.collection.bucket_name}` WHERE collection_id = $collection_id AND {f.key} = $value'
            self.collection.cluster.query(query, {"collection_id": self.collection_id, "value": f.value}).execute()
