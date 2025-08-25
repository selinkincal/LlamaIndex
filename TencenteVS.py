from typing import Sequence
from llama_index.core import BaseNode, VectorStoreIndex, StorageContext
from llama_index.vector_stores.tencent import TencentVectorStore  # Tencent için özel adapter
from tencentcloud.vdb.v20230901 import vdb_client, models
from tencentcloud.common import credential
from helpers.database_helpers import delete_data_source, fetch_items, settings
from vector_protocol import VectorStoreProtocol


class TencentVS(VectorStoreProtocol):
    def __init__(self, collection_id: str, config: dict, embded_dim: int = 1536):
       
        self.collection_id = collection_id
        self.embedded_dim = embded_dim
        self.config = config

        self.cred = credential.Credential(
            self.config["secret_id"],
            self.config["secret_key"]
        )

      
        self.client = vdb_client.VdbClient(
            self.cred,
            self.config["region"]
        )

    def delete_collection(self) -> None:
        
        try:
            req = models.DeleteCollectionRequest()
            req.CollectionName = self.collection_id
            self.client.DeleteCollection(req)
        except Exception as e:
            raise RuntimeError(f"Tencent koleksiyonu silinirken hata oluştu: {e}")

    def get_vector_store(self) -> TencentVectorStore:
        
        try:
            return TencentVectorStore(
                client=self.client,
                collection_name=self.collection_id,
                embedding_dim=self.embedded_dim
            )
        except Exception as e:
            raise RuntimeError(f"Tencent Vector Store oluşturulamadı: {e}")

