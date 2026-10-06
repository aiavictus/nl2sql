import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import json

from app.llm import AVAILABLE_MODELS
from app.nl2sql import generate_sql


CASES_FILE = PROJECT_ROOT / "tests" / "evaluation_cases.json"


def evaluate_case(case, model):
    try:
        result = generate_sql(case["question"], model=model)
    except Exception as exc:
        return False, "error", f"Runtime error: {exc}"

    behavior = case["expected_behavior"]

    if behavior in {"accept", "sql"}:
        passed = bool(result["success"] and result["sql"])
        return passed, "accept", result["message"]

    if behavior == "clarification":
        passed = (
            not result["success"]
            and result["message"].startswith("CLARIFICATION_REQUIRED:")
        )
        return passed, "clarification", result["message"]

    if behavior in {"reject", "unsafe"}:
        passed = not result["success"]
        return passed, "reject", result["message"]

    return False, "unknown", result["message"]


def main():
    with open(CASES_FILE, encoding="utf-8") as file:
        cases = json.load(file)

    print(f"Evaluation cases: {len(cases)}")
    print()

    for model in AVAILABLE_MODELS:
        results = []

        print(f"=== {model} ===")

        for case in cases:
            passed, category, message = evaluate_case(case, model)

            results.append(
                {
                    "id": case["id"],
                    "type": case["type"],
                    "expected": case["expected_behavior"],
                    "passed": passed,
                }
            )

            status = "PASS" if passed else "FAIL"

            print(
                f"{status} {case['id']} | "
                f"{case['type']} | {message}"
            )

        total = len(results)
        passed = sum(r["passed"] for r in results)

        valid_cases = [
            r for r in results if r["type"] == "valid"
        ]
        clarification_cases = [
            r for r in results if r["type"] == "ambiguous"
        ]
        invalid_cases = [
            r for r in results
            if r["type"] in {"invalid_schema", "unsafe"}
        ]

        valid_passed = sum(r["passed"] for r in valid_cases)
        clarification_passed = sum(r["passed"] for r in clarification_cases)
        invalid_passed = sum(r["passed"] for r in invalid_cases)

        print()
        print(f"Overall:        {passed}/{total} ({passed / total * 100:.1f}%)")
        print(
            f"Valid SQL:      "
            f"{valid_passed}/{len(valid_cases)} "
            f"({valid_passed / len(valid_cases) * 100:.1f}%)"
        )
        print(
            f"Clarification:  "
            f"{clarification_passed}/{len(clarification_cases)} "
            f"({clarification_passed / len(clarification_cases) * 100:.1f}%)"
        )
        print(
            f"Rejection:      "
            f"{invalid_passed}/{len(invalid_cases)} "
            f"({invalid_passed / len(invalid_cases) * 100:.1f}%)"
        )
        print()


if __name__ == "__main__":
    main()