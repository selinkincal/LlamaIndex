# main_opensearch.py
import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, StorageContext, SimpleDirectoryReader, Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.opensearch import OpenSearchVectorStore
from opensearchpy import OpenSearch


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY bulunamadı! .env dosyasını kontrol et.")
os.environ["OPENAI_API_KEY"] = api_key


class OpenSearchVS:
    def __init__(self, index_name: str, host="localhost", port=9200, user=None, password=None):
        self.index_name = index_name
        self.client = OpenSearch(
            hosts=[{"host": host, "port": port}],
            http_auth=(user, password) if user and password else None
        )

    def delete_index(self) -> None:
        """OpenSearch index'i siler"""
        if self.client.indices.exists(index=self.index_name):
            self.client.indices.delete(index=self.index_name)

    def get_vector_store(self) -> OpenSearchVectorStore:
        return OpenSearchVectorStore(
            opensearch_client=self.client,
            index_name=self.index_name
        )

    def create_index(self, nodes):
        vector_store = self.get_vector_store()
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        return VectorStoreIndex(nodes, storage_context=storage_context)
