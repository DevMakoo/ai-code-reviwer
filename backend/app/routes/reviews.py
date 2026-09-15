from fastapi import APIRouter

from app.schemas.review import ReviewRequest, ReviewResponse
from app.services.code_analyzer import analyze_code


router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)


@router.post("/", response_model=ReviewResponse)
def create_review(review: ReviewRequest):
    analysis = analyze_code(
        review.code,
        review.language
    )

    return {
        "id": 1,
        "language": review.language,
        "score": analysis["score"],
        "summary": analysis["summary"],
        "issues": analysis["issues"]
    }