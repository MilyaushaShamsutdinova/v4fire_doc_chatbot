from src.db_prep.vector_db import VectorDB


def is_request_in_db(request: str):
    db = VectorDB(db_name="qa_db")
    results = db.query(query_text=request, n_results=1)
    if results['distances'][0][0] < 0.1:
        return True
    return False


def get_response_from_db(request: str):
    db = VectorDB(db_name="qa_db")
    results = db.query(query_text=request, n_results=1)
    return results['metadatas'][0]['response']


def store_in_db(request: str, response: str):
    db = VectorDB(db_name="qa_db")
    db.add([{"document": request, "metadata": {"response": response}}])
