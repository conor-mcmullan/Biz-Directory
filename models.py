import re
from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel, Field, condecimal, EmailStr, field_validator
from typing import List, Optional

class ReviewModel(BaseModel):
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


class BusinessModel(BaseModel):
    businessID: ObjectId
    name: str
    address: str
    contactEmail: EmailStr  # Pydantic will validate this
    contactPhone: str  # Keep it as a string for validation
    businessType: Optional[str] = Field(None, description="Type or category of the business")
    reviews: Optional[List[ReviewModel]] = Field(default_factory=list)
    overallRating: condecimal(gt=-0.01, lt=5.01, decimal_places=2) = Field(0.00)

    @field_validator('name', 'businessType')
    @classmethod
    def check_alphanumeric(cls, v: str, info) -> str:
        if isinstance(v, str):
            is_alphanumeric = v.replace(' ', '').isalnum()
            assert is_alphanumeric, f'{info.field_name} must be alphanumeric.'
        return v

    @field_validator('contactPhone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        # Regex pattern for validating phone numbers
        pattern_international = re.compile(r'^\+?\d{1,3}\s?\d{9,15}$')  # For international format
        pattern_local = re.compile(r'^0\d{10,14}$')  # For local format starting with '0'

        # Check if it matches either of the patterns
        if not (pattern_international.match(v) or pattern_local.match(v)):
            raise ValueError(
                "Invalid phone number format. Expected formats: +44 02879549749, 07522432105, 447522432105, +4407522432105."
            )
        return v

    @field_validator('contactEmail')
    @classmethod
    def validate_contact_email(cls, v: str) -> str:
        if not v:
            raise ValueError("Contact email cannot be empty.")
        return v  # Already validated by EmailStr
