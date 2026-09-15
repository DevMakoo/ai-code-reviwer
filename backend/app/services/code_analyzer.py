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


def generate_summary(issues: list[dict]) -> str:
    if not issues:
        return "No obvious issues were detected."

    severity_counts = {
        "critical": 0,
        "warning": 0,
        "info": 0
    }

    for issue in issues:
        severity = issue["severity"]

        if severity in severity_counts:
            severity_counts[severity] += 1

    parts = []

    if severity_counts["critical"] > 0:
        parts.append(
            f"{severity_counts['critical']} critical"
        )

    if severity_counts["warning"] > 0:
        parts.append(
            f"{severity_counts['warning']} warning"
        )

    if severity_counts["info"] > 0:
        parts.append(
            f"{severity_counts['info']} info"
        )

    return f"{len(issues)} issue(s) detected: {', '.join(parts)}."


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
                    "rule": "syntax-error",
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
    summary = generate_summary(issues)

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