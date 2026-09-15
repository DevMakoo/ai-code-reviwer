import ast


def analyze_python_code(code: str):
    issues = []

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

    for node in ast.walk(tree):

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):

                if node.func.id == "print":
                    issues.append({
                        "severity": "info",
                        "category": "code-quality",
                        "line": node.lineno,
                        "message": "Debug output detected.",
                        "suggestion": "Consider using a logging system instead of print()."
                    })

                if node.func.id == "eval":
                    issues.append({
                        "severity": "critical",
                        "category": "security",
                        "line": node.lineno,
                        "message": "Use of eval() detected.",
                        "suggestion": "Avoid eval() because it can execute arbitrary code."
                    })

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if "password" in target.id.lower():
                        issues.append({
                            "severity": "critical",
                            "category": "security",
                            "line": node.lineno,
                            "message": "Possible hardcoded password detected.",
                            "suggestion": "Never store passwords directly in source code."
                        })

        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    issues.append({
                        "severity": "warning",
                        "category": "code-quality",
                        "line": node.lineno,
                        "message": "Wildcard import detected.",
                        "suggestion": "Import only the specific names you need."
                    })

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if len(node.args.args) > 5:
                issues.append({
                    "severity": "warning",
                    "category": "code-quality",
                    "line": node.lineno,
                    "message": "Function has too many parameters.",
                    "suggestion": "Consider grouping related parameters into an object or data structure."
                })

        if isinstance(node, ast.ExceptHandler):
            if node.type is None:
                issues.append({
                    "severity": "warning",
                    "category": "code-quality",
                    "line": node.lineno,
                    "message": "Generic exception handler detected.",
                    "suggestion": "Catch specific exceptions instead of using a bare except."
                })

    if not issues:
        score = 100
        summary = "No obvious issues were detected."
    else:
        score = max(0, 100 - len(issues) * 15)
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