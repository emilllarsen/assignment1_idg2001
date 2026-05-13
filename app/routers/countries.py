"""Country data endpoint."""
from app.utils.token_dep import consume_token
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.utils.response_format import format_response
from app.models.olympic_event import OlympicEvent
from app.database import get_db

router = APIRouter()


@router.get("/country/{noc}")
def get_country(
    noc: str,
    fmt: str = Query(default="json"),
    db: Session = Depends(get_db),
    user=Depends(consume_token),
):
    """Return medal summary for a country grouped by sport."""
    noc = noc.upper()
    rows = db.query(OlympicEvent).filter(OlympicEvent.noc == noc).all()

    if not rows:
        raise HTTPException(status_code=404, detail="Country not found")

    sports = {}
    for row in rows:
        sport = row.sport
        if sport not in sports:
            sports[sport] = {
                "gold": 0, "silver": 0, "bronze": 0,
                "participations": 0,
            }
        sports[sport]["participations"] += 1
        if row.medal == "Gold":
            sports[sport]["gold"] += 1
        elif row.medal == "Silver":
            sports[sport]["silver"] += 1
        elif row.medal == "Bronze":
            sports[sport]["bronze"] += 1

    return format_response({"noc": noc, "sports": sports}, fmt)
