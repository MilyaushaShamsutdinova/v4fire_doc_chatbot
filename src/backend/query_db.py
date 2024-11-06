from src.db_prep.vector_db import VectorDB
import os

db = VectorDB(db_name="docs")

print(len(db))

# query_text = "write component that creates button based on icon using b-icon-button"
# results = db.query(query_text=query_text, n_results=3)

# for result in results:
#     # print("Document:", result)
#     print(result)

# print(results)
