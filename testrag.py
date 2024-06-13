import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from langchain_community.llms.ollama import Ollama
from run import query_bot

EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""

def calculate_similarity(expected, actual):
    vectorizer = TfidfVectorizer().fit_transform([expected, actual])
    vectors = vectorizer.toarray()
    cos_sim = cosine_similarity(vectors)
    return cos_sim[0][1]

def query_and_validate(question: str, expected_response: str):
    response_text = query_bot(question)
    prompt = EVAL_PROMPT.format(
        expected_response=expected_response, actual_response=response_text
    )

    model = Ollama(model="mistral")
    evaluation_results_str = model.invoke(prompt)
    evaluation_results_str_cleaned = evaluation_results_str.strip().lower()

    similarity_score = calculate_similarity(expected_response, response_text)

    print(prompt)

    if "true" in evaluation_results_str_cleaned:
        print("\033[92m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return True, similarity_score, response_text
    elif "false" in evaluation_results_str_cleaned:
        print("\033[91m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return False, similarity_score, response_text
    else:
        raise ValueError(
            f"Invalid evaluation result. Cannot determine if 'true' or 'false'."
        )

query_response_pairs = pd.read_csv('testdata.csv')

results = []

for index, row in query_response_pairs.iterrows():
    question = row['question']
    expected_response = row['expected_response']
    
    try:
        match, similarity, actual_response = query_and_validate(question, expected_response)
        results.append({
            "Question": question,
            "Expected Response": expected_response,
            "Actual Response": actual_response,
            "Match": match,
            "Similarity": similarity
        })
    except Exception as e:
        results.append({
            "Question": question,
            "Expected Response": expected_response,
            "Actual Response": str(e),
            "Match": False,
            "Similarity": 0.0
        })

df_results = pd.DataFrame(results)

print(df_results)
df_results.to_csv("chatbot_evaluation_results.csv", index=False)

