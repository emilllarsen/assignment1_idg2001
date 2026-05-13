"""Sport data endpoint with query parameter support."""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.olympic_event import OlympicEvent
from app.utils.token_dep import consume_token

router = APIRouter()


@router.get("/sport/{sport_name}")
def get_sport(
    sport_name: str,
    country: Optional[str] = Query(default=None),
    year: Optional[int] = Query(default=None),
    season: Optional[str] = Query(default=None),
    medals: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    user=Depends(consume_token),
):
    """Return Olympic results for a sport with optional filters."""
    search = sport_name.replace("-", " ")
    query = db.query(OlympicEvent).filter(
        OlympicEvent.sport.ilike(f"%{search}%")
    )

    if country:
        query = query.filter(OlympicEvent.noc == country.upper())
    if year:
        query = query.filter(OlympicEvent.year == year)
    if season:
        query = query.filter(OlympicEvent.season.ilike(season))
    if medals:
        if medals.lower() == "any":
            query = query.filter(OlympicEvent.medal.isnot(None))
        else:
            query = query.filter(OlympicEvent.medal.ilike(medals))

    rows = query.all()

    results = [
        {
            "name": r.name,
            "event": r.event,
            "year": r.year,
            "noc": r.noc,
            "medal": r.medal,
        }
        for r in rows
    ]

    return {
        "sport": sport_name.replace("-", " ").title(),
        "filters": {
            "country": country,
            "year": year,
            "season": season,
            "medals": medals,
        },
        "count": len(results),
        "results": results,
    }
