import ast


def detect_code_quality_issues(tree: ast.AST):
    issues = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id == "print":
                    issues.append({
                        "severity": "info",
                        "category": "code-quality",
                        "rule": "debug-print",
                        "line": node.lineno,
                        "message": "Debug output detected.",
                        "suggestion": "Consider using a logging system instead of print()."
                    })

        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    issues.append({
                        "severity": "warning",
                        "category": "code-quality",
                        "rule": "wildcard-import",
                        "line": node.lineno,
                        "message": "Wildcard import detected.",
                        "suggestion": "Import only the specific names you need."
                    })

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if len(node.args.args) > 5:
                issues.append({
                    "severity": "warning",
                    "category": "code-quality",
                    "rule": "too-many-parameters",
                    "line": node.lineno,
                    "message": "Function has too many parameters.",
                    "suggestion": "Consider grouping related parameters into an object or data structure."
                })

        if isinstance(node, ast.ExceptHandler):
            if node.type is None:
                issues.append({
                    "severity": "warning",
                    "category": "code-quality",
                    "rule": "bare-except",
                    "line": node.lineno,
                    "message": "Generic exception handler detected.",
                    "suggestion": "Catch specific exceptions instead of using a bare except."
                })

    return issues