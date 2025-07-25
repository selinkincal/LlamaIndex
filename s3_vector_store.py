from llama_index.vector_stores.s3 import S3VectorStore
import boto3
from llama_index.core import VectorStoreIndex, StorageContext, Document
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.vector_stores.types import MetadataFilters, MetadataFilter, FilterOperator, FilterCondition
import os

load_dotenv()

aws_session = boto3.Session(
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    region_name=os.environ["AWS_REGION"],
)

openai_api_key = os.environ["OPENAI_API_KEY"]

vector_store = S3VectorStore.create_index_from_bucket(
    bucket_name_or_arn="python-bucket27",
    index_name="S3-index",
    dimension=1536,
    distance_metric="cosine",
    data_type="float32",
    insert_batch_size=500,
    non_filterable_metadata_keys=["custom_field"],
    sync_session=aws_session,
)

documents = [
    Document(text="Hello, world!", metadata={"key": "1"}),
    Document(text="Hello, world! 2", metadata={"key": "2"}),
]

index = VectorStoreIndex.from_documents(
    documents,
    storage_context=StorageContext.from_defaults(vector_store=vector_store),
    embed_model=OpenAIEmbedding(model="text-embedding-3-small", api_key="sk-proj-s4n_FzghR_EO0F6VhrZi2Kp9zxZbe42reTnxpzshT67doLhZzK3GWxZQ7s9RP8Rss2akSBHBUDT3BlbkFJEF2JbFbUIJepvSq1ARb_BhCQ0WxsWoMaXasWl3Gn373QY8qXdzgoC_kLuXsT0TYdRtF7-jdJ4AAZ"),
)


nodes = index.as_retriever(
    similarity_top_k=2,
    filters=MetadataFilters(
        filters=[
            MetadataFilter(key="key", value="2", operator=FilterOperator.EQ),
        ],
        condition=FilterCondition.AND,
    ),
).retrieve("Hello, world!")

print(nodes[0].text) 