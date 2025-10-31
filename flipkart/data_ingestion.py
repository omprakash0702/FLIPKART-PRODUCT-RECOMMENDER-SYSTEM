from langchain_astradb import AstraDBVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings  # Use local embeddings
from flipkart.data_converter import DataConverter
from flipkart.config import Config

class DataIngestor:
    def __init__(self):
        # Use local HuggingFace embeddings instead of endpoint
        self.embedding = HuggingFaceEmbeddings(
            model_name=Config.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},  # Use 'cuda' if you have GPU
            encode_kwargs={'normalize_embeddings': True}
        )

        self.vstore = AstraDBVectorStore(
            embedding=self.embedding,
            collection_name="flipkart_database",
            api_endpoint=Config.ASTRA_DB_API_ENDPOINT,
            token=Config.ASTRA_DB_APPLICATION_TOKEN,
            namespace=Config.ASTRA_DB_KEYSPACE
        )

    def ingest(self, load_existing=True):
        if load_existing == True:
            return self.vstore
        
        docs = DataConverter("data/flipkart_product_review.csv").convert()
        self.vstore.add_documents(docs)
        return self.vstore