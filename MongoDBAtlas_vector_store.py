
import os
import pymongo 
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch 
from llama_index.core import VectorStoreIndex 
from llama_index.core import StorageContext 
from llama_index.core import SimpleDirectoryReader
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
mongo_uri = os.getenv("MONGODB_ATLAS_URI")

mongodb_client = pymongo.MongoClient(mongo_uri)


store = MongoDBAtlasVectorSearch(
    mongodb_client,
    db_name="llama_pdf_arşivi",
    collection_name="documents_uber_2021"
)
store.create_vector_search_index(
    dimensions=1536,
    path="embedding",
    similarity="cosine"
)

storage_context = StorageContext.from_defaults(vector_store=store)
uber_docs = SimpleDirectoryReader(
    input_files=["./data/uber_2021.pdf"]
).load_data()
index = VectorStoreIndex.from_documents(
    uber_docs, storage_context=storage_context
)

response = index.as_query_engine().query("Uber'in geliri ne kadardı?")
print(response)


