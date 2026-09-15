from app.services.code_analyzer import analyze_code


def test_detects_print():
    result = analyze_code(
        "print('Hello World')",
        "python"
    )

    assert result["score"] < 100
    assert len(result["issues"]) == 1
    assert result["issues"][0]["category"] == "code-quality"


def test_detects_eval():
    result = analyze_code(
        "eval(user_input)",
        "python"
    )

    assert result["score"] < 100
    assert result["issues"][0]["severity"] == "critical"
    assert result["issues"][0]["category"] == "security"


def test_detects_hardcoded_password():
    result = analyze_code(
        'password = "123456"',
        "python"
    )

    assert result["score"] < 100
    assert result["issues"][0]["category"] == "security"


def test_detects_syntax_error():
    result = analyze_code(
        "def hello(",
        "python"
    )

    assert result["score"] == 0
    assert result["issues"][0]["category"] == "syntax"


def test_clean_code():
    result = analyze_code(
        "name = 'Marco'",
        "python"
    )

    assert result["score"] == 100
    assert len(result["issues"]) == 0