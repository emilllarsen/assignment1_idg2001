"""Token management endpoint."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas import TokenAdd, TokenResponse

router = APIRouter()


@router.post("/tokens", response_model=TokenResponse)
def add_tokens(payload: TokenAdd, db: Session = Depends(get_db)):
    """Add tokens to a user's account."""
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.tokens += payload.amount
    db.commit()
    db.refresh(user)

    return {
        "user_id": user.id,
        "tokens": user.tokens,
        "message": (
            f"Added {payload.amount} tokens."
            f" New balance: {user.tokens}"
        ),
    }
