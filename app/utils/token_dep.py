"""Token consumption dependency for data endpoints."""
from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User


def consume_token(
    x_user_id: str = Header(...),
    db: Session = Depends(get_db),
):
    """Check user has tokens and deduct one."""
    user = db.query(User).filter(User.id == x_user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user ID")
    if user.tokens <= 0:
        raise HTTPException(status_code=403, detail="No tokens remaining")

    user.tokens -= 1
    db.commit()
    db.refresh(user)
    return user
