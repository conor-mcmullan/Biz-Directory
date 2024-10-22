from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel, condecimal, EmailStr, field_validator


class Review(BaseModel):
    reviewID: ObjectId
    review_ts: datetime
    rating: condecimal(gt=-0.01, lt=5.01, decimal_places=2)
    description: str
    reviewerEmail: EmailStr  # Pydantic will validate this
    reviewerName: str

    @field_validator('reviewerEmail')
    @classmethod
    def validate_reviewer_email(cls, v: str) -> str:
        if not v:
            raise ValueError("Reviewer email cannot be empty.")
        return v  # Already validated by EmailStr

