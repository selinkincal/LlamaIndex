from datetime import timedelta
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from llama_index.vector_stores.couchbase import CouchbaseSearchVectorStore
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
import os
from dotenv import load_dotenv

load_dotenv()

COUCHBASE_CONNECTION_STRING = os.getenv("COUCHBASE_CONNECTION_STRING")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

auth = PasswordAuthenticator(DB_USERNAME, DB_PASSWORD)
options = ClusterOptions(auth)
cluster = Cluster(COUCHBASE_CONNECTION_STRING, options)
cluster.wait_until_ready(timedelta(seconds=5))


vector_store = CouchbaseSearchVectorStore(
    cluster=cluster,
    bucket_name="vector-data",
    scope_name="_default",
    collection_name="_default",
    index_name="vector-index",
)


documents = SimpleDirectoryReader("./data/paul_graham_essay3.txt").load_data()
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)


