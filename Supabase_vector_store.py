
import os
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.vector_stores.supabase import SupabaseVectorStore
from llama_index.core.schema import TextNode
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters
import textwrap
from dotenv import load_dotenv
load_dotenv() 

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PG_CONN_STR = os.getenv("PG_CONN_STR")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

documents = SimpleDirectoryReader("./data/").load_data()
print(f"Yüklenen belge ID: {documents[0].doc_id}")

vector_store_docs = SupabaseVectorStore(
    postgres_connection_string=PG_CONN_STR,
    collection_name="base_demo"
)
storage_context = StorageContext.from_defaults(vector_store=vector_store_docs)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

nodes = [
    TextNode(text="The Shawshank Redemption", metadata={"author": "Stephen King", "theme": "Friendship"}),
    TextNode(text="The Godfather", metadata={"director": "Francis Ford Coppola", "theme": "Mafia"}),
    TextNode(text="Inception", metadata={"director": "Christopher Nolan"}),
]

vector_store_metadata = SupabaseVectorStore(
    postgres_connection_string=PG_CONN_STR,
    collection_name="metadata_demo"
)
storage_context = StorageContext.from_defaults(vector_store=vector_store_metadata)
index = VectorStoreIndex(nodes, storage_context=storage_context)

filters = MetadataFilters(filters=[ExactMatchFilter(key="theme", value="Mafia")])
retriever = index.as_retriever(filters=filters)
results = retriever.retrieve("What is inception about?")
for result in results:
    print(result.node.text, result.node.metadata)



