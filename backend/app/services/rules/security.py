import ast


def detect_security_issues(tree: ast.AST):
    issues = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
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

    return issues