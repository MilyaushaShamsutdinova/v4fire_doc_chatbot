from fetch_data import fetch_github_docs
from vector_db import VectorDB

db = VectorDB("docs")

repo_owner = "V4Fire"
repos = ["Client", "Core"]

for repo in repos:
    docs = fetch_github_docs(repo_owner, repo)
    db.add(docs)
    