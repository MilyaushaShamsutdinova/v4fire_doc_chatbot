import spacy

nlp = spacy.load("en_core_web_sm")
technical_keywords = {"implement", "code", "integration", "detailed", "write"}
moderate_keywords = {"features", "benefits", "key points", "general", "usage", "principles"}
general_keywords = {"what", "who", "when", "where", "overview", "summary", "introduction", "explain"}


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

# # Example usage
# queries = [
#     "How do I implement a custom dependency injection in V4Fire?",
#     "What are the key features of V4Fire framework?",
#     "Explain the architecture of V4Fire in detail.",
#     "What's V4Fire?",
#     "Who developed V4Fire?",
#     "Where can I find V4Fire documentation?"
# ]

# for query in queries:
#     complexity = estimate_query_complexity(query)
#     print(f"Query: \"{query}\"\nComplexity Level: {complexity}\n")
