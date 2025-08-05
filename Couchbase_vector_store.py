from datetime import timedelta
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from llama_index.vector_stores.couchbase import CouchbaseSearchVectorStore
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext

COUCHBASE_CONNECTION_STRING = "couchbases://cb.3ovlzfr3klydpgu.cloud.couchbase.com"
DB_USERNAME = "couchbaseLlamaIndex"
DB_PASSWORD = "N0d3X!9tLeRu7K"

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

