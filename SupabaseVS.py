import os
from dotenv import load_dotenv
from vector_protocol import VectorStoreProtocol
from llama_index.vector_stores.supabase import SupabaseVectorStore

# .env dosyasını yükle
load_dotenv()

class SupabaseVS(VectorStoreProtocol):
    def __init__(self, collection_id: str):
        self.collection_id = collection_id

        # ENV'den config bilgilerini alıyoruz
        self.config = {
            "url": os.getenv("SUPABASE_URL"),
            "key": os.getenv("SUPABASE_KEY"),
        }

        # Supabase vector store instance
        self.vector_store = SupabaseVectorStore(
            collection_name=self.collection_id,
            url=self.config["url"],
            key=self.config["key"],
        )

    def delete_collection(self) -> None:
        # Supabase'de koleksiyonu silme işlemi
        self.vector_store.delete_collection(self.collection_id)

    def get_vector_store(self) -> SupabaseVectorStore:
        return self.vector_store
