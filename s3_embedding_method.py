from typing import Sequence, List, Protocol, Optional
from llama_index.core.schema import Document, BaseNode
from llama_index.readers.s3 import S3Reader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
import multiprocessing

class VectorStoreProtocol:
    pass
class TaskManagerProtocol:
    pass
class EmbeddingMethod(Protocol):
    """Common protocol for all embedding methods"""

    def get_documents(self, data_source_id: str) -> Sequence[Document]:
        """Get documents from the data source."""
        raise NotImplementedError

    def get_nodes(self, documents: Sequence[Document]) -> Sequence[BaseNode]:
        """Process documents and return nodes."""
        raise NotImplementedError

    @staticmethod
    def customize_metadata(
        document: Document, data_source_id: str, **kwargs
    ) -> Document:
        """Modify metadata of the nodes."""
        raise NotImplementedError

    def apply_rules(
        self,
        documents: Sequence[Document],
        inclusion_rules: List[str],
        exclusion_rules: List[str],
    ) -> Sequence[Document]:
        """Apply rules to the documents."""
        raise NotImplementedError
    
    def process(
        self,
        vector_store: VectorStoreProtocol,
        task_manager: TaskManagerProtocol,
        data_source_id: str,
        task_id: str,
        **kwargs,
    ) -> None:
        """Process the embedding method with the given parameters."""
        raise NotImplementedError
    

class S3EmbeddingMethod(EmbeddingMethod):
    """Embedding method for S3 bucket"""

    def __init__(self, bucket: str, prefix: str = "", aws_access_id: str = "", aws_access_secret: str = "", region_name: str = "eu-north-1"):
        self.bucket = bucket
        self.prefix = prefix
        self.aws_access_id = aws_access_id
        self.aws_access_secret = aws_access_secret
        self.region_name = region_name

    @staticmethod
    def customize_metadata(document: Document, data_source_id: str, **kwargs) -> Document:
        document.metadata = {
            "description": document.metadata.get("description", ""),
            "data_source_id": data_source_id,
        }
        return document
    
    def apply_rules(self, documents: Sequence[Document], inclusion_rules: List[str], exclusion_rules: List[str]) -> Sequence[Document]:
        return documents  # Gerekirse filtreleme ekleyebilirsin

    def get_documents(self, data_source_id: str, key: Optional[str] = None) -> List[Document]:
        if key:
            reader = S3Reader(
                bucket=self.bucket,
                key=key,
                aws_access_id=self.aws_access_id,
                aws_access_secret=self.aws_access_secret,
                region_name=self.region_name
            )
        else:
            reader = S3Reader(
                bucket=self.bucket,
                prefix=self.prefix,
                aws_access_id=self.aws_access_id,
                aws_access_secret=self.aws_access_secret,
                region_name=self.region_name
            )
        documents = reader.load_data()
        for document in documents:
            self.customize_metadata(document, data_source_id)
        return documents

    def get_nodes(self, documents: Sequence[Document]) -> Sequence[BaseNode]:
        pipeline = IngestionPipeline(
            transformations=[
                SentenceSplitter(chunk_size=512, chunk_overlap=20)
            ]
        )
        num_workers = multiprocessing.cpu_count()
        return pipeline.run(documents=documents, num_workers=num_workers)
    

    def process(
        self,
        vector_store: VectorStoreProtocol,
        task_manager: TaskManagerProtocol,
        data_source_id: str,
        task_id: str,
        **kwargs,
    ) -> None:
        # Şimdilik içi boş, sonra doldurabilirsin
        pass 

s3_embedder = S3EmbeddingMethod(
    bucket="phyton-bucket27",
    prefix="dosyalar/", 
    aws_access_id="AKIA4UR6H2EZGEBYQ3CM",
    aws_access_secret="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",
    region_name="eu-north-1"
)
documents = s3_embedder.get_documents(data_source_id="s3_1")
print(f"{len(documents)} adet belge bulundu.")  
nodes = s3_embedder.get_nodes(documents)
