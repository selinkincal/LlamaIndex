
import openai
from llama_index.vector_stores.singlestoredb import SingleStoreVectorStore
from llama_index.core.schema import TextNode
from llama_index.core.vector_stores import VectorStoreQuery
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

vector_store = SingleStoreVectorStore(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    table_name="documents",
    content_field="content",
    metadata_field="metadata",
    vector_field="embedding",
    timeout=30,
)


def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

my_text = """Llama Index, farklı kaynaklardan gelen verileri kolayca işleyip, embedding'lere dönüştürerek vector store'larda saklamayı sağlar. Vector store'lar, metinlerin sayısal vektör temsilcilerini tutar ve benzer içeriklerin hızlıca bulunmasını mümkün kılar. Bu sayede yapay zeka uygulamalarında, bilgiye erişim ve arama performansı çok artar. SinglestoreDB ise güçlü bir vector store çözümü olarak, ölçeklenebilir ve hızlı sorgulama imkanı sunar."""
doc_id = "llama_index_001"
embedding_vector = get_embedding(my_text)

node = TextNode(
    text=my_text,
    id_=doc_id,
    embedding=embedding_vector,
    metadata={"kategori": "hava durumu"}

)

vector_store.add([node])
print("Metin başarıyla eklendi!")

vector_store.delete(ref_doc_id="llama_index_001")
print("Belirtilen doküman silindi.")

query_text = "Llama Index nedir?"
query_embedding = get_embedding(query_text)
query = VectorStoreQuery(query_embedding=query_embedding, similarity_top_k=3)
result = vector_store.query(query)

for node in result.nodes:
    print("Sonuç:", node.text)

