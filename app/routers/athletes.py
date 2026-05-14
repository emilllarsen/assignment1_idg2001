"""Athlete data endpoint."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.olympic_event import OlympicEvent
from app.utils.response_format import format_response
from app.utils.token_dep import consume_token, deduct_token

router = APIRouter()


@router.get("/athlete/{name}")
def get_athlete(
    name: str,
    fmt: str = Query(default="json"),
    db: Session = Depends(get_db),
    user=Depends(consume_token),
):
    """Search for an athlete by name and return their Olympic results."""
    search_name = name.replace("-", " ")
    matching_records = db.query(OlympicEvent).filter(
        OlympicEvent.name.ilike(f"%{search_name}%")
    ).all()

    if not matching_records:
        raise HTTPException(status_code=404, detail="Athlete not found")

    deduct_token(user, db)
    results = []
    for record in matching_records:
        results.append({
            "name": record.name,
            "sport": record.sport,
            "event": record.event,
            "year": record.year,
            "city": record.city,
            "noc": record.noc,
            "medal": record.medal,
        })

    data = {"athlete": name, "count": len(results), "results": results}
    return format_response(data, fmt)
