
from core.retrieval import retrieve_chunks
import json
import pandas as pd

def testing_questions(questions):
    j = 0
    with open("FILE PATH", "a") as file:
        for question in questions:
            query = question
            results = retrieve_chunks(query)
            i = 0 
            testcase_results = []
            for result in results:
                document, similarity_score = result
                metadata = document.metadata
                chunk_id = metadata.get("_id")
                rank = i + 1

                result_row = {"Chunk_id": chunk_id, "rank": rank, "score": similarity_score}
                testcase_results.append(result_row)
                
                i += 1
    
            testcase = {
                f"TC00{j}": {
                    "Question": query,
                    "results": testcase_results
                }
            }
            file.write(json.dumps(testcase) + "\n")
            j += 1




if __name__ == "__main__":

    test_data = pd.read_excel("FILE PATH")
    questions = test_data['Question']
    testing_questions(questions)
    