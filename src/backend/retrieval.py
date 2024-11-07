from src.db_prep.vector_db import VectorDB


def retrieve_relevant(text: str, n_results: int = 2):
    db = VectorDB(db_name="docs")
    results = db.query(query_text=text, n_results=n_results)
    rel_docs = []

    # preprocessing to retrieve only most relevant and in format list of strings
    for i in range(len(results['ids'][0])):
        rel_docs.append(f"{results['documents'][0][i]}\n Reference: {results['metadatas'][0][i]['url']}")

    return rel_docs


# query_text = "write component that creates button based on icon using b-icon-button"
# print(retrieve_relevant(query_text))
