import chromadb
import hashlib
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

load_dotenv()


class VectorDB:
    def __init__(self, db_name: str,
                #  persist_dir: str = os.path.join(os.getenv("PROJECT_DIR"), "database"),
                 persist_dir: str = os.path.join(os.getcwd(), "database"),
                 embedder_name: str = "all-mpnet-base-v2"):
        
        if not os.path.exists(persist_dir):
            os.makedirs(persist_dir)
        
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.model = SentenceTransformer(embedder_name)
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
            include=["embeddings", "metadatas", "documents", "distances"],
        )
        return results
    
    def __len__(self):
        return self.collection.count()
    
    def clear_collection(self, collection_name: str):
        self.client.delete_collection(name=collection_name)

    def get_docs(self):
        documents = self.collection.get(include=['embeddings', 'documents', 'metadatas'])
        return documents
    