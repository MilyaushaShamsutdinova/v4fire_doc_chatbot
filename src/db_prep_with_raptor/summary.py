from src.db_prep_with_raptor.vector_db import VectorDB
from sklearn.cluster import KMeans
from src.backend.llm import GeminiAI

gemini = GeminiAI()


def cluster_documents(level: int, avg_cluster_size: int = 5) -> list[str]:
    db = VectorDB(f"docs_{level}")
    docs = db.get_docs()
    embeddings = docs['embeddings']
    documents = docs['documents']

    num_clusters = max(len(embeddings) // avg_cluster_size, 1)
    kmeans = KMeans(n_clusters=num_clusters).fit(embeddings)
    
    clusters = [[] for _ in range(num_clusters)]
    for i, label in enumerate(kmeans.labels_):
        clusters[label].append(documents[i])
    return clusters


def generate_summary(clusters: list[str]):
    summaries = []
    for cluster in clusters:
        combined_text = " ".join(cluster)
        summary = gemini.get_summary(combined_text)
        summaries.append(summary)
    return summaries


def store_summaries(summaries, level):
    db = VectorDB(f"docs_{level}")
    summaries = [
        {
            "document": summary,
            "metadata": {"level": level}
        }
        for summary in summaries
    ]
    db.add(summaries)

