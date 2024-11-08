from src.db_prep.vector_db import VectorDB


def is_request_in_db(request: str):
    db = VectorDB(db_name="qa_db")
    results = db.query(query_text=request, n_results=1)
    if len(results["ids"][0]) < 1:
        return False
    if results['distances'][0][0] < 0.1:
        return True
    return False


def get_response_from_db(request: str):
    db = VectorDB(db_name="qa_db")
    results = db.query(query_text=request, n_results=1)
    # return results
    return results['metadatas'][0][0]['response']


def store_in_db(request: str, response: str):
    db = VectorDB(db_name="qa_db")
    db.add([{"document": request, "metadata": {"response": response}}])


def clear_db():
    db = VectorDB(db_name="qa_db")
    db.clear_collection("qa_db")


# clear_db()

