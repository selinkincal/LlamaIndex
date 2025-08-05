# LlamaIndex
# 🧠 Vector Store Entegrasyonları

Bu proje, farklı vektör veritabanları (vector stores) ile kolayca çalışmanı sağlayan Python modülleri içerir. Her dosya belirli bir veritabanı için hazırlanmış ve temel işlemleri gerçekleştirecek şekilde yapılandırılmıştır.


# ⚙️ Kurulum

Öncelikle gerekli Python paketlerini kurmalısınız:

```bash
pip install -r requirements.txt

# 🗂️ Proje Yapısı

├── Chroma_vector_store.py
├── Couchbase_vector_store.py
├── MongoDBAtlas_vector_store.py
├── Pinecone_vector_store.py
├── Qdrant_vector_store.py
├── Single_store_vector.py
├── Supabase_vector_store.py
├── s3_embedding_method.py
├── s3_vector_store.py
├── Weaviate_vector_store.py
├── requirements.txt
└── README.md


# 📁 Dosyalar ve Detaylı Açıklamaları

Aşağıda bu projede bulunan dosyalar ve her birinin görevi detaylı bir şekilde açıklanmıştır.

### 🔹 `Chroma_vector_store.py`
- [Chroma DB](https://www.trychroma.com/) ile vektör verilerini yerel olarak saklamak ve aramak için kullanılır.
- Hafif, hızlı ve yerel geliştirme için uygundur.
- Kurulum ve kullanım kolaylığı sayesinde prototipleme için idealdir.


### 🔹 `Couchbase_vector_store.py`
- [Couchbase](https://www.couchbase.com/) NoSQL veritabanı ile çalışır.
- Embedding verilerini Couchbase’e kaydeder ve buradan vektör araması yapar.
- Couchbase’in full-text arama ve JSON doküman özelliklerinden faydalanır.
- Büyük ölçekli sistemlerde güçlü bir alternatif olabilir.


### 🔹 `MongoDBAtlas_vector_store.py`
- [MongoDB Atlas](https://www.mongodb.com/atlas/database) üzerinde çalışan bir çözüm.
- Bulut tabanlı, güvenli ve ölçeklenebilir bir altyapı sunar.
- Metin + vektör aramaları gibi karmaşık sorguları destekler.

### 🔹 `Pinecone_vector_store.py`
- [Pinecone](https://www.pinecone.io/) ile çalışır.
- Büyük miktarda embedding verisini saklamak ve hızlıca benzerlik aramaları yapmak için idealdir.
- API tabanlıdır, kendi iç depolama altyapısını kullanır.
- Performans ve güvenlik açısından üst düzeydedir.

### 🔹 `Qdrant_vector_store.py`
- [Qdrant](https://qdrant.tech/) açık kaynak vektör veritabanı ile çalışır.
- Filtreleme, metadata desteği ve yüksek performans sunar.
- Docker ile kolayca kurulur, lokal veya uzak sunucuda çalışabilir.
- Python SDK’sı üzerinden kolayca kontrol edilebilir.

### 🔹 `Single_store_vector.py`
- [SingleStore](https://www.singlestore.com/) ile entegredir.
- SQL tabanlı bir vektör veritabanı sağlar.
- Yapısal veriler ile embedding verilerini birlikte sorgulamak isteyen projeler için uygundur.


### 🔹 `Supabase_vector_store.py`
- [Supabase](https://supabase.com/) + `pgvector` kullanılarak PostgreSQL üzerinde çalışır.
- Açık kaynak ve sunucusuz altyapı ile hızlı kurulum sağlar.
- SQL sorguları ile embedding verileri üzerinde çalışabilirsiniz.
- Uygun maliyetli ve geliştirici dostudur.


### 🔹 `s3_embedding_method.py`
- Embedding üretimi için kullanılan merkezi bir modüldür.
- Belge veya metinleri alır, embedding (vektör) verisine çevirir.
- OpenAI, HuggingFace, Sentence Transformers gibi modeller ile uyumlu çalışabilir.
- Üretilen embedding’ler vektör store’lara gönderilmek üzere kullanılır.


### 🔹 `s3_vector_store.py`
- AWS S3 üzerinde embedding verilerini saklamak için geliştirilmiştir.
- Küçük projeler, lokal testler veya dosya bazlı uygulamalar için uygundur.
- Vektör araması, belleğe yüklenmiş veriler üzerinden yapılır.


### 🔹 `Weaviate_vector_store.py`
- [Weaviate](https://weaviate.io/) ile entegre çalışır.
- REST veya GraphQL API üzerinden erişilebilir.
- Otomatik schema tanımlama, metadata filtreleme gibi gelişmiş özellikler sunar.
- Docker veya Weaviate Cloud hizmeti üzerinden çalışabilir.
- Tamamen açık kaynak ve geliştirici dostudur.


## 🧠 Ne zaman hangi vector store'u kullanmalıyım?

- **Hızlı prototipleme** → `Chroma`, `Qdrant`, `Weaviate`
- **Kurumsal ve ölçeklenebilir çözümler** → `Pinecone`, `MongoDBAtlas`, `SingleStore`
- **Sunucusuz mimari** → `Supabase`, `S3 Vector Store`
- **Offline veya yerel test ortamı** → `Chroma`, `S3 Vector Store`
- **SQL tabanlı yapı tercih ediyorsanız** → `SingleStore`, `Supabase`


