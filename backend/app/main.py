from fastapi import FastAPI

app = FastAPI(
    title="AI Code Reviewer",
    description="AI-powered code review API",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "message": "AI Code Reviewer API",
        "status": "online"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }