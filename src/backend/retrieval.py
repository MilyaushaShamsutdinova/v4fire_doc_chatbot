from src.db_prep_with_raptor.vector_db import VectorDB
import spacy


nlp = spacy.load("en_core_web_sm")
technical_keywords = {"implement", "code", "integration", "detailed", "write"}
moderate_keywords = {"features", "benefits", "key points", "general", "usage", "principles"}
general_keywords = {"what", "who", "when", "where", "overview", "summary", "introduction", "explain"}

db_docs_0 = VectorDB(db_name="docs_0")
db_docs_1 = VectorDB(db_name="docs_1")
db_docs_2 = VectorDB(db_name="docs_2")

DISTANCE_THRESHOLD = 1.6


def estimate_query_complexity(query):
    doc = nlp(query.lower())
    
    if any(token.text in technical_keywords for token in doc) or len(doc) > 20:
        return 0
    
    if any(token.text in general_keywords for token in doc):
        if "detail" in query.lower() or "deep" in query.lower() or "explain in" in query.lower():
            return 1
        return 2

    if any(token.text in moderate_keywords for token in doc) or len(doc) > 10:
        return 1
    
    num_clauses = sum(1 for token in doc if token.dep_ in {"csubj", "ccomp", "xcomp", "advcl", "acl"})
    if num_clauses >= 2:
        return 0
    
    return 2


def retrieve_relevant_docs(query: str) -> list[str]:
    try:
        complexity_level = estimate_query_complexity(query)

        if complexity_level == 0:
            db = db_docs_0
        elif complexity_level == 1:
            db = db_docs_1
        else:
            db = db_docs_2

        results = db.query(query_text=query, n_results=5)
        distances = results["distances"][0]
        relevant_docs = []

        for i in range(len(distances)):
            doc = results['documents'][0][i]
            metadata = results['metadatas'][0][i]

            if distances[i] < DISTANCE_THRESHOLD:
                if 'url' in metadata:
                    relevant_docs.append(f"{doc}\nReference: {metadata['url']}")
                else:
                    relevant_docs.append(f"{doc}")
        return relevant_docs
    
    except Exception as e:
        print(e)
        return None
