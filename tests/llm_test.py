import ast
import json
from pathlib import Path

import google.generativeai as genai
import pandas as pd

from config.setting import setting
from core.generation import generate_response


def _normalize_context(value):
    if isinstance(value, str):
        context_text = value.strip()
        if not context_text:
            raise ValueError("Reference Context cannot be empty")

        try:
            value = ast.literal_eval(context_text)
        except (SyntaxError, ValueError):
            return [(context_text, 0.0)]

        if isinstance(value, str) and value.strip():
            return [(value.strip(), 0.0)]

    if isinstance(value, (list, tuple)):
        if not value:
            raise ValueError("Reference Context cannot be empty")

        if (
            len(value) == 2
            and isinstance(value[0], str)
            and isinstance(value[1], (int, float))
        ):
            return [tuple(value)]

        normalized = []
        for item in value:
            if isinstance(item, (list, tuple)) and len(item) == 2:
                normalized.append(tuple(item))
            elif isinstance(item, str) and item.strip():
                normalized.append((item, 0.0))
            else:
                raise TypeError(
                    "Reference Context must contain text or two-item entries"
                )
        return normalized

    if pd.isna(value):
        raise ValueError("Reference Context cannot be empty")

    raise TypeError(
        "Reference Context must be a string or a list of two-item entries"
    )


def testing_llm_gen(model, test_data):
    history = ""
    output_path = (
        Path(__file__).resolve().parent.parent
        / "evals"
        / "llm_evaluation_result.jsonl"
    )

    with output_path.open("a", encoding="utf-8") as file:
        for test in test_data.to_dict(orient="records"):
            query = test["Question"]
            test_id = test["Test_id"]
            context = _normalize_context(test["Reference Context"])
            result = generate_response(model, query, context, history)
            result_row = {
                "Test_id": test_id,
                "Generated Answer": result.answer,
                "Category": result.category.value,
                "Faithfulness": 0,
                "Correctness": 0,
                "Relevance": 0,
                "Completeness": 0,
                "Evaluation Reason": "",
                "Final_Status": "",
            }
            file.write(json.dumps(result_row, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    genai.configure(api_key=setting.gemini_api_key)
    model = genai.GenerativeModel(setting.gemini_model)

    test_data = pd.read_excel(
        "FILE PATH"
        "independent_evaluation_result.xlsx"
    )
    testing_llm_gen(model, test_data)
