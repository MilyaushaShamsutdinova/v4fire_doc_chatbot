from fetch_data import fetch_github_docs
from vector_db import VectorDB
import time


db = VectorDB("docs")

repo_owner = "V4Fire"
repos = ["Client", "Core"]

s = time.time()
for repo in repos:
    print(len(db))
    docs = fetch_github_docs(repo_owner, repo)
    db.add(docs)
e = time.time()

print(len(db))
print(e-s)
