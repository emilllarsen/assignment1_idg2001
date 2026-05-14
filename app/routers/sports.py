"""Sport data endpoint. Supports filtering by country, year, season and medals."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.olympic_event import OlympicEvent
from app.utils.response_format import format_response
from app.utils.token_dep import consume_token, deduct_token

router = APIRouter()


@router.get("/sport/{sport_name}")
def get_sport(
    sport_name: str,
    fmt: str = Query(default="json"),
    country: Optional[str] = Query(default=None),
    year: Optional[int] = Query(default=None),
    season: Optional[str] = Query(default=None),
    medals: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    user=Depends(consume_token),
):
    """Get all results for a sport. Can be filtered by country, year, season and medals."""
    search_name = sport_name.replace("-", " ")
    db_query = db.query(OlympicEvent).filter(
        OlympicEvent.sport.ilike(f"%{search_name}%")
    )

    if country:
        db_query = db_query.filter(OlympicEvent.noc == country.upper())
    if year:
        db_query = db_query.filter(OlympicEvent.year == year)
    if season:
        db_query = db_query.filter(OlympicEvent.season.ilike(season))
    if medals:
        if medals.lower() == "any":
            db_query = db_query.filter(OlympicEvent.medal.isnot(None))
        else:
            db_query = db_query.filter(OlympicEvent.medal.ilike(medals))

    matching_records = db_query.all()

    if not matching_records:
        raise HTTPException(status_code=404, detail="Sport not found")

    deduct_token(user, db)
    results = []
    for record in matching_records:
        results.append({
            "name": record.name,
            "event": record.event,
            "year": record.year,
            "noc": record.noc,
            "medal": record.medal,
        })

    return format_response(
        {
            "sport": sport_name.replace("-", " ").title(),
            "filters": {
                "country": country,
                "year": year,
                "season": season,
                "medals": medals,
            },
            "count": len(results),
            "results": results,
        },
        fmt,
    )
