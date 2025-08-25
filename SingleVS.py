
import os
from dotenv import load_dotenv
from typing import Sequence
from llama_index.core import BaseNode, VectorStoreIndex, StorageContext
from llama_index.vector_stores.singlestore import SingleStoreVectorStore  # <-- Bunu kullanacağız
from helpers.database_helpers import delete_data_source, fetch_items, settings
from .vector_protocol import VectorStoreProtocol  # Eğer aynı dosyadaysa gerek yok

# .env dosyasını yükle
load_dotenv()

class SingleStoreVS(VectorStoreProtocol):
    def __init__(self, collection_id: str):
        self.collection_id = collection_id

        # ENV'den config bilgilerini alıyoruz
        self.config = {
            "host": os.getenv("SINGLESTORE_HOST"),
            "port": int(os.getenv("SINGLESTORE_PORT", 3306)),
            "user": os.getenv("SINGLESTORE_USER"),
            "password": os.getenv("SINGLESTORE_PASSWORD"),
            "database": os.getenv("SINGLESTORE_DATABASE"),
        }

        # SingleStore bağlantısını kur
        self.vector_store = SingleStoreVectorStore(
            host=self.config["host"],
            port=self.config["port"],
            user=self.config["user"],
            password=self.config["password"],
            database=self.config["database"],
            table_name=self.collection_id,
        )


    def delete_collection(self) -> None:
        
        try:
            self.vector_store.delete_table()
        except Exception as e:
            raise RuntimeError(f"Koleksiyon silinirken hata oluştu: {e}")

    def get_vector_store(self) -> SingleStoreVectorStore:
        
        return self.vector_store
