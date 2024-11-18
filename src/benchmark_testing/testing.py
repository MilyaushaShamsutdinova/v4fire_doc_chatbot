import pandas as pd
import time
from src.backend.pipeline import get_response
from collections import Counter


def load_dataset(file_path):
    data = pd.read_csv(file_path)
    return data["question"], data["answer"]


def query_rag_system(question):
    time.sleep(10)
    start_time = time.time()
    response = get_response(request=question)
    response_time = time.time() - start_time
    return response, response_time


def calculate_f1_score(reference, generated):
    reference_tokens = reference.split()
    generated_tokens = generated.split()

    ref_counter = Counter(reference_tokens)
    gen_counter = Counter(generated_tokens)

    common_tokens = ref_counter & gen_counter
    num_common_tokens = sum(common_tokens.values())

    if len(generated_tokens) == 0 or len(reference_tokens) == 0:
        return 0.0

    precision = num_common_tokens / len(generated_tokens)
    recall = num_common_tokens / len(reference_tokens)

    if precision + recall == 0:
        return 0.0
    f1 = 2 * (precision * recall) / (precision + recall)
    return f1


def test_rag_system(file_path):
    questions, reference_answers = load_dataset(file_path)
    
    generated_answers = []
    total_response_time = 0

    print(len(questions))
    for i in range(len(questions)):
        generated_answer, response_time = query_rag_system(questions[i])
        generated_answers.append(generated_answer)
        total_response_time += response_time

    f1_scores = [
        calculate_f1_score(ref, gen)
        for ref, gen in zip(reference_answers, generated_answers)
    ]

    avg_f1_score = sum(f1_scores) / len(f1_scores)
    avg_response_time = total_response_time / len(questions)

    print(f"Average F1 Score: {avg_f1_score:.4f}")
    print(f"Average Response Time: {avg_response_time:.4f} seconds")


test_rag_system("test_dataset.csv")
