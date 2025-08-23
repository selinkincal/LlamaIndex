from typing import Sequence
from vector_protocol import VectorStoreProtocol
from llama_index.core import BaseNode, VectorStoreIndex, StorageContext
from llama_index.core.vector_stores.types import MetadataFilter, MetadataFilters
from helpers.database_helpers import delete_data_source
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
import os
from dotenv import load_dotenv

load_dotenv()  # .env yükler

elastic_config = {
    "es_url": os.getenv("ELASTICSEARCH_URL"),
    "es_api_key": os.getenv("ELASTICSEARCH_API_KEY")
}

class ElasticVS(VectorStoreProtocol):
    def __init__(self, collection_id: str, config: dict = elastic_config, embed_dim: int = 1536):
        self.collection_id = collection_id
        self.config = config
        self.embed_dim = embed_dim

        
        self.vector_store = ElasticsearchStore(
            index_name=self.collection_id,
            es_url=self.config.get("es_url"),
            es_api_key=self.config.get("es_api_key"),
        )

    def delete_collection(self) -> None:
        try:
            self.vector_store.es_client.indices.delete(index=self.collection_id, ignore=[400, 404])
        except Exception:
            pass

    def get_vector_store(self) -> ElasticsearchStore:
        return self.vector_store

    def delete_data_source(self, data_source_id: str) -> None:
        filters = MetadataFilters(filters=[MetadataFilter(key="data_source_id", value=data_source_id)])
        self.vector_store.delete_nodes(filters=filters)
        delete_data_source(data_source_id)

    async def adelete_data_source(self, data_source_id: str) -> None:
        filters = MetadataFilters(filters=[MetadataFilter(key="data_source_id", value=data_source_id)])
        await self.vector_store.adelete_nodes(filters=filters)
        delete_data_source(data_source_id)

    def create_index(self, nodes: Sequence[BaseNode]) -> VectorStoreIndex:
        self.vector_store.add(nodes)
        storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        return VectorStoreIndex(nodes, storage_context=storage_context)

    async def acreate_index(self, nodes: Sequence[BaseNode]) -> VectorStoreIndex:
        await self.vector_store.async_add(nodes)
        storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        return VectorStoreIndex(nodes, storage_context=storage_context)

    def get_index(self) -> VectorStoreIndex:
        return VectorStoreIndex.from_vector_store(self.vector_store)

    def query(self, *args, **kwargs):
        return self.vector_store.query(*args, **kwargs)

    async def aquery(self, *args, **kwargs):
        return await self.vector_store.aquery(*args, **kwargs)

    def get_nodes(self, *args, **kwargs):
        return self.vector_store.get_nodes(*args, **kwargs)

    async def aget_nodes(self, *args, **kwargs):
        return await self.vector_store.aget_nodes(*args, **kwargs)
