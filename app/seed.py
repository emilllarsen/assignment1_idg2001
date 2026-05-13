"""Loads the Kaggle CSV into the database."""
import os
import pandas as pd
from app.database import SessionLocal
from app.models.olympic_event import OlympicEvent


def seed_database():
    """Seed the olympic_events table from the CSV file."""
    db = SessionLocal()
    try:
        count = db.query(OlympicEvent).count()
        if count > 0:
            print(f"Database already seeded ({count} records). Skipping.")
            return

        csv_path = os.path.join(
            os.path.dirname(__file__), "data", "athlete_events.csv"
        )
        if not os.path.exists(csv_path):
            print("CSV not found in data/ folder!")
            return

        print("Seeding database... this may take a moment.")
        df = pd.read_csv(csv_path)

        records = []
        for _, row in df.iterrows():
            record = OlympicEvent(
                name=row.get("Name"),
                sex=row.get("Sex"),
                age=clean_float(row.get("Age")),
                height=clean_float(row.get("Height")),
                weight=clean_float(row.get("Weight")),
                team=row.get("Team"),
                noc=row.get("NOC"),
                games=row.get("Games"),
                year=clean_int(row.get("Year")),
                season=row.get("Season"),
                city=row.get("City"),
                sport=row.get("Sport"),
                event=row.get("Event"),
                medal=clean_str(row.get("Medal")),
            )
            records.append(record)

        chunk_size = 5000
        for i in range(0, len(records), chunk_size):
            db.bulk_save_objects(records[i:i + chunk_size])
            db.commit()
            n = min(i + chunk_size, len(records))
            print(f"  Inserted {n}/{len(records)}")

        print("Seeding complete!")
    finally:
        db.close()


def clean_float(val):
    """Convert a value to float, returning None for NaN or missing."""
    try:
        f = float(val)
        if pd.isna(f):
            return None
        return f
    except (ValueError, TypeError):
        return None


def clean_int(val):
    """Convert a value to int, returning None for NaN or missing."""
    f = clean_float(val)
    return int(f) if f is not None else None


def clean_str(val):
    """Convert a value to string, returning None for NaN or missing."""
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return None
    s = str(val).strip()
    return s if s and s.lower() != "nan" else None
