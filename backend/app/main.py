from fastapi import FastAPI

from app.routes.reviews import router as reviews_router


app = FastAPI(
    title="AI Code Reviewer",
    description="AI-powered code review API",
    version="0.1.0"
)


app.include_router(reviews_router)


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