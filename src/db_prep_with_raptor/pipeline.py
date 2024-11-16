from src.db_prep_with_raptor.fetch_data import fetch_github_docs
from src.db_prep_with_raptor.vector_db import VectorDB
from src.db_prep_with_raptor.summary import populate_db_with_summaries


def populate_db(db_name: str):
    db = VectorDB(db_name)
    repo_owner = "V4Fire"
    # repos = ["Client", "Core"]
    repos = ["Core"]

    for repo in repos:
        docs = fetch_github_docs(repo_owner, repo)
        db.add(docs)


# populate_db(db_name="docs_0")
# populate_db_with_summaries(up_to_level=2)