import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from typing import Protocol, Sequence
from llama_index.core.schema import TextNode, BaseNode
from llama_index.embeddings.openai import OpenAIEmbedding
from dotenv import load_dotenv
load_dotenv()

embed_model = OpenAIEmbedding(model="text-embedding-ada-002") 


class VectorStoreProtocol(Protocol):
    def __init__(self, collection_id: str):
        ...

    def check_collection(self) -> bool:
        ...

    def delete_collection(self, delete_data_sources: bool) -> None:
        ...

    def delete_data_source(self, data_source_id: str) -> None:
        ...

    def get_index(self) -> VectorStoreIndex:
        ...

    def create_index(self, nodes: Sequence[BaseNode]) -> VectorStoreIndex:
        ...


class ChromaDBVectorStore(VectorStoreProtocol):
    def __init__(self, collection_id: str, persist_dir: str = "./chroma_db"):
        self.collection_id = collection_id
        self.persist_dir = persist_dir

    def get_vector_store(self) -> ChromaVectorStore:
        db = chromadb.PersistentClient(path=self.persist_dir)
        chroma_collection = db.get_or_create_collection(self.collection_id)
        return ChromaVectorStore(chroma_collection=chroma_collection)

    def create_index(self, nodes: Sequence[BaseNode]) -> VectorStoreIndex:
        vector_store = self.get_vector_store()
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        return VectorStoreIndex(nodes, storage_context=storage_context, insert_batch_size=100)

    def get_index(self) -> VectorStoreIndex:
        vector_store = self.get_vector_store()
        return VectorStoreIndex.from_vector_store(vector_store)

    def delete_collection(self, delete_data_sources=True) -> None:
        db = chromadb.PersistentClient(path=self.persist_dir)
        db.delete_collection(self.collection_id)

    def delete_data_source(self, data_source_id: str) -> None:
        # Chroma'da metadata ile filtreleyerek silme işlemi yapılabilir
        vector_store = self.get_vector_store()
        from llama_index.core.vector_stores import MetadataFilter, MetadataFilters
        filters = [MetadataFilter(key="data_source_id", value=data_source_id)]
        vector_store.delete_nodes(filters=MetadataFilters(filters=filters))

    def check_collection(self) -> bool:
        db = chromadb.PersistentClient(path=self.persist_dir)
        collections = [col.name for col in db.list_collections()]
        return self.collection_id in collections


db = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db.get_or_create_collection("ornek_koleksiyon")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

nodes = [
    TextNode(text="İlk doküman: LlamaIndex ile ChromaDB kullanımı.", id_="doc1"),
    TextNode(text="İkinci doküman: Python ile vektör veritabanı entegrasyonu.", id_="doc2"),
]

embed_model = OpenAIEmbedding()

index = VectorStoreIndex(
    nodes,
    storage_context=storage_context,
    embed_model=embed_model
)

query_engine = index.as_query_engine()
response = query_engine.query("LlamaIndex ile hangi veritabanı kullanıldı?")
print("Sorgu Sonucu:", response)