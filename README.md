# LlamaIndex
# 🧠 Vector Store Entegrasyonları

Bu proje, çeşitli **vektör veri tabanları (vector stores)** ile kolayca çalışmanı sağlayan Python modüllerini içerir.  
Her bir branch, farklı bir vektör veri tabanının temel işlemlerini gerçekleştirecek şekilde yapılandırılmıştır.

## 🚀 Özellikler
- Çoklu vektör veri tabanı desteği
- Esnek yapılandırma dosyaları (.env)
- Temiz ve modüler Python kod yapısı
- CRUD (Create, Read, Update, Delete) operasyonları için hazır metodlar
- Kolay genişletilebilir mimari


## 🗂️ Desteklenen Vektör Veri Tabanları
Projede farklı branch’ler halinde aşağıdaki veri tabanları desteklenmektedir:

| Branch Adı      | Teknoloji       | Açıklama                                  |
|-----------------|-----------------|-------------------------------------------|
| `ChromaDB`      | Chroma          | Hafif ve hızlı vektör depolama            |
| `Couchbase`     | Couchbase       | Yüksek performanslı KV-store              |
| `Dash-Vector`   | Dash            | Veri analizi ve görselleştirme için destek|
| `Elasticsearch` | Elasticsearch   | Gelişmiş arama ve indeksleme              |
| `MongoDB-Atlas` | MongoDB Atlas   | Bulut tabanlı MongoDB entegrasyonu        |
| `Neo4jVector`   | Neo4j           | Graph tabanlı vektör veritabanı           |
| `Open-Search`   | OpenSearch      | AWS uyumlu arama motoru                   |
| `Pinecone`      | Pinecone        | Ölçeklenebilir vektör arama altyapısı     |
| `Qdrant`        | Qdrant          | GPU destekli vektör arama veritabanı      |



## 🛠️ Kurulum

Öncelikle gerekli Python bağımlılıklarını yükleyin:

```bash
pip install -r requirements.txt
