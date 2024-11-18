from src.backend.llm import GeminiAI
from src.db_prep_with_raptor.vector_db import VectorDB
import random
import ast
import csv


def retrieve_random_docs(n_docs_0=75, n_docs_1=20, n_docs_2=5):
    db_docs_0 = VectorDB("docs_0")
    db_docs_1 = VectorDB("docs_1")
    db_docs_2 = VectorDB("docs_2")

    docs_0 = db_docs_0.get_docs()['documents']
    docs_1 = db_docs_1.get_docs()['documents']
    docs_2 = db_docs_2.get_docs()['documents']

    random_n_from_docs_0 = random.sample(docs_0, n_docs_0)
    random_n_from_docs_1 = random.sample(docs_1, n_docs_1)
    random_n_from_docs_2 = random.sample(docs_2, n_docs_2)

    random_docs = random_n_from_docs_0
    random_docs.extend(random_n_from_docs_1)
    random_docs.extend(random_n_from_docs_2)

    return random_docs


def extract_json_snippet(response_text):
    start = response_text.find('{')
    end = response_text.rfind('}')
    if start != -1 and end != -1:
        json_string = response_text[start:end + 1]
        
        try:
            extracted_dict = ast.literal_eval(json_string)
            return extracted_dict
        except Exception as e:
            print(f"{e}: {response_text}")
            return None
    else:
        print(f"No valid JSON structure found: {response_text}")
        return None
    

def generate_dataset(docs):
    gemini = GeminiAI()
    file_name = 'test_dataset.csv'

    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["question", "answer"])
        writer.writeheader()

        for doc in docs:
            qa = gemini.generate_qa(doc)
            qa = extract_json_snippet(qa)
            if qa:
                row = {
                    "question": qa['question'],
                    "answer": qa['answer'],
                }
                writer.writerow(row)


rand_docs = retrieve_random_docs()
generate_dataset(rand_docs)
