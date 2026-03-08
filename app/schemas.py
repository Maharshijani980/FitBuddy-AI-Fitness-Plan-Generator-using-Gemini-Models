from pydantic import BaseModel


# -------------------------
# User Input Schema
# -------------------------

class UserInput(BaseModel):
    name: str
    age: int
    weight: int
    goal: str
    intensity: str


# -------------------------
# Feedback Schema
# -------------------------

class FeedbackRequest(BaseModel):
    user_id: int
    feedback: str