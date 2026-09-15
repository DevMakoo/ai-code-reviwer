import ast

from app.services.rules.security import detect_security_issues
from app.services.rules.code_quality import detect_code_quality_issues


SEVERITY_PENALTIES = {
    "critical": 30,
    "warning": 15,
    "info": 5
}


def calculate_score(issues: list[dict]) -> int:
    score = 100

    for issue in issues:
        penalty = SEVERITY_PENALTIES.get(
            issue["severity"],
            0
        )

        score -= penalty

    return max(0, score)


def analyze_python_code(code: str):
    try:
        tree = ast.parse(code)
    except SyntaxError as error:
        return {
            "score": 0,
            "summary": "The code contains a syntax error.",
            "issues": [
                {
                    "severity": "critical",
                    "category": "syntax",
                    "line": error.lineno or 1,
                    "message": error.msg,
                    "suggestion": "Fix the syntax error before running the code."
                }
            ]
        }

    issues = []

    issues.extend(
        detect_security_issues(tree)
    )

    issues.extend(
        detect_code_quality_issues(tree)
    )

    score = calculate_score(issues)

    if not issues:
        summary = "No obvious issues were detected."
    else:
        summary = f"{len(issues)} issue(s) detected."

    return {
        "score": score,
        "summary": summary,
        "issues": issues
    }


def analyze_code(code: str, language: str):
    if language.lower() == "python":
        return analyze_python_code(code)

    return {
        "score": 100,
        "summary": f"Analysis for {language} is not available yet.",
        "issues": []
    }