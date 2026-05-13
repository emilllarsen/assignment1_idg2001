"""Event creation endpoint."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.olympic_event import OlympicEvent
from app.utils.token_dep import consume_token

router = APIRouter()


@router.post("/event", status_code=201)
def create_event(
    payload: dict,
    db: Session = Depends(get_db),
    user=Depends(consume_token),
):
    """Create a new athlete participation record."""
    event = OlympicEvent(
        name=payload.get("name"),
        sex=payload.get("sex"),
        age=payload.get("age"),
        height=payload.get("height"),
        weight=payload.get("weight"),
        team=payload.get("team"),
        noc=payload.get("noc", "").upper(),
        games=payload.get("games"),
        year=payload.get("year"),
        season=payload.get("season"),
        city=payload.get("city"),
        sport=payload.get("sport"),
        event=payload.get("event"),
        medal=payload.get("medal"),
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    return {"message": "Event created", "id": event.id}
