
import os
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from pinecone import Pinecone
from dotenv import load_dotenv
load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
pinecone_key = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=pinecone_key)
pinecone_index = pc.Index("pinecone-llamaindex")


vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

documents = SimpleDirectoryReader("./data/paul_graham_essay1").load_data()

index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

query_engine = index.as_query_engine()
response = query_engine.query("Yazar ilk yıllarında ne tür programlamalar yaptı?")
print(response)