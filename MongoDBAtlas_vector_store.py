
import os
import pymongo 
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch 
from llama_index.core import VectorStoreIndex 
from llama_index.core import StorageContext 
from llama_index.core import SimpleDirectoryReader

os.environ["OPENAI_API_KEY"] = "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"

mongo_uri = ( "mongodb+srv://vectorUser:M0ng0DBAI2025@vectormongodb.zh0nhso.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"
)

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

