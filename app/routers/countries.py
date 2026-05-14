"""Country data endpoint."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.olympic_event import OlympicEvent
from app.utils.response_format import format_response
from app.utils.token_dep import consume_token, deduct_token

router = APIRouter()


@router.get("/country/{noc}")
def get_country(
    noc: str,
    fmt: str = Query(default="json"),
    db: Session = Depends(get_db),
    user=Depends(consume_token),
):
    """Get all Olympic results for a country, grouped by sport."""
    noc = noc.upper()
    matching_records = db.query(OlympicEvent).filter(OlympicEvent.noc == noc).all()

    if not matching_records:
        raise HTTPException(status_code=404, detail="Country not found")

    deduct_token(user, db)
    sports_summary = {}
    for record in matching_records:
        sport_name = record.sport
        if sport_name not in sports_summary:
            sports_summary[sport_name] = {
                "gold": 0, "silver": 0, "bronze": 0,
                "participations": 0,
            }
        sports_summary[sport_name]["participations"] += 1
        if record.medal == "Gold":
            sports_summary[sport_name]["gold"] += 1
        elif record.medal == "Silver":
            sports_summary[sport_name]["silver"] += 1
        elif record.medal == "Bronze":
            sports_summary[sport_name]["bronze"] += 1

    return format_response({"noc": noc, "sports": sports_summary}, fmt)
