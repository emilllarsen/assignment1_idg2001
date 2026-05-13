"""Athlete data endpoint."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.olympic_event import OlympicEvent
from app.utils.token_dep import consume_token

router = APIRouter()


@router.get("/athlete/{name}")
def get_athlete(
    name: str,
    db: Session = Depends(get_db),
    user=Depends(consume_token),
):
    """Return all Olympic results for an athlete."""
    search = name.replace("-", " ")
    rows = db.query(OlympicEvent).filter(
        OlympicEvent.name.ilike(f"%{search}%")
    ).all()

    if not rows:
        raise HTTPException(status_code=404, detail="Athlete not found")

    results = [
        {
            "name": r.name,
            "sport": r.sport,
            "event": r.event,
            "year": r.year,
            "city": r.city,
            "noc": r.noc,
            "medal": r.medal,
        }
        for r in rows
    ]

    return {"athlete": name, "count": len(results), "results": results}
