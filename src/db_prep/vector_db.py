import chromadb
import hashlib
from sentence_transformers import SentenceTransformer


class VectorDB:
    def __init__(self, db_name: str, persist_dir: str = "./database", embedder_name: str = "all-mpnet-base-v2"):
        self.client = chromadb.Client(chromadb.config.Settings(persist_directory=persist_dir))
        self.model = SentenceTransformer(embedder_name)
        
        for collection in self.client.list_collections():
            if collection.name == db_name:
                self.client.delete_collection(name=db_name)
        self.collection = self.client.get_or_create_collection(name=db_name)

    def _embed_text(self, text: str):
        return self.model.encode(text)

    def add(self, docs: list):
        ids = []
        embeddings = []
        metadatas = []
        documents = []
        
        for doc in docs:
            document = doc["document"]
            metadata = doc["metadata"]

            embedding = self._embed_text(document)
            doc_id = hashlib.md5((document).encode()).hexdigest()
            
            ids.append(doc_id)
            embeddings.append(embedding)
            metadatas.append(metadata)
            documents.append(document)

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents
        )
    
    def query(self, query_text: str, n_results: int = 1):
        query_embedding = self._embed_text(query_text)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["embeddings", "metadatas", "documents"],
        )
        return results
    
    def __len__(self):
        return self.collection.count()

    