import pandas as pd
from pathlib import Path
import json
from core.retrieval import retrieve_chunks
from core.generation import generate_response

import google.generativeai as genai
from config.setting import setting

def testing_gen_with_retriever(model, test_data):
    history = ""
    output_path = (
        Path(__file__).resolve().parent.parent
        / "evals"
        / "generation_evalutation_result.jsonl"
    )

    with output_path.open("a", encoding="utf-8") as file:
        for test in test_data.to_dict(orient="records"):
            query = test["Question"]
            test_id = test["Test_id"]

            context = retrieve_chunks(query)
            testcase_results = []
            i = 0
            for result in context:
                document, similarity_score = result
                metadata = document.metadata
                chunk_id = metadata.get("_id")
                rank = i + 1

                result_row = {"Chunk_id": chunk_id, "rank": rank, "score": similarity_score}
                testcase_results.append(result_row)
                
                i += 1

            result = generate_response(model, query, context, history)
            result_row = {
                "Test_id": test_id,
                "Generated Answer": result.answer,
                "Category": result.category.value,
                "Retrieve_chunks" : json.dumps(testcase_results),
                "Faithfulness": 0,
                "Correctness": 0,
                "Relevance": 0,
                "Completeness": 0,
                "Evaluation Reason": "",
                "Final_Status": "",
            }
            file.write(json.dumps(result_row, ensure_ascii=False) + "\n")





if __name__ == "__main__":

    test_data = pd.read_excel(
        "FILE PATH"
        "generation_withretriever_test.xlsx"
    )
    genai.configure(api_key=setting.gemini_api_key)
    model = genai.GenerativeModel(setting.gemini_model)


    testing_gen_with_retriever(model,test_data)


