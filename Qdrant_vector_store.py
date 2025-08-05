import qdrant_client
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
import os

os.environ["OPENAI_API_KEY"] = "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"

# Qdrant bağlantısı
client = qdrant_client.QdrantClient(
    host="localhost",
      port=6333
)

#Qdrant koleksiyonu
vector_store = QdrantVectorStore(client=client, collection_name="my_collection")
documents = SimpleDirectoryReader("./data/paul_graham_essay2.txt/").load_data()
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, 
    storage_context=storage_context
)


query_engine = index.as_query_engine()
response = query_engine.query("What did the author do growing up?")
