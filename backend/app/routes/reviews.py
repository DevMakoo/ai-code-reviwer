from fastapi import APIRouter

from app.schemas.review import ReviewRequest, ReviewResponse
from app.services.code_analyzer import analyze_code
from app.services.ai_reviewer import generate_ai_review


router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)


@router.post("/", response_model=ReviewResponse)
def create_review(review: ReviewRequest):
    static_analysis = analyze_code(
        review.code,
        review.language
    )

    ai_review = generate_ai_review(
        review.code,
        review.language,
        static_analysis
    )

    return {
        "id": 1,
        "language": review.language,
        "score": static_analysis["score"],
        "summary": static_analysis["summary"],
        "issues": static_analysis["issues"]
    }