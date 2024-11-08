from src.backend.retrieval import retrieve_relevant
from src.backend.llm import GeminiAI
from src.backend.qa_db import is_request_in_db, get_response_from_db, store_in_db


gemini = GeminiAI()

def get_response(request: str):

    # check if request already has a response in db
    if is_request_in_db(request):
        response = get_response_from_db(request)
        return response

    rel_docs = retrieve_relevant(request)
    content = " ".join(rel_docs)
    response = gemini.get_response(request, content)

    # store request and response in db
    store_in_db(request, response)

    return response


# request = "write component that creates button based on icon using b-icon-button"
# response = get_response(request)

# print(response)
