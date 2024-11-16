from src.backend.retrieval import retrieve_relevant_docs
from src.backend.llm import GeminiAI
from src.backend.qa_db import *


gemini = GeminiAI()

def get_response(request: str):
    if is_request_in_db(request):
        response = get_response_from_db(request)
        return response

    relevant_docs = retrieve_relevant_docs(request)

    if not relevant_docs:
        response = "I cannot answer this question. But feel free to ask any question related to V4Fire!"
    else:
        content = " ".join(relevant_docs)
        response = gemini.get_response(request, content)
        store_in_db(request, response)

    return response


# request = "write component that creates button based on icon using b-icon-button"
# response = get_response(request)

# print(response)
