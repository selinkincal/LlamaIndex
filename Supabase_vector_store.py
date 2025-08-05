
import os
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.vector_stores.supabase import SupabaseVectorStore
from llama_index.core.schema import TextNode
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters
import textwrap

os.environ["OPENAI_API_KEY"] = "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"

PG_CONN_STR = "postgresql://postgres:spbsllamaındex2025@db.phberswfcmldavtuircd.supabase.co:5432/postgres"
documents = SimpleDirectoryReader("./data/").load_data()
print(f"Yüklenen belge ID: {documents[0].doc_id}")

vector_store_docs = SupabaseVectorStore(
    postgres_connection_string=PG_CONN_STR,
    collection_name="base_demo"
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
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
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex(nodes, storage_context=storage_context)


filters = MetadataFilters(filters=[ExactMatchFilter(key="theme", value="Mafia")])
retriever = index.as_retriever(filters=filters)
results = retriever.retrieve("What is inception about?")
for result in results:
    print(result.node.text, result.node.metadata)


