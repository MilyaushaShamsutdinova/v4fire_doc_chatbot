from src.backend.retrieval import retrieve_relevant
from src.backend.llm import GeminiAI


gemini = GeminiAI()

def get_response(request: str):
    rel_docs = retrieve_relevant(request)
    content = " ".join(rel_docs)
    response = gemini.get_response(request, content)
    return response


# request = "write component that creates button based on icon using b-icon-button"
# response = get_response(request)

# print(response)
