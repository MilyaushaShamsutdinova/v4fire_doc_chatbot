from src.db_prep.fetch_data import fetch_github_docs
from src.db_prep.vector_db import VectorDB


def populate_db(db_name: str):
    db = VectorDB(db_name)
    repo_owner = "V4Fire"
    repos = ["Client", "Core"]

    for repo in repos:
        docs = fetch_github_docs(repo_owner, repo)
        db.add(docs)


populate_db(db_name="docs")
