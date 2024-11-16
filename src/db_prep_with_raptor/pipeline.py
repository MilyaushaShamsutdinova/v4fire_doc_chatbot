from src.db_prep_with_raptor.fetch_data import fetch_github_docs
from src.db_prep_with_raptor.vector_db import VectorDB
from src.db_prep_with_raptor.summary import *


def populate_db_with_original_docs(db_name: str):
    db = VectorDB(db_name)
    repo_owner = "V4Fire"
    repos = ["Client", "Core"]

    for repo in repos:
        docs = fetch_github_docs(repo_owner, repo)
        print(f"Data fetched from {repo}")

        db.add(docs)
        print("Data added")


def populate_db_with_summaries(up_to_level: int=2):
    for lvl in range(up_to_level):
        clusters = cluster_documents(level=lvl)
        print(f"Num of clusters in docs_{lvl}: {len(clusters)}")

        summaries = generate_summary(clusters)
        print(f"{len(summaries)} summaries (docs_{lvl}) generated")

        store_summaries(summaries, level=lvl+1)
        print(f"Summaries succesfully saved in docs_{lvl+1}")


def create_and_populate_db():
    populate_db_with_original_docs(db_name="docs_0")
    populate_db_with_summaries(up_to_level=2)


create_and_populate_db()
